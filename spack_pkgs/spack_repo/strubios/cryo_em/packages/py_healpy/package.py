# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack_repo.builtin.build_systems.python import PythonPackage


class PyHealpy(PythonPackage):
    """healpy is a Python package to handle pixelated data on the sphere."""

    homepage = "https://healpy.readthedocs.io/"
    pypi = "healpy/healpy-1.19.0.tar.gz"

    license("GPL-2.0-only")

    version(
        "1.19.0",
        sha256="28e839cb885a23d36c77fc3423a3cb9271a07fda94085bd12fc329f941130ec5",
    )
    version(
        "1.14.0",
        sha256="2720b5f96c314bdfdd20b6ffc0643ac8091faefcf8fd20a4083cedff85a66c5e",
    )

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    # Build deps
    depends_on("py-setuptools@3.2:72", type="build", when="@:1.14")
    depends_on("py-setuptools@3.2:", type="build", when="@1.15:")
    depends_on("py-cython", type="build", when="@1.15:")
    depends_on("py-pkgconfig", type="build")

    # Runtime deps
    depends_on("py-numpy@1.13:1", type=("build", "run"), when="@:1.14")
    depends_on("py-numpy@1.13:", type=("build", "run"), when="@1.15:")
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-astropy", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-six", type=("build", "run"), when="@:1.14")

    depends_on("cfitsio")
    depends_on("healpix-cxx", when="@:1.14")

    # 1.14.0 uses pre-generated Cython incompatible with Python 3.11+
    depends_on("python@:3.10", when="@:1.14")

    # Older versions need fortran for bundled libsharp
    depends_on("fortran", type="build", when="@:1.14")

    def patch(self):
        if self.spec.satisfies("@:1.14"):
            # Fix cfitsio version check for 3-part versions (>= 4.x)
            fitshandle = FileFilter("healpixsubmodule/src/cxx/cxxsupport/fitshandle.cc")
            fitshandle.filter(
                r"int v_header\s*=\s*nearest<int>\(1000\.\*CFITSIO_VERSION\)",
                "int v_header  = CFITSIO_MAJOR*1000 + CFITSIO_MINOR*100",
            )
