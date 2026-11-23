# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyOpencvPython(PythonPackage):
    """Wrapper package for OpenCV python bindings."""

    homepage = "https://github.com/opencv/opencv-python"
    pypi = "opencv-python/opencv-python-4.10.0.84.tar.gz"

    license("Apache-2.0")

    # RELION 5.1 pins 4.10.0.84 with numpy 1.26; builtin only has 4.12.0.88.
    version(
        "4.10.0.84",
        sha256="72d234e4582e9658ffea8e9cae5b63d488ad06994ef12d81dc303b17472f3526",
    )

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("cmake@3.5.1:", type="build")
    depends_on("py-pip", type="build")
    depends_on("py-scikit-build@0.14:", type="build")

    # Runtime numpy requirements from setup.py of 4.10. Builtin requires numpy 2 for every
    # version on Python 3.9+, which 4.10 does not need, and RELION uses numpy 1.26.
    with default_args(type=("build", "run")):
        depends_on("py-numpy@1.21.2:")
        depends_on("py-numpy@1.23.5:", when="^python@3.11:")
        depends_on("py-numpy@1.26:", when="^python@3.12:")
