# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack_repo.builtin.packages.py_psygnal.package import PyPsygnal as BuiltinPyPsygnal


class PyPsygnal(BuiltinPyPsygnal):
    # RELION 5.x environment.yml:22 pins psygnal==0.11.1; builtin starts at 0.14.0.
    version("0.11.1", sha256="f9b02ca246ab0adb108c4010b4a486e464f940543201074591e50370cd7b0cc0")
