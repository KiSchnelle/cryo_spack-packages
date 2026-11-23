# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyPyfftw(PythonPackage):
    """A pythonic wrapper around FFTW, the FFT library,
    presenting a unified interface for all the supported transforms."""

    homepage = "https://pyfftw.readthedocs.io/en/latest/"
    pypi = "pyfftw/pyfftw-0.15.1.tar.gz"

    license("BSD-3-Clause")

    # Builtin's py-setuptools@:59.4.0 is unconditional and predates pyproject support.
    version(
        "0.15.1",
        sha256="bbcde6d40d165e1cbaf12dde062ebfebe9e43394cac8c166e699ba2c9a4b0461",
    )

    depends_on("c", type="build")

    depends_on("python@3.11:", type=("build", "run"))

    depends_on("py-setuptools@77:", type="build")
    depends_on("py-setuptools-scm@8:", type="build")
    depends_on("py-cython@3.0:3", type="build")

    depends_on("py-numpy@1.20:", type=("build", "run"))

    depends_on("fftw@3.3:")

    def setup_build_environment(self, env: EnvironmentModifications) -> None:
        env.prepend_path("CPATH", self.spec["fftw"].prefix.include)
        # setuptools appends LDFLAGS to the extension link line, so the RPATH to fftw
        # does not depend on that link going through Spack's wrapper.
        for libdir in self.spec["fftw"].libs.directories:
            env.prepend_path("LIBRARY_PATH", libdir)
            env.append_flags("LDFLAGS", f"-Wl,-rpath,{libdir}")
