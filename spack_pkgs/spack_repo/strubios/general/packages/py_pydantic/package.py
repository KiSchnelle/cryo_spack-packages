# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack_repo.builtin.packages.py_pydantic.package import PyPydantic as BuiltinPyPydantic


class PyPydantic(BuiltinPyPydantic):
    # RELION environment.yml:19 pins pydantic==1.10.18, which builtin does not carry.
    version("1.10.18", sha256="baebdff1907d1d96a139c25136a9bb7d17e118f133a76a2ef3b845e831e3403a")
