# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack_repo.builtin.build_systems.python import PythonPackage


class PySkan(PythonPackage):
    """
    scikit-image's skeleton analysis module, extracted as a standalone package.
    """

    homepage = "https://github.com/jni/skan"
    pypi = "skan/skan-0.2.12.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.12.2",
        sha256="5c9e5c2dc169f2f4972b085f311a5961ba4351cafa57ff0c5aa418ac6f05a1d6",
    )

    depends_on("py-setuptools@45:", type="build")
    depends_on("py-setuptools-scm@6.2:", type="build")
    depends_on("py-wheel", type="build")
    depends_on("python@3.9:", type=("build", "run"))

    depends_on("py-imageio@2.10.1:", type=("build", "run"))
    depends_on("py-magicgui@0.7.3:", type=("build", "run"))
    depends_on("py-matplotlib@3.4:", type=("build", "run"))
    depends_on("py-networkx@2.7:", type=("build", "run"))
    depends_on("py-numba@0.53:", type=("build", "run"))
    depends_on("py-numpy@1.25:", type=("build", "run"))
    depends_on("py-pandas@2.0.2:", type=("build", "run"))
    depends_on("py-openpyxl@2.6:", type=("build", "run"))
    depends_on("py-scikit-image@0.17.1:", type=("build", "run"))
    depends_on("py-scipy@1.7:", type=("build", "run"))
    depends_on("py-toolz@0.10.0:", type=("build", "run"))
    depends_on("py-tqdm@4.57.0:", type=("build", "run"))
    depends_on("py-scikit-image+data", type=("build", "run"))
