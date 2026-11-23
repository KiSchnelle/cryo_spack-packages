# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyUcsfPyem(PythonPackage):
    """UCSF pyem is a collection of Python modules and command-line
    utilities for electron microscopy of biological samples."""

    homepage = "https://github.com/asarnow/pyem"
    url = "https://github.com/asarnow/pyem/archive/refs/tags/v0.69.tar.gz"

    license("GPL-3.0-or-later")

    # Builtin only has two snapshots from 2021 and 2024.
    version("0.69", sha256="969e0075ea7ba854e6ab2c5cf9ab315c7dc994dcb738574707cd4aad380c1105")

    # Bugs of 0.69 itself: --normalize fails with numpy 2, and project.py leaves a column
    # in its star file that makes projection_subtraction.py fail. See the patch header.
    patch("pyem_0.69_fixes.patch")

    depends_on("py-setuptools", type="build")

    # from requirements.txt of 0.69
    with default_args(type=("build", "run")):
        depends_on("py-numba@0.41:")
        # np.row_stack, used by cfsc.py, was removed in numpy 2.5
        depends_on("py-numpy@1.26:2.4")
        # numexpr 2.14.1 gives wrong results on large arrays (numexpr issue 566). pandas
        # shares this numexpr; only its main branch excludes 2.14.1, pandas 3.0 does not.
        depends_on("py-numexpr@2.8:2.14.0")
        depends_on("py-scipy@1.2:")
        depends_on("py-matplotlib@2.2:")
        depends_on("py-seaborn@0.9:")
        depends_on("py-pandas@0.23.4:")
        depends_on("py-pathos@0.2.1:")
        depends_on("py-pyfftw@0.10:")
        depends_on("py-healpy@1.11:")
        depends_on("py-natsort@6.0:")
        depends_on("py-starfile")
        # imported by pyem/cli/star.py, missing from setup.py
        depends_on("py-six")
