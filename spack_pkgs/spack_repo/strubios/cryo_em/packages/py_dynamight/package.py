# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack_repo.builtin.build_systems.cuda import CudaPackage
from spack_repo.builtin.build_systems.python import PythonPackage


class PyDynamight(PythonPackage, CudaPackage):
    """DynaMight estimates continuous molecular motions and improves
    reconstructions from cryo-EM images."""

    homepage = "https://github.com/3dem/DynaMight"
    git = "https://github.com/3dem/DynaMight.git"

    license("BSD-3-Clause")

    version("main", branch="main")
    version(
        "2025.09.18",
        commit="358db04d5c2ec2997f3f17060a456293f0b02185",
        preferred=True,
    )

    variant("cuda", default=True, description="Use CUDA acceleration")
    conflicts("~cuda", msg="tsnecuda is imported at runtime and requires CUDA")
    conflicts(
        "cuda_arch=none",
        when="+cuda",
        msg="Must specify CUDA compute capabilities of your GPU, see "
        "https://developer.nvidia.com/cuda-gpus",
    )

    depends_on("py-hatchling", type="build")
    depends_on("py-hatch-vcs", type="build")
    depends_on("python@3.10:", type=("build", "run"))

    # CUDA-aware deps — propagate cuda_arch
    for _arch in CudaPackage.cuda_arch_values:
        # torch up to 2.13 otherwise forces py-protobuf@3.13 and py-tensorboard@2.11,
        # and every DynaMight command imports tensorboard.
        depends_on(
            f"py-torch@1.13:+cuda+custom-protobuf cuda_arch={_arch}",
            when=f"+cuda cuda_arch={_arch}",
            type=("build", "run"),
        )
        depends_on(
            f"tsne-cuda@3.0.1+cuda+python cuda_arch={_arch}",
            when=f"+cuda cuda_arch={_arch}",
            type=("build", "run"),
        )

    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-mrcfile", type=("build", "run"))
    depends_on("py-starfile", type=("build", "run"))
    depends_on("py-scikit-learn", type=("build", "run"))
    depends_on("py-umap-learn", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-napari@0.4.18:0.5", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
    depends_on("py-tensorboard", type=("build", "run"))
    depends_on("py-pyqt5", type=("build", "run"))
    depends_on("py-qtpy", type=("build", "run"))
    depends_on("py-magicgui", type=("build", "run"))
    depends_on("py-typer", type=("build", "run"))
    depends_on("py-biopython", type=("build", "run"))
