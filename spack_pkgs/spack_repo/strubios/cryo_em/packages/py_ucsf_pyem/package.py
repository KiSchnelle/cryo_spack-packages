# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyUcsfPyem(PythonPackage):
    """UCSF pyem is a collection of Python modules and command-line
    utilities for electron microscopy of biological samples."""

    homepage = "https://github.com/asarnow/pyem"
    url = "https://github.com/asarnow/pyem/archive/refs/tags/v0.68.tar.gz"
    git = "https://github.com/asarnow/pyem.git"

    license("GPL-3.0-only", checked_by="A-N-Other")

    version(
        "0.68",
        sha256="105c2fc9860dd927b051ceb90287cf5a4a2664ffa8ae0f95464263570ee733c5",
        preferred=True,
    )

    depends_on("py-setuptools", type="build")

    depends_on("py-numba@0.41:")
    depends_on("py-numpy@1.26:1")
    depends_on("py-numexpr@2.8:")
    depends_on("py-scipy@1.2:")
    depends_on("py-matplotlib@2.2:")
    depends_on("py-seaborn@0.9:")
    depends_on("py-pandas@0.23.4:")
    depends_on("py-pathos@0.2.1:")
    depends_on("py-pyfftw@0.10:")
    depends_on("py-healpy@1.11:")
    depends_on("py-natsort@6.0:")
    depends_on("py-starfile@0.5.2:")
    depends_on("python@3.9:")
