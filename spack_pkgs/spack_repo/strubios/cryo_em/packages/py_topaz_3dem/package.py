# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack_repo.builtin.build_systems.cuda import CudaPackage
from spack_repo.builtin.build_systems.python import PythonPackage


class PyTopaz3dem(PythonPackage, CudaPackage):
    """topaz: Pipeline for particle picking in cryo-electron microscopy images using
    convolutional neural networks trained from positive and unlabeled examples. Also
    featuring micrograph and tomogram denoising with DNNs."""

    homepage = "https://github.com/3dem/topaz"
    git = "https://github.com/3dem/topaz.git"

    license("GPL-3.0-or-later")

    version("master", branch="master")
    version(
        "2026.01.08",
        commit="c8dd487cbf9d27139d0d430068033fb90dd9a393",
        preferred=True,
    )

    variant("cuda", default=True, description="Use CUDA")
    conflicts("~cuda", msg="This site builds GPU versions only")
    conflicts(
        "cuda_arch=none",
        when="+cuda",
        msg="Must specify cuda_arch, see https://developer.nvidia.com/cuda-gpus",
    )

    # RELION's default picking path needs pkg_resources, which setuptools 82 removed.
    depends_on("py-setuptools@:81", type=("build", "run"))
    depends_on("python@3.8:", type=("build", "run"))

    # CUDA-aware deps — propagate cuda_arch
    for _arch in CudaPackage.cuda_arch_values:
        depends_on(
            f"py-torch@2.0.1:+cuda cuda_arch={_arch}",
            when=f"+cuda cuda_arch={_arch}",
            type=("build", "run"),
        )

    depends_on("py-numpy@1.11:", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-scikit-learn@0.19.0:", type=("build", "run"))
    depends_on("py-scipy@0.17.0:", type=("build", "run"))
    depends_on("py-pillow@6.2.0:", type=("build", "run"))
    depends_on("py-future", type=("build", "run"))

    def patch(self):
        filter_file(
            r"torch\.load\((name|path|args\.model)\)",
            r"torch.load(\1, weights_only=False)",
            "topaz/denoise.py",
            "topaz/commands/denoise3d.py",
            "topaz/commands/train.py",
        )
        filter_file(
            r"pd\.concat\((groups_train|groups_test), 0\)",
            r"pd.concat(\1, axis=0)",
            "topaz/commands/train_test_split.py",
        )
