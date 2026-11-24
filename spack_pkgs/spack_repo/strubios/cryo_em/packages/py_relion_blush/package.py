# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyRelionBlush(PythonPackage):
    """Blush Refinement for Relion."""

    homepage = "https://github.com/3dem/relion-blush"
    git = "https://github.com/3dem/relion-blush.git"

    license("MIT")

    version("2025.12.15", commit="ab48e6380e66b9aaf52362e86e060e9b9d8a40fd")

    depends_on("py-setuptools", type="build")
    depends_on("python@3.5:", type=("build", "run"))

    # GPU or CPU is decided by how py-torch is built
    depends_on("py-torch@2.0.1:", type=("build", "run"))

    # No py-torchvision: all checkpoints and the live code import no torchvision.
    depends_on("py-numpy@1.24.4:", type=("build", "run"))
    depends_on("py-loguru", type=("build", "run"))
    depends_on("py-mrcfile", type=("build", "run"))
    depends_on("py-filelock", type=("build", "run"))
