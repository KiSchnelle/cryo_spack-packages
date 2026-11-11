# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack_repo.builtin.packages.py_grpcio.package import PyGrpcio as BuiltinPyGrpcio


class PyGrpcio(BuiltinPyGrpcio):
    # Builtin applies grpc commit 223be69 (missing includes for abseil-cpp 20260107) to
    # @1.71:1.76, but one of its files, src/core/channelz/v2tov1/property_list.cc, only
    # exists from 1.75 on, so 1.71 fails in the patch stage. 1.75 takes the patch and
    # 1.78+ already contain it. Remove this override once builtin fixes the range.
    conflicts("@1.71", msg="builtin's grpc 223be69 patch does not apply to py-grpcio 1.71")
