# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyTopaz3dem(PythonPackage):
    """topaz: Pipeline for particle picking in cryo-electron microscopy images using
    convolutional neural networks trained from positive and unlabeled examples. Also
    featuring micrograph and tomogram denoising with DNNs."""

    homepage = "https://github.com/3dem/topaz"
    git = "https://github.com/3dem/topaz.git"

    license("GPL-3.0-or-later")

    version("2026.01.08", commit="c8dd487cbf9d27139d0d430068033fb90dd9a393")

    # RELION's default picking path needs pkg_resources, which setuptools 82 removed.
    depends_on("py-setuptools@:81", type=("build", "run"))
    depends_on("python@3.8:", type=("build", "run"))

    # GPU or CPU is decided by how py-torch is built
    depends_on("py-torch@2.0.1:", type=("build", "run"))

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
