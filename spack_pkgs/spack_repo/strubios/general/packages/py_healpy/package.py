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

    # Builtin stops at 1.14.0 and forces healpix-cxx, fortran and py-six.
    version("1.19.0", sha256="28e839cb885a23d36c77fc3423a3cb9271a07fda94085bd12fc329f941130ec5")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("python@3.10:", type=("build", "run"))

    with default_args(type="build"):
        depends_on("py-setuptools@77:")
        depends_on("py-setuptools-scm@8:")
        depends_on("py-cython")
        depends_on("gmake")
        depends_on("pkgconfig")

    with default_args(type=("build", "run")):
        depends_on("py-numpy@1.19:")
        depends_on("py-scipy")
        depends_on("py-astropy")
        depends_on("py-matplotlib")

    depends_on("cfitsio@4.5:")

    def patch(self):
        with open("setup.cfg", "a") as f:
            f.write(f"\n[build_clib]\nbuild_clib = {self.prefix.lib.healpy_vendored}\n")

    def setup_build_environment(self, env):
        # patch() installs the bundled healpix_cxx and libsharp below build_clib. RPATH every
        # link there: the extensions and libhealpix_cxx, which needs libsharp. setuptools and
        # the bundled configure scripts both read LDFLAGS.
        env.append_flags("LDFLAGS", f"-Wl,-rpath,{self.prefix.lib.healpy_vendored.lib}")
