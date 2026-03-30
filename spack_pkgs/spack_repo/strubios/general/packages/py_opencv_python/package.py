# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack_repo.builtin.build_systems.python import PythonPackage


class PyOpencvPython(PythonPackage):
    """Wrapper package for OpenCV python bindings."""

    homepage = "https://github.com/opencv/opencv-python"
    pypi = "opencv-python/opencv-python-4.10.0.84.tar.gz"

    license("Apache-2.0")

    version(
        "4.10.0.84",
        sha256="72d234e4582e9658ffea8e9cae5b63d488ad06994ef12d81dc303b17472f3526",
    )

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("cmake@3.1:", type="build")
    depends_on("py-numpy@2:", type=("build", "run"), when="^python@3.9:")
    depends_on("py-numpy@:2", type=("build", "run"), when="^python@:3.8")
    depends_on("py-pip", type="build")
    depends_on("py-scikit-build", type="build")
