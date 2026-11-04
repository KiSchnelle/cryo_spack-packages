# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack_repo.builtin.packages.alsa_lib.package import AlsaLib as BuiltinAlsaLib


class AlsaLib(BuiltinAlsaLib):
    # Builtin fetches over FTP, which is untested on the install node. Use HTTPS.
    url = "https://www.alsa-project.org/files/pub/lib/alsa-lib-1.2.15.3.tar.bz2"
