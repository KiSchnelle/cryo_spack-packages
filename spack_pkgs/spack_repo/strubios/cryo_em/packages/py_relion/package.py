# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack_repo.builtin.build_systems.cuda import CudaPackage
from spack_repo.builtin.build_systems.python import PythonPackage


class PyRelion(PythonPackage, CudaPackage):
    """This is a helper package for relion, not to be used by end-users.

    relion (for REgularised LIkelihood OptimisatioN, pronounce rely-on) is a
    software package that employs an empirical Bayesian approach for electron
    cryo-microscopy (cryo-EM) structure determination.
    """

    homepage = "https://relion.readthedocs.io/en/latest/"
    git = "https://github.com/3dem/relion.git"
    url = "https://github.com/3dem/relion/archive/5.1.0.zip"

    license("GPL-2", checked_by="Markus92")

    version(
        "5.1.0",
        sha256="714649163fbd7ee63cf9331d97751bd2e972703482349d8d7f2110387ef556d2",
    )
    version(
        "5.0.1",
        sha256="3253230cd4b3d9633a5cac906937039b9971eb9430c3e2d838473777fb811f4c",
    )

    variant("cuda", default=True, description="Build with CUDA (recommended)")

    depends_on("python@3.10:", type=("build", "run"))
    depends_on("py-setuptools@59.5.0", type="build")
    depends_on("py-wheel", type="build")
    depends_on("py-setuptools-scm@6.3:", type="build")

    # CUDA-aware deps — propagate cuda_arch
    for _arch in CudaPackage.cuda_arch_values:
        depends_on(
            f"py-torch@2.0.1+cuda cuda_arch={_arch}",
            when=f"@5.0.1 +cuda cuda_arch={_arch}",
            type=("build", "run"),
        )
        depends_on(
            f"py-torch@2.7.1+cuda cuda_arch={_arch}",
            when=f"@5.1.0 +cuda cuda_arch={_arch}",
            type=("build", "run"),
        )
        depends_on(
            f"tsne-cuda@3.0.1+cuda+python cuda_arch={_arch}",
            when=f"+cuda cuda_arch={_arch}",
            type=("build", "run"),
        )
        depends_on(
            f"py-relion-classranker+cuda cuda_arch={_arch}",
            when=f"+cuda cuda_arch={_arch}",
            type=("build", "run"),
        )
        depends_on(
            f"py-relion-blush+cuda cuda_arch={_arch}",
            when=f"+cuda cuda_arch={_arch}",
            type=("build", "run"),
        )
        depends_on(
            f"py-dynamight+cuda cuda_arch={_arch}",
            when=f"+cuda cuda_arch={_arch}",
            type=("build", "run"),
        )
        depends_on(
            f"py-topaz-3dem+cuda cuda_arch={_arch}",
            when=f"+cuda cuda_arch={_arch}",
            type=("build", "run"),
        )
        depends_on(
            f"py-model-angelo+cuda cuda_arch={_arch}",
            when=f"+cuda cuda_arch={_arch}",
            type=("build", "run"),
        )

    depends_on("py-torch@2.0.1~cuda", when="@5.0.1 ~cuda", type=("build", "run"))
    depends_on("py-torch@2.7.1~cuda", when="@5.1.0 ~cuda", type=("build", "run"))
    depends_on("tsne-cuda~cuda+python@3.0.1", when="~cuda", type=("build", "run"))
    depends_on("py-relion-classranker~cuda", when="~cuda", type=("build", "run"))
    depends_on("py-relion-blush~cuda", when="~cuda", type=("build", "run"))
    depends_on("py-dynamight~cuda", when="~cuda", type=("build", "run"))
    depends_on("py-topaz-3dem~cuda", when="~cuda", type=("build", "run"))
    depends_on("py-model-angelo~cuda", when="~cuda", type=("build", "run"))

    depends_on("py-morphosamplers", type=("build", "run"))
    depends_on("py-torchvision@0.15.2", type=("build", "run"), when="@5.0.1")
    depends_on("py-tqdm@4.65.0", type=("build", "run"))
    depends_on("py-mrcfile@1.4.3", type=("build", "run"))
    depends_on("py-starfile@0.5.6:", type=("build", "run"))
    depends_on("py-loguru@0.7.0", type=("build", "run"))
    depends_on("py-scikit-learn@1.3.0", type=("build", "run"))
    depends_on("py-umap-learn@0.5.3", type=("build", "run"))
    depends_on("py-matplotlib@3.7.2", type=("build", "run"))
    depends_on("py-pydantic@1.10.18", type=("build", "run"))
    depends_on("py-napari+all@0.4.18", type=("build", "run"))
    depends_on("py-pyqt5@5.15.9", type=("build", "run"))
    depends_on("py-typer@0.9.0", type=("build", "run"))
    depends_on("py-click@:8.2.0", type=("build", "run"))
    depends_on("py-biopython@1.81", type=("build", "run"))
    depends_on("py-fastcluster@1.2.6", type=("build", "run"))
    depends_on("py-seaborn@0.12.2", type=("build", "run"))
    depends_on("py-dill@0.3.7", type=("build", "run"))
    depends_on("py-numpy@1.26.1", type=("build", "run"))
    depends_on("py-scipy@1.11.2", type=("build", "run"))
    depends_on("py-skan@0.2.12", type=("build", "run"), when="@5.1.0")
    depends_on("py-opencv-python@4.10.0.84", type=("build", "run"), when="@5.1.0")

    # relion pyproject.toml deps
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-mdocfile", type=("build", "run"))
    depends_on("py-rich", type=("build", "run"))
    depends_on("py-einops", type=("build", "run"))
    depends_on("py-lil-aretomo", type=("build", "run"))
    depends_on("py-makefun", type=("build", "run"))
    depends_on("py-lru-dict", type=("build", "run"))
    depends_on("py-superqt", type=("build", "run"))

    # relion pyproject.toml deps[vis]
    depends_on("py-napari-threedee", type=("build", "run"))
    depends_on("py-qtpy", type=("build", "run"))
    depends_on("py-psygnal", type=("build", "run"))

    # Set version so setuptools won't complain about not being able to determine it
    def setup_build_environment(self, env):
        env.set("SETUPTOOLS_SCM_PRETEND_VERSION", str(self.spec.version))
