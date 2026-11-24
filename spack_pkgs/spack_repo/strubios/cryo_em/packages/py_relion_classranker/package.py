# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyRelionClassranker(PythonPackage):
    """The class ranker is part of the cryogenic electron microscopy (cryo-EM)
    dataset processing pipeline in RELION. It is used to automatically
    select suitable particles (EM images) assigned to 2D class averages
    for further downstream processing."""

    homepage = "https://github.com/3dem/relion-classranker"
    git = "https://github.com/3dem/relion-classranker.git"

    license("GPL-3.0-only")

    version("2025.09.16", commit="352adf8b690ba56e9f4073cfee41c8fcad3dfb81")

    depends_on("py-setuptools", type="build")
    depends_on("python@3.5:", type=("build", "run"))

    # GPU or CPU is decided by how py-torch is built
    depends_on("py-torch@2.0.1:", type=("build", "run"))

    depends_on("py-numpy@1.24.4:", type=("build", "run"))
