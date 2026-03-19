# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *
from spack_repo.builtin.build_systems.cuda import CudaPackage
from spack_repo.builtin.build_systems.makefile import MakefilePackage


class Aretomo2(MakefilePackage, CudaPackage):
    """AreTomo2 is a multi-GPU accelerated software package that fully automates
    motion-corrected marker-free tomographic alignment and reconstruction, now
    includes robust GPU-accelerated CTF (Contrast Transfer Function) estimation
    in a single package."""

    homepage = "https://github.com/czimaginginstitute/AreTomo2"
    url = (
        "https://github.com/czimaginginstitute/AreTomo2/archive/refs/tags/v1.1.2.tar.gz"
    )

    maintainers("Markus92")

    license("BSD-3-Clause", checked_by="Markus92")

    version(
        "1.1.2",
        sha256="4cbb4d25d28778041d80ef2c598519b17b9a40aa84e1e99daf48ad5a90d946b4",
    )

    depends_on("c", type="build")  # Not really, but CUDA does
    depends_on("cxx", type="build")
    depends_on("gmake", type="build")
    depends_on("cuda@11:", type=("build", "link"))

    conflicts("~cuda")
    conflicts(
        "cuda_arch=none", when="+cuda", msg="A value for cuda_arch must be specified."
    )

    build_targets = ["exe"]

    patch("cuda_arch_makefile.patch")

    def setup_build_environment(self, env):
        env.prepend_path("LIBRARY_PATH", self.spec["cuda"].prefix.lib64.stub)

    def edit(self, spec, prefix):
        cuda = spec["cuda"]
        cuda_arch = spec.variants["cuda_arch"].value
        cuda_gencode = " ".join(self.cuda_flags(cuda_arch))
        stubs = cuda.prefix.lib64.stubs

        makefile = FileFilter("makefile")

        # Set CUDA paths
        makefile.filter(
            r"CUDAHOME = .*",
            f"CUDAHOME = {cuda.prefix}",
        )

        # Use Spack's compiler wrappers instead of hardcoded g++
        makefile.filter(
            r"^CC = g\+\+ -std=c\+\+11",
            "CC = c++ -std=c++11",
        )

        # Use nvcc from CUDA toolkit
        makefile.filter(
            r"NVCC = \$\(CUDAHOME\)/bin/nvcc -std=c\+\+11",
            f"NVCC = {cuda.prefix}/bin/nvcc -std=c++11",
        )

        # Set CUDA arch flags
        makefile.filter(
            r"CUFLAG = -Xptxas -dlcm=ca -O2 \\.*",
            f"CUFLAG = -Xptxas -dlcm=ca -O2 {cuda_gencode}",
        )
        # Remove the old multi-line gencode entries
        makefile.filter(r"\s*-gencode arch=compute_\d+,code=sm_\d+.*", "")

        # Add CUDA stubs path for -lcuda (driver lib not in build container)
        makefile.filter("-lcuda", f"-L{stubs} -lcuda")

        # Fix hardcoded g++ in link line
        makefile.filter(
            r"\t@g\+\+ -g -pthread -m64 \$\(OBJS\)",
            "\t@c++ -g -pthread -m64 $(OBJS)",
        )

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install("AreTomo2", prefix.bin)
