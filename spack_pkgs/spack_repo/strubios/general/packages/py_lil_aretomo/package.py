# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack_repo.builtin.build_systems.python import PythonPackage


class PyLilAretomo(PythonPackage):
    """A lightweight Python API for AreTomo."""

    homepage = "https://github.com/teamtomo/lil-aretomo"
    pypi = "lil_aretomo/lil_aretomo-0.1.1.tar.gz"

    license("BSD-3-Clause")

    version("0.1.1", sha256="02ccb0efbf2c06304570117f142e78331bfffdde46864e22de11c6cd7f30f178")

    # No aretomo dependency: builtin's needs a manual download and CUDA 11.8 or older,
    # which cannot share a solve with RELION's cuda@12:. Builtin also has no runtime
    # Python dependencies, so a subclass would fit neither way.
    depends_on("py-setuptools@42:", type="build")
    depends_on("py-setuptools-scm@3.4: +toml", type="build")

    with default_args(type=("build", "run")):
        depends_on("python@3.8:")
        depends_on("py-numpy")
        depends_on("py-pandas")
        depends_on("py-mrcfile@1.4:")
        depends_on("py-typer")
        depends_on("py-rich")
