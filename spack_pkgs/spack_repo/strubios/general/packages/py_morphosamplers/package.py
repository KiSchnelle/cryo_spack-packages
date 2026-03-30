# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack_repo.builtin.build_systems.python import PythonPackage


class PyMorphosamplers(PythonPackage):
    """
    MorphoSamplers is a Python library for sampling-based methods in cryo-EM image processing,
    including particle picking, 2D classification, and 3D reconstruction.
    """

    homepage = "https://github.com/morphometrics/morphosamplers"
    pypi = "morphosamplers/morphosamplers-0.0.13.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.0.13",
        sha256="7a59e87932d04b366e62ce9105390598a6b3bba6675d9adf2450b32bd7057f22",
    )

    variant("segment", default=False, description="Enable segmentation support")

    depends_on("py-setuptools", type="build")
    depends_on("python@3.8:", type=("build", "run"))

    depends_on("py-einops", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-psygnal", type=("build", "run"))
    depends_on("py-pydantic", type=("build", "run"))
    depends_on("py-pydantic-compat", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-typing-extensions", type=("build", "run"))

    depends_on("py-skan", type=("build", "run"), when="+segment")
    depends_on("py-scikit-image", type=("build", "run"), when="+segment")
    depends_on("py-dijkstra3d", type=("build", "run"), when="+segment")
    depends_on("py-pandas", type=("build", "run"), when="+segment")
