# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack_repo.builtin.build_systems.cuda import CudaPackage
from spack_repo.builtin.build_systems.python import PythonPackage


class PyRelionBlush(PythonPackage, CudaPackage):
    """Blush Refinement for Relion."""

    homepage = "https://github.com/3dem/relion-blush"
    git = "https://github.com/3dem/relion-blush.git"

    license("MIT", checked_by="github_user1")

    version("main", branch="main", preferred=True)

    depends_on("py-setuptools", type="build")
    depends_on("python@3.5:", type=("build", "run"))

    # CUDA-aware deps — propagate cuda_arch
    for _arch in CudaPackage.cuda_arch_values:
        depends_on(
            f"py-torch@2.0.1:+cuda cuda_arch={_arch}",
            when=f"+cuda cuda_arch={_arch}",
            type=("build", "run"),
        )
    depends_on("py-torch@2.0.1:~cuda", when="~cuda", type=("build", "run"))

    depends_on("py-torchvision@0.15.2:", type=("build", "run"))
    depends_on("py-numpy@1.24.4:", type=("build", "run"))
