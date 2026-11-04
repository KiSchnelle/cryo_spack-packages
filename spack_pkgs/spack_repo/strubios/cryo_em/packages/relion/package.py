# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import hashlib
import os
import time

from spack.package import *
from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.builtin.build_systems.cuda import CudaPackage

ESM = "esm1b_t33_650M_UR50S"
ESM_SHA256 = "0569754efaff7dcb7e068c27367bc73f10afb4b450ea30aac30d9bc60783a8b1"
# Exact bytes, relative to <TORCH_HOME>/hub/checkpoints
WEIGHT_SIZES = {
    "relion_class_ranker/v1.0.ckpt": 2373099,
    "relion_blush/v1.0.ckpt": 51935787,
    "relion_blush/amy-v1.0.ckpt": 51949867,
    "relion_blush/amy-v1.0-lsd.ckpt": 51949959,
    "model_angelo_v1.0/nucleotides/c_alpha/chkpt.torch": 734237153,
    "model_angelo_v1.0/nucleotides/gnn/chkpt_483863.torch": 1603440621,
    "model_angelo_v1.0/nucleotides_no_seq/c_alpha/chkpt.torch": 734237153,
    "model_angelo_v1.0/nucleotides_no_seq/gnn/chkpt_329999.torch": 1189103291,
    f"{ESM}.pt": 7828576466,
    f"{ESM}-contact-regression.pt": 3174,
}
TRACER_SIZES = {
    "relion_trace_amyloids/amytracer-v2.0.ckpt": 1489216652,
    "relion_trace_amyloids/carbonpicker-v1.0.ckpt": 347270796,
}
WEIGHT_MARKERS = (
    "relion_class_ranker/v1.0_installed.txt",
    "relion_blush/v1.0_installed.txt",
    "relion_blush/amy-v1.0_installed.txt",
    "relion_blush/amy-v1.0-lsd_installed.txt",
    "model_angelo_v1.0/nucleotides/success.txt",
    "model_angelo_v1.0/nucleotides_no_seq/success.txt",
)
TRACER_MARKERS = (
    "relion_trace_amyloids/amytracer-v2.0_installed.txt",
    "relion_trace_amyloids/carbonpicker-v1.0_installed.txt",
)
# A stalled download otherwise hangs forever: torch.hub calls urlopen with no timeout.
FETCH_TIMEOUT = 4 * 3600


