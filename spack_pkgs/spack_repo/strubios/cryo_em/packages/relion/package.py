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
    url = "https://github.com/3dem/relion/archive/5.0.1.zip"
    maintainers("kischnelle")

    license("GPL-2.0-only")

    version(
        "5.0.1",
        sha256="3253230cd4b3d9633a5cac906937039b9971eb9430c3e2d838473777fb811f4c",
    )
    version(
        "3.1.4",
        sha256="c7b668879fa06bcb854f2f131970d9747320f75b45e335f937bc0d7088bd1c13",
    )
    version(
        "3.0.8",
        sha256="18cdd58e3a612d32413eb37e473fe8fbf06262d2ed72e42da20356f459260973",
    )

    variant("gui", default=True, description="build the gui")
    variant("double", default=True, description="double precision (cpu) code")
    variant("double-gpu", default=False, description="double precision gpu")
    variant("cuda", default=True, description="enable compute on gpu")
    variant("force-fftw", default=True, description="download fftw during install")
    variant(
        "mklfft",
        default=False,
        when="~force-fftw",
        description="Use MKL rather than FFTW for FFT",
    )
    variant("amdfftw", default=True, description="AMD optimized FFTW version")
    variant("altcpu", default=False, description="Use CPU acceleration", when="~cuda")

    depends_on("gcc", type="build")
    depends_on("mpi")
    depends_on("cuda", when="+cuda")

    depends_on("ctffind")
    depends_on("ghostscript")
    depends_on("fltk+xft", when="+gui")
    depends_on("libxft", when="+gui")
    depends_on("libx11", when="+gui")
    depends_on("fftw", when="~force-fftw~mklfft~amdfftw")
    depends_on("amdfftw", when="~force-fftw+amdfftw")
    depends_on("libtiff")
    depends_on("libpng")
    depends_on("xz")

    depends_on("tbb", when="+altcpu")
    depends_on("mkl", when="+mklfft")

    def cmake_args(self):
        args = [
            "-DCMAKE_C_FLAGS=-g",
            "-DCMAKE_CXX_FLAGS=-g",
            "-DGUI=%s" % ("ON" if "+gui" in self.spec else "OFF"),
            "-DDoublePrec_CPU=%s" % ("ON" if "+double" in self.spec else "OFF"),
            "-DDoublePrec_GPU=%s" % ("ON" if "+double-gpu" in self.spec else "OFF"),
            "-DFORCE_OWN_FFTW=%s" % ("ON" if "+force-fftw" in self.spec else "OFF"),
            "-DMKLFFT=%s" % ("ON" if "+mklfft" in self.spec else "OFF"),
            "-DAMDFFTW=%s" % ("ON" if "+amdfftw" in self.spec else "OFF"),
            "-DALTCPU=%s" % ("ON" if "+altcpu" in self.spec else "OFF"),
        ]

        if self.spec.satisfies("@5.0.1:"):
            args.extend(
                [
                    "-DPYTHON_EXE_PATH=/appl/spack/opt/spack/linux-rocky9-x86_64_v3/gcc-11.5.0/miniforge3-24.3.0-0-youy4hac6epwzeya7zqdpsfag7dhbczh/envs/relion-5.0/bin/python",
                    "-DTORCH_HOME_PATH=/appl/torch/relion_torch",
                ]
            )

        if "+cuda" in self.spec:
            carch = self.spec.variants["cuda_arch"].value[0]

            # relion+cuda requires selecting cuda_arch
            if carch == "none":
                raise ValueError("Must select a value for cuda_arch")
            else:
                args += ["-DCUDA=ON", "-DCUDA_ARCH=%s" % (carch)]

        return args

    def setup_run_environment(self, env):
        env.set("RELION_CTFFIND_EXECUTABLE", "ctffind")
        if self.spec.satisfies("@5.0.1:"):
            env.set("RELION_QSUB_TEMPLATE", "/appl/scripts/relion5.sh")
        if self.spec.satisfies("@3.1.4:"):
            env.set("RELION_QSUB_TEMPLATE", "/appl/scripts/relion31.sh")
        if self.spec.satisfies("@3.0.8:"):
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
