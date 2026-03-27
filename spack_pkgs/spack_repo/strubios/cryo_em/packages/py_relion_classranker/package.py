# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack_repo.builtin.build_systems.cuda import CudaPackage
from spack_repo.builtin.build_systems.python import PythonPackage


class PyRelionClassranker(PythonPackage, CudaPackage):
    """The class ranker is part of the cryogenic electron microscopy (cryo-EM)
    dataset processing pipeline in RELION. It is used to automatically
    select suitable particles (EM images) assigned to 2D class averages
    for further downstream processing."""

    homepage = "https://github.com/3dem/relion-classranker"
    git = "https://github.com/3dem/relion-classranker.git"

    license("GPL-3.0-only", checked_by="snehring")

    version("main", branch="main", preferred=True)

    depends_on("py-setuptools", type="build")
    depends_on("python@3.5:", type=("build", "run"))

    # CUDA-aware deps — propagate cuda_arch
    for _arch in CudaPackage.cuda_arch_values:
        depends_on(
            f"py-torch+cuda cuda_arch={_arch}",
            when=f"+cuda cuda_arch={_arch}",
            type=("build", "run"),
        )
    depends_on("py-torch~cuda", when="~cuda", type=("build", "run"))

    depends_on("py-torchvision@0.15.2:", type=("build", "run"))
    depends_on("py-numpy@1.24.4:", type=("build", "run"))
