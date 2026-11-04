# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack_repo.builtin.packages.py_morphosamplers.package import (
    PyMorphosamplers as BuiltinPyMorphosamplers,
)


class PyMorphosamplers(BuiltinPyMorphosamplers):
    # RELION environment.yml:18 pins 0.0.13; builtin only has 0.0.16.
    version("0.0.13", sha256="7a59e87932d04b366e62ce9105390598a6b3bba6675d9adf2450b32bd7057f22")
