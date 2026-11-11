# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack_repo.builtin.packages.py_scipy.package import PyScipy as BuiltinPyScipy


class PyScipy(BuiltinPyScipy):
    # RELION pins scipy 1.11.2. scipy up to 1.11 compiles with -std=c++14 (meson.build),
    # but pythran 0.19 moved its headers to C++17 (std::is_integral_v, ...), and builtin has
    # no upper bound. Upstream 1.11.2 asks for pythran<0.14, but builtin only has 0.12.x
    # there, which predates numpy 1.26. 0.18.1 is the newest C++14 pythran.
    # Remove this override once builtin caps pythran for these versions.
    depends_on("py-pythran@:0.18", type="build", when="@:1.11")
