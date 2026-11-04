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
    url = "https://github.com/3dem/relion/archive/5.1.1.zip"

    license("GPL-2.0-only", checked_by="Markus92")

    version("5.1.1", sha256="1bf75dcf287fb6d591cd4194c0d0cddf98590ae36c54fafbbcb7aa4daef85ec6")
    version("5.1.0", sha256="714649163fbd7ee63cf9331d97751bd2e972703482349d8d7f2110387ef556d2")
    version("5.0.1", sha256="3253230cd4b3d9633a5cac906937039b9971eb9430c3e2d838473777fb811f4c")

    variant("cuda", default=True, description="Build with CUDA")
    conflicts("~cuda", msg="This site builds GPU versions only")
    conflicts("cuda_arch=none", when="+cuda",
              msg="Must specify cuda_arch, see https://developer.nvidia.com/cuda-gpus")

    # Deliberate deviations from upstream environment.yml: python 3.10 and setuptools 59.5.0
    # are not used, torch is newer than 2.7.1, scikit-learn is newer than 1.3.0.
    depends_on("python@3.11", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-wheel", type="build")
    depends_on("py-setuptools-scm@6.3:", type="build")

    # Exact pins so a rebuild does not drift with upstream branches.
    for _arch in CudaPackage.cuda_arch_values:
        with default_args(when=f"+cuda cuda_arch={_arch}", type=("build", "run")):
            depends_on(f"py-torch@2.7.1:+cuda cuda_arch={_arch}")
            depends_on(f"tsne-cuda@3.0.1+cuda+python cuda_arch={_arch}")
            depends_on(f"py-relion-classranker@2025.09.16 +cuda cuda_arch={_arch}")
            depends_on(f"py-relion-blush@2025.12.15 +cuda cuda_arch={_arch}")
            depends_on(f"py-dynamight@2025.09.18 +cuda cuda_arch={_arch}")
            depends_on(f"py-topaz-3dem@2026.01.08 +cuda cuda_arch={_arch}")
            # ~weights: relion fetches the only copy into its own prefix.
            depends_on(f"py-model-angelo ~weights +cuda cuda_arch={_arch}")

    with default_args(type=("build", "run")):
        depends_on("py-tqdm@4.65.0")
        depends_on("py-mrcfile@1.4.3")
        depends_on("py-starfile@0.5.6:")
        depends_on("py-loguru@0.7.0")
        depends_on("py-scikit-learn@1.5:1.7")
        depends_on("py-umap-learn@0.5.3")
        depends_on("py-matplotlib@3.7.2")
        depends_on("py-morphosamplers@0.0.13")
        depends_on("py-pydantic@1.10.18")
        depends_on("py-napari+all@0.4.18")
        depends_on("py-napari-threedee@0.0.28")
        depends_on("py-psygnal@0.11.1")
        depends_on("py-pyqt5@5.15.9")
        depends_on("py-typer@0.9.0")
        depends_on("py-click@:8.1.9")
        depends_on("py-biopython@1.81")
        depends_on("py-fastcluster@1.2.6")
        depends_on("py-seaborn@0.12.2")
        depends_on("py-dill@0.3.7")
        depends_on("py-numpy@1.26")
        depends_on("py-scipy@1.11.2")
        depends_on("py-skan@0.12.2", when="@5.1:")
        depends_on("py-opencv-python@4.10.0.84", when="@5.1:")
        depends_on("py-scikit-image", when="@5.1:")
        depends_on("py-qtpy")

        # relion pyproject.toml deps
        depends_on("py-pandas@2.1.1:2~performance")  # +performance would force numpy 1.25
        depends_on("py-mdocfile@0.0.8")              # 0.1+ needs pydantic 2
        depends_on("py-yet-another-imod-wrapper@0.0.9:")
        for _d in ("py-rich", "py-einops", "py-lil-aretomo", "py-makefun",
                   "py-lru-dict", "py-superqt", "py-magicgui"):
            depends_on(_d)

    # Set version so setuptools won't complain about not being able to determine it
    def setup_build_environment(self, env):
        env.set("SETUPTOOLS_SCM_PRETEND_VERSION", str(self.spec.version))
