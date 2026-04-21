# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.builtin.build_systems.cuda import CudaPackage


class Relion(CMakePackage, CudaPackage):
    """RELION (for REgularised LIkelihood OptimisatioN, pronounce rely-on) is a
    stand-alone computer program that employs an empirical Bayesian approach to
    refinement of (multiple) 3D reconstructions or 2D class averages in
    electron cryo-microscopy (cryo-EM)."""

    homepage = "https://www2.mrc-lmb.cam.ac.uk/relion"
    git = "https://github.com/3dem/relion.git"
    url = "https://github.com/3dem/relion/archive/5.1.0.zip"
    maintainers("dacolombo", "Markus92")

    license("GPL-2.0-only")

    version(
        "5.1.0",
        sha256="714649163fbd7ee63cf9331d97751bd2e972703482349d8d7f2110387ef556d2",
    )
    version(
        "5.0.1",
        sha256="3253230cd4b3d9633a5cac906937039b9971eb9430c3e2d838473777fb811f4c",
    )
    version(
        "4.0.1",
        sha256="7e0d56fd4068c99f943dc309ae533131d33870392b53a7c7aae7f65774f667be",
    )
    version(
        "3.1.4",
        sha256="3bf3449bd2d71dc85d2cdbd342e772f5faf793d8fb3cda6414547cf34c98f34c",
    )
    version(
        "3.0.8",
        sha256="18cdd58e3a612d32413eb37e473fe8fbf06262d2ed72e42da20356f459260973",
    )

    variant("gui", default=True, description="build the gui")
    variant("double", default=True, description="double precision (cpu) code")
    variant("double-gpu", default=False, description="double precision gpu")

    conflicts(
        "+double-gpu", when="~cuda", msg="Double precision GPU code requires CUDA"
    )

    variant("own-fftw", default=True, description="Use bundled FFTW.")
    variant("amd-fftw", default=True, when="+own-fftw", description="Use AMD's FFTW.")
    variant("mklfft", default=False, description="Use MKL rather than FFTW for FFT")

    conflicts("+mklfft", when="+own-fftw", msg="Cannot use MKL FFT with bundled FFTW")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("fortran", type="build", when="+own-fftw")
    depends_on("mpi")
    depends_on("cmake@3:", type="build")
    depends_on("binutils@2.32:", type="build")

    depends_on("ctffind@4", type="run")
    depends_on("ghostscript", type="run", when="@4:")
    # use the +xft variant so the interface is not so horrible looking
    depends_on("fltk+xft", when="+gui")
    depends_on("libtiff")
    depends_on("libpng", when="@4:")
    depends_on("pbzip2", type="run", when="@4:")
    depends_on("xz", type="run", when="@4:")
    depends_on("zstd", type="run", when="@4:")

    depends_on("cuda@11:", when="+cuda")

    depends_on("mkl", when="+mklfft")

    # CUDA-aware deps — propagate cuda_arch
    for _arch in CudaPackage.cuda_arch_values:
        depends_on(
            f"py-relion@5.0.1:+cuda cuda_arch={_arch}",
            when=f"@5.0.1+cuda cuda_arch={_arch}",
            type=("build", "run"),
        )
        depends_on(
            f"py-relion@5.1.0: +cuda cuda_arch={_arch}",
            when=f"@5.1.0 +cuda cuda_arch={_arch}",
            type=("build", "run"),
        )
    depends_on(
        "py-relion@5.0.1 ~cuda",
        type=("build", "run"),
        when="@5.0.1 ~cuda",
    )
    depends_on(
        "py-relion@5.1.0: ~cuda",
        type=("build", "run"),
        when="@5.1.0: ~cuda",
    )

    def cmake_args(self):
        args = [
            "-DGUI=%s" % ("+gui" in self.spec),
            "-DDoublePrec_CPU=%s" % ("+double" in self.spec),
            "-DDoublePrec_GPU=%s" % ("+double-gpu" in self.spec),
            "-DFORCE_OWN_FFTW=%s" % ("+own-fftw" in self.spec),
            "-DAMDFFTW=%s" % ("+amd-fftw" in self.spec),
            "-DMKLFFT=%s" % ("+mklfft" in self.spec),
        ]
        if self.spec.satisfies("+gui"):
            incs = [
                f"-I{self.spec[lib].prefix.include}" for lib in ["libx11", "xproto"]
            ]
            args += ["-DCMAKE_CXX_FLAGS=" + " ".join(incs)]

        if "+cuda" in self.spec:
            carch = self.spec.variants["cuda_arch"].value[0]

            # relion+cuda requires selecting cuda_arch
            if carch == "none":
                raise ValueError("Must select a value for cuda_arch")
            else:
                args += ["-DCUDA=ON", "-DCudaTexture=ON", "-DCUDA_ARCH=%s" % (carch)]

        if self.spec.satisfies("@5: ~cuda"):
            # Relion 5 defaults to CUDA=ON so it has to be explicitly disabled.
            args.append("-DCUDA=OFF")

        if self.spec.satisfies("@5:"):
            args.append(f"-DPYTHON_EXE_PATH={self.spec['python'].command.path}")
            args.append("-DFETCH_WEIGHTS=OFF")

        return args

    def setup_run_environment(self, env):
        env.set("RELION_CTFFIND_EXECUTABLE", self.spec["ctffind"].prefix.bin.ctffind)
        if self.spec.satisfies("@5:"):
            env.set("RELION_QSUB_TEMPLATE", "/appl/scripts/relion5.sh")
        elif self.spec.satisfies("@3.1"):
            env.set("RELION_QSUB_TEMPLATE", "/appl/scripts/relion31.sh")
        elif self.spec.satisfies("@3.0"):
            env.set("RELION_QSUB_TEMPLATE", "/appl/scripts/relion30.sh")
        env.set("RELION_QUEUE_USE", "yes")
        env.set("RELION_QUEUE_NAME", "p.cryo")
        env.set("RELION_QSUB_COMMAND", "sbatch")
        env.set("RELION_SCRATCH_DIR", "/scratch/${SLURM_JOB_ID}/")
        env.set("RELION_QSUB_EXTRA_COUNT", "5")
        env.set("RELION_QSUB_EXTRA1", "Memory")
        env.set("RELION_QSUB_EXTRA1_DEFAULT", "50")
        env.set(
            "RELION_QSUB_EXTRA1_HELP", "Sets the reserved about of RAM memory in GB."
        )
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
