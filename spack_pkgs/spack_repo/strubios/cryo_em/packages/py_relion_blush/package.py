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

    license("MIT")

    version("main", branch="main")
    version(
        "2025.12.15",
        commit="ab48e6380e66b9aaf52362e86e060e9b9d8a40fd",
        preferred=True,
    )

    variant("cuda", default=True, description="Use CUDA")
    conflicts("~cuda", msg="This site builds GPU versions only")
    conflicts(
        "cuda_arch=none",
        when="+cuda",
        msg="Must specify cuda_arch, see https://developer.nvidia.com/cuda-gpus",
    )

    depends_on("py-setuptools", type="build")
    depends_on("python@3.5:", type=("build", "run"))

    # CUDA-aware deps — propagate cuda_arch
    for _arch in CudaPackage.cuda_arch_values:
        depends_on(
            f"py-torch@2.0.1:+cuda cuda_arch={_arch}",
            when=f"+cuda cuda_arch={_arch}",
            type=("build", "run"),
        )

    # No py-torchvision: all checkpoints and the live code import no torchvision.
    depends_on("py-numpy@1.24.4:", type=("build", "run"))
    depends_on("py-loguru", type=("build", "run"))
    depends_on("py-mrcfile", type=("build", "run"))
    depends_on("py-filelock", type=("build", "run"))
