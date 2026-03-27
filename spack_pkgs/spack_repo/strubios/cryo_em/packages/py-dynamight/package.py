# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack_repo.builtin.build_systems.cuda import CudaPackage
from spack_repo.builtin.build_systems.python import PythonPackage


class PyDynaMight(PythonPackage, CudaPackage):
    """ModelAngelo is an automatic atomic model building program for cryo-EM maps."""

    homepage = "https://github.com/3dem/DynaMight"
    git = "https://github.com/3dem/DynaMight.git"

    license("BSD")

    version("main", branch="main", preferred=True)

    depends_on("py-hatchling", type="build")
    depends_on("py-hatch-vcs", type="build")
    depends_on("python@3.8:", type=("build", "run"))

    # CUDA-aware deps — propagate cuda_arch
    for _arch in CudaPackage.cuda_arch_values:
        depends_on(
            f"py-torch+cuda cuda_arch={_arch}",
            when=f"+cuda cuda_arch={_arch}",
            type=("build", "run"),
        )
        depends_on(
            f"tsne-cuda+cuda+python cuda_arch={_arch}",
            when=f"+cuda cuda_arch={_arch}",
            type=("build", "run"),
        )
    depends_on("py-torch~cuda", when="~cuda", type=("build", "run"))
    depends_on("tsne-cuda~cuda+python", when="~cuda", type=("build", "run"))

    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-mrcfile", type=("build", "run"))
    depends_on("py-starfile", type=("build", "run"))
    depends_on("py-scikit-learn", type=("build", "run"))
    depends_on("py-umap-learn", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-napari", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
    depends_on("py-tensorboard", type=("build", "run"))
    depends_on("py-pyqt5", type=("build", "run"))
    depends_on("py-typer", type=("build", "run"))
    depends_on("py-biopython", type=("build", "run"))
