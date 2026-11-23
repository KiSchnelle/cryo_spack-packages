# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyPynndescent(PythonPackage):
    """PyNNDescent is a Python nearest neighbor descent for
    approximate nearest neighbors."""

    homepage = "https://github.com/lmcinnes/pynndescent"
    pypi = "pynndescent/pynndescent-0.7.0.tar.gz"

    license("BSD-2-Clause")

    # Builtin only has 0.5.7, which fails with numpy 2. cryodrgn runs with numpy 2 and gets
    # 0.7.0. RELION pins numpy 1.26 and stays on 0.5.7, see py-relion.
    version("0.7.0", sha256="54f097a003bfdb917225e1bcf55c4027e283a37a2b5e3cae4b4aaf21197f6d1c")
    version("0.5.7", sha256="ecb395255fa36a748b5870b4ba0300ea0f7da8b1964864b8edd62577a84dfd7d")

    # 0.7 writes its license as an SPDX string, which setuptools reads from 77 on
    depends_on("py-setuptools@77:", type="build", when="@0.7:")
    # 0.5.7 imports pkg_resources, which setuptools 82 removed
    depends_on("py-setuptools@:81", type=("build", "run"), when="@:0.5.7")

    with default_args(type=("build", "run")):
        depends_on("py-scikit-learn@0.18:")
        depends_on("py-scipy@1.0:")
        depends_on("py-numba@0.55:", when="@0.7:")
        depends_on("py-numba@0.51.2:")
        depends_on("py-llvmlite@0.38:", when="@0.7:")
        depends_on("py-llvmlite@0.30:")
        depends_on("py-joblib@0.11:")
        depends_on("py-numpy")
        # np.infty, removed in numpy 2.0, is used up to 0.5.12
        depends_on("py-numpy@:1", when="@:0.5.12")
