# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack_repo.builtin.build_systems.python import PythonPackage


class PyLibigl(PythonPackage):
    """
    libigl is a simple C++ geometry processing library. This package provides Python bindings for libigl,
    allowing users to access its functionality from Python.
    """

    homepage = "https://github.com/libigl/libigl-python-bindings"
    pypi = "libigl/libigl-2.6.2.tar.gz"

    license("BSD-3-Clause")

    version(
        "2.6.2",
        sha256="5da0c5d889a66e3e90eefe6b7f0e7239ade6ac94353585f1b5b086bb1372599e",
    )

    depends_on("py-nanobind@1.3.2:", type="build")
    depends_on("py-numpy@2.0.0:", type=("build"), when="^python@3.9:")
    depends_on("py-numpy@:1", type=("build"), when="^python@3.8")
    depends_on("py-packaging", type="build")
    depends_on("py-scikit-build-core@0.10:+pyproject", type="build")
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-typing-extensions", type="build")
    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-numpy", type=("run"))
