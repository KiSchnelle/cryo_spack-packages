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
    git = "https://github.com/czimaginginstitute/AreTomo2.git"

    license("BSD-3-Clause", checked_by="Markus92")

    version("main", branch="main", preferred=True)
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

    @property
    def build_directory(self):
        return self.stage.source_path

    def edit(self, spec, prefix):
        cuda = spec["cuda"]
        cuda_arch = spec.variants["cuda_arch"].value
        cuda_gencode = " ".join(self.cuda_flags(cuda_arch))
        stubs = cuda.prefix.lib64.stubs
        makefile = FileFilter("makefile11")

        # Set CUDA paths
        makefile.filter(r"^CUDAHOME = .*", f"CUDAHOME = {cuda.prefix}")

        # Use Spack's compiler wrappers instead of hardcoded g++
        makefile.filter(r"^CC = g\+\+", "CC = c++")

        # Use nvcc from CUDA toolkit
        makefile.filter(
            r"^NVCC = \$\(CUDAHOME\)/bin/nvcc",
            f"NVCC = {cuda.prefix}/bin/nvcc",
        )

        # Set CUDA arch flags
        makefile.filter(
            r"^CUFLAG = -Xptxas -dlcm=ca -O2 \\",
            f"CUFLAG = -Xptxas -dlcm=ca -O2 {cuda_gencode}",
        )
        # Remove the old multi-line gencode entries
        makefile.filter(r"^\s+-gencode arch=compute_\d+,code=sm_\d+.*", "")

        # Add CUDA stubs path for -lcuda (driver lib not in build container)
        makefile.filter(
            r"-L\$\(CUDALIB\) -L/usr/lib64",
            f"-L$(CUDALIB) -L{stubs} -L/usr/lib64",
        )

        # Fix hardcoded g++ in link line
        makefile.filter(r"@g\+\+ ", "@c++ ")

    def build(self, spec, prefix):
        make("-f", "makefile11", "exe")

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install("AreTomo2", prefix.bin)
