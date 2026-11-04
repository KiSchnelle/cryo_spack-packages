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

    depends_on("cmake@3.5.1:", type="build")
    depends_on("py-pip", type="build")
    depends_on("py-scikit-build@0.14:", type="build")
    # Builtin forces numpy 2 on Python 3.9+; RELION pins numpy 1.26 with this opencv.
    depends_on("py-numpy@1.21.2:", type=("build", "run"))
    depends_on("py-numpy@1.23.5:", type=("build", "run"), when="^python@3.11:")
    depends_on("py-numpy@1.26:", type=("build", "run"), when="^python@3.12:")

    def setup_build_environment(self, env):
        env.set(
            "SKBUILD_CONFIGURE_OPTIONS",
            "-DOPENCV_FORCE_3RDPARTY_BUILD=ON -DWITH_GTK=OFF -DWITH_FFMPEG=OFF "
            "-DWITH_GSTREAMER=OFF -DWITH_V4L=OFF -DWITH_1394=OFF -DWITH_OPENCL=OFF "
            "-DWITH_LAPACK=OFF -DWITH_VA=OFF -DWITH_VA_INTEL=OFF -DWITH_IPP=OFF -DWITH_ADE=OFF",
        )