class Relion(CMakePackage, CudaPackage):
    """RELION (for REgularised LIkelihood OptimisatioN, pronounce rely-on) is a
    stand-alone computer program that employs an empirical Bayesian approach to
    refinement of (multiple) 3D reconstructions or 2D class averages in
    electron cryo-microscopy (cryo-EM)."""

    homepage = "https://www2.mrc-lmb.cam.ac.uk/relion"
    git = "https://github.com/3dem/relion.git"
    url = "https://github.com/3dem/relion/archive/5.1.1.zip"
    maintainers("dacolombo", "Markus92")

    license("GPL-2.0-only")

    version("5.1.1", sha256="1bf75dcf287fb6d591cd4194c0d0cddf98590ae36c54fafbbcb7aa4daef85ec6")
    version("5.1.0", sha256="714649163fbd7ee63cf9331d97751bd2e972703482349d8d7f2110387ef556d2")
    version("5.0.1", sha256="3253230cd4b3d9633a5cac906937039b9971eb9430c3e2d838473777fb811f4c")

    variant("cuda", default=True, description="Build with CUDA")
    conflicts("~cuda", msg="This site builds GPU RELION only")
    conflicts("cuda_arch=none", when="+cuda",
              msg="Must specify cuda_arch, see https://developer.nvidia.com/cuda-gpus")

    variant("gui", default=True, description="build the gui")
    variant("double", default=True, description="double precision (cpu) code")
    variant("double-gpu", default=False, description="double precision gpu")

    variant("own-fftw", default=True, description="Use bundled FFTW.")
    variant("amd-fftw", default=True, description="Use AMD's FFTW.")
    variant("mklfft", default=False, description="Use MKL rather than FFTW for FFT")

    conflicts("+mklfft", when="+own-fftw", msg="Cannot use MKL FFT with bundled FFTW")
    conflicts("+amd-fftw", when="+mklfft", msg="Cannot use AMD FFTW with MKL FFT")

    # Keep above def patch: the method would shadow the directive name.
    patch("relion_5.1.1_post_tag_fixes.patch", when="@5.1.1")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("fortran", type="build", when="+own-fftw")
    depends_on("mpi")
    depends_on("cmake@3.21:", type="build", when="@5.1:")
    depends_on("cmake@3:3", type="build", when="@:5.0")
    depends_on("binutils@2.32:", type="build")

    depends_on("amdfftw", when="~own-fftw +amd-fftw ~mklfft")
    depends_on("mkl", when="+mklfft")
    depends_on("fftw precision=float,double", when="~own-fftw ~amd-fftw ~mklfft")

    depends_on("ctffind@4", type="run")
    depends_on("ghostscript", type="run")
    # use the +xft variant so the interface is not so horrible looking
    depends_on("fltk+xft", when="+gui")
    depends_on("libtiff")
    depends_on("libpng")
    depends_on("pbzip2", type="run")
    depends_on("xz", type="run")
    depends_on("zstd", type="run")
    depends_on("cuda@12:")
    # relion_schemegui imports tkinter at top level; builtin python defaults to ~tkinter.
    depends_on("python+tkinter", when="+gui", type=("build", "run"))

    # The build edge must stay: the install-time weight fetch gets PYTHONPATH through it.
    for _v in ("5.0.1", "5.1.0", "5.1.1"):
        for _arch in CudaPackage.cuda_arch_values:
            depends_on(f"py-relion@={_v} +cuda cuda_arch={_arch}",
                       when=f"@={_v} +cuda cuda_arch={_arch}", type=("build", "run"))

    @property
    def _torch_home(self):
        return str(self.prefix.share.relion.torch_home)

    def patch(self):
        if self.spec.satisfies("@5.0.1"):
            # Backport 5e18e811: the Intel disguise breaks nvcc on GCC 13+ (#1313, #1315)
            filter_file("-D__INTEL_COMPILER ", "", "cmake/BuildTypes.cmake", string=True)
        if self.spec.satisfies("@5.1.0"):
            # 5.1.0's wrapper points at the deleted build stage; fixed upstream in 5.1.1
            filter_file('"@Relion_BINARY_DIR@"', '"@CMAKE_INSTALL_PREFIX@"',
                        "scripts/python_trace_amyloids.in", string=True)
        if self.spec.satisfies("@5.1:"):
            # torch.compile needs Triton on a GPU, and builtin py-torch does not depend on it.
            # PyPI wheels bring it, which is why upstream's conda environment works.
            filter_file(r"^\s*@torch\.compile\s*$", "", "scripts/trace_amyloids.py")

    @run_before("cmake")
    def create_torch_home(self):
        # FindCondaPython.cmake drops TORCH_HOME_PATH if the directory does not exist
        mkdirp(self._torch_home)

    def cmake_args(self):
        args = [
            "-DGUI=%s" % ("+gui" in self.spec),
            "-DDoublePrec_CPU=%s" % ("+double" in self.spec),
            self.define("DoublePrec_ACC", self.spec.satisfies("+double-gpu")),
            "-DFORCE_OWN_FFTW=%s" % ("+own-fftw" in self.spec),
            self.define("AMDFFTW", self.spec.satisfies("+own-fftw +amd-fftw")),
            "-DMKLFFT=%s" % ("+mklfft" in self.spec),
            self.define("CUDA", True),
            self.define("CUDA_ARCH", ";".join(self.spec.variants["cuda_arch"].value)),
            f"-DPYTHON_EXE_PATH={self.spec['python'].command.path}",
            "-DFETCH_WEIGHTS=OFF",
            self.define("TORCH_HOME_PATH", self._torch_home),
        ]
        if self.spec.satisfies("+gui"):
            incs = [f"-I{self.spec[lib].prefix.include}" for lib in ["libx11", "xproto"]]
            args += ["-DCMAKE_CXX_FLAGS=" + " ".join(incs)]
        return args

    def setup_run_environment(self, env):
        env.set("RELION_CTFFIND_EXECUTABLE", self.spec["ctffind"].prefix.bin.ctffind)
        env.set("RELION_QSUB_TEMPLATE", "/appl/scripts/relion5.sh")
        # Direct model_angelo calls read this; the wrappers use the baked path.
        env.set("TORCH_HOME", self._torch_home)
        # GUI defaults otherwise point at /public/EM. The tools come from Extra software.
        env.set("RELION_ARETOMO_EXECUTABLE", "AreTomo2")
        env.set("RELION_BATCHTOMO_EXECUTABLE", "batchruntomo")
        env.set("RELION_QUEUE_USE", "yes")
        env.set("RELION_QUEUE_NAME", "p.cryo")
        env.set("RELION_QSUB_COMMAND", "sbatch")
        env.set("RELION_SCRATCH_DIR", "/scratch/${SLURM_JOB_ID}/")
        env.set("RELION_QSUB_EXTRA_COUNT", "5")
        env.set("RELION_QSUB_EXTRA1", "Memory")
        env.set("RELION_QSUB_EXTRA1_DEFAULT", "50")
        env.set("RELION_QSUB_EXTRA1_HELP", "Sets the reserved about of RAM memory in GB.")
        env.set("RELION_QSUB_EXTRA2", "Mincpus")
        env.set("RELION_QSUB_EXTRA2_DEFAULT", "1")
        env.set("RELION_QSUB_EXTRA2_HELP", "Set the mincpus reseverd per node.")
        env.set("RELION_QSUB_EXTRA3", "Nodes")
        env.set("RELION_QSUB_EXTRA3_DEFAULT", "1")
        env.set("RELION_QSUB_EXTRA3_HELP", "Sets the nodes reserved.")
        env.set("RELION_QSUB_EXTRA4", "GPUs")
        env.set("RELION_QSUB_EXTRA4_DEFAULT", "0")
        env.set("RELION_QSUB_EXTRA4_HELP", "Sets the amount of GPUs to be reserved.")
        env.set("RELION_QSUB_EXTRA5", "Extra software")
        env.set("RELION_QSUB_EXTRA5_DEFAULT", "")
        env.set("RELION_QSUB_EXTRA5_HELP", "Name of extra spack modules to load.")

    def _check_wrappers(self):
        tools = ["blush", "classranker", "modelangelo"]
        if self.spec.satisfies("@5.1:"):
            tools.append("trace_amyloids")
        want = f'torch_home="{self._torch_home}"'
        for tool in tools:
            with open(join_path(self.prefix.bin, f"relion_python_{tool}")) as f:
                text = f.read()
            if want not in text:
                raise InstallError(f"relion_python_{tool}: wrong baked torch_home")
        # text is trace_amyloids here, the last entry on @5.1:
        if self.spec.satisfies("@5.1.0") and f'relion_home="{self.prefix}"' not in text:
            raise InstallError("relion_python_trace_amyloids points outside the prefix")

    def _check_weights(self):
        ckpt = join_path(self._torch_home, "hub", "checkpoints")
        sizes = dict(WEIGHT_SIZES)
        markers = list(WEIGHT_MARKERS)
        if self.spec.satisfies("@5.1:"):
            sizes.update(TRACER_SIZES)
            markers.extend(TRACER_MARKERS)
        problems = [m for m in markers if not os.path.isfile(join_path(ckpt, m))]
        for name, size in sizes.items():
            path = join_path(ckpt, name)
            if not os.path.isfile(path) or os.path.getsize(path) != size:
                problems.append(f"{name} (expected {size} bytes)")
        for root, _, files in os.walk(ckpt):
            problems.extend(
                join_path(root, f) for f in files if f.endswith((".gz", ".zip", ".partial"))
            )
        if problems:
            raise InstallError("Missing or bad weights: " + "; ".join(problems))
        # ModelAngelo downloads ESM-1b without any hash check
        digest = hashlib.sha256()
        with open(join_path(ckpt, f"{ESM}.pt"), "rb") as f:
            for block in iter(lambda: f.read(1 << 24), b""):
                digest.update(block)
        if digest.hexdigest() != ESM_SHA256:
            raise InstallError(f"{ESM}.pt has the wrong sha256")

    @run_after("install")
    def fetch_weights(self):
        self._check_wrappers()
        os.environ.pop("DISPLAY", None)
        scratch = join_path(self.stage.path, "weights_scratch")
        mkdirp(scratch)
        env = {
            "CUDA_VISIBLE_DEVICES": "",
            "MPLBACKEND": "Agg",
            "MPLCONFIGDIR": scratch,
            "NUMBA_CACHE_DIR": scratch,
        }
        steps = [
            ("relion_python_classranker",),
            ("relion_python_blush",),
            ("relion_python_blush", "-m", "amy-v1.0"),
            ("relion_python_blush", "-m", "amy-v1.0-lsd"),
        ]
        if self.spec.satisfies("@5.1:"):
            steps.append(("relion_python_trace_amyloids",))
        steps += [
            ("relion_python_modelangelo", "setup_weights", "--bundle-name", "nucleotides"),
            ("relion_python_modelangelo", "setup_weights", "--bundle-name", "nucleotides_no_seq"),
        ]
        for tool, *args in steps:
            wrapper = Executable(join_path(self.prefix.bin, tool))
            for attempt in range(3):
                try:
                    wrapper(*args, extra_env=env, timeout=FETCH_TIMEOUT)
                    break
                except ProcessError:
                    if attempt == 2:
                        raise
                    time.sleep(60)
        self._check_weights()
