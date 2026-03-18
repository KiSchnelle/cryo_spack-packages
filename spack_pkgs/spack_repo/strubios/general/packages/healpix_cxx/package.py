# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack_repo.builtin.build_systems.autotools import AutotoolsPackage


class HealpixCxx(AutotoolsPackage):
    """Healpix-CXX is a C/C++ library for calculating
    Hierarchical Equal Area isoLatitude Pixelation of a sphere."""

    homepage = "https://healpix.sourceforge.io"
    url = "https://ayera.dl.sourceforge.net/project/healpix/Healpix_3.50/healpix_cxx-3.50.0.tar.gz"

    license("GPL-2.0-or-later")

    version(
        "3.50.0",
        sha256="6538ee160423e8a0c0f92cf2b2001e1a2afd9567d026a86ff6e2287c1580cb4c",
    )

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("cfitsio")
    depends_on("libsharp", type="build")

    def patch(self):
        spec = self.spec
        configure_fix = FileFilter("configure")
        # Link libsharp static libs
        configure_fix.filter(
            r"^SHARP_LIBS=.*$",
            'SHARP_LIBS="-L{0} -lsharp -lc_utils -lfftpack -lm"'.format(
                spec["libsharp"].prefix.lib
            ),
        )
        # Fix cfitsio version check broken by 3-part version numbers
        fitshandle = FileFilter("cxxsupport/fitshandle.cc")
        fitshandle.filter(
            r"int v_header\s*=\s*nearest<int>\(1000\.\*CFITSIO_VERSION\)",
            "int v_header  = CFITSIO_MAJOR*1000 + CFITSIO_MINOR*100",
        )
