# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack_repo.builtin.packages.pbzip2.package import Pbzip2 as BuiltinPbzip2


class Pbzip2(BuiltinPbzip2):
    def edit(self, spec, prefix):
        super().edit(spec, prefix)
        # Unlike builtin, also set the RPATH: relion runs pbzip2 without LD_LIBRARY_PATH.
        libdirs = spec["bzip2"].libs.directories
        ldflags = " ".join(f"-L{d} -Wl,-rpath,{d}" for d in libdirs)
        FileFilter("Makefile").filter(r"^LDFLAGS = .*$", f"LDFLAGS = {ldflags}")
