# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack_repo.builtin.build_systems.python import PythonPackage


class PyYetAnotherImodWrapper(PythonPackage):
    """A simple API for automated tilt-series alignment using IMOD."""

    homepage = "https://github.com/teamtomo/yet-another-imod-wrapper"
    pypi = "yet_another_imod_wrapper/yet_another_imod_wrapper-0.1.2.tar.gz"

    license("BSD-3-Clause")

    version("0.1.2", sha256="47e61ab00adf584db6067acbf716029e4a7cafdfbca6c90b86646b879d3faea4")

    depends_on("py-hatchling", type="build")
    depends_on("py-hatch-vcs", type="build")

    with default_args(type=("build", "run")):
        depends_on("python@3.8:")
        depends_on("py-mrcfile@1.4:")
        depends_on("py-numpy")
        depends_on("py-packaging")
        depends_on("py-pandas")
        depends_on("py-rich")
        depends_on("py-starfile")
        depends_on("py-typer")
