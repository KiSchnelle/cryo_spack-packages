# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class Topaz(PythonPackage):
    """topaz: Pipeline for particle picking in cryo-electron microscopy images using
    convolutional neural networks trained from positive and unlabeled examples. Also
    featuring micrograph and tomogram denoising with DNNs."""

    homepage = "https://topaz-em.readthedocs.io/"
    pypi = "topaz-em/topaz_em-0.3.21.tar.gz"

    license("GPL-3.0-or-later")

    # Builtin stops at 0.3.18, which has training bugs that 0.3.21 fixes.
    version("0.3.21", sha256="3a67a28f4d84f690e2555452bb8f57c88b1c8a0dd11688c1d3fc9307ff782122")

    depends_on("py-setuptools@61:", type="build")

    # from pyproject.toml and requirements.txt of 0.3.21
    with default_args(type=("build", "run")):
        depends_on("python@3.8:3.13")
        depends_on("py-torch@1:")
        depends_on("py-torchvision")
        depends_on("py-tqdm@4.65.0:")
        depends_on("py-h5py@3.7.0:")
        depends_on("py-numpy@1.11:")
        depends_on("py-pandas@0.20.3:")
        depends_on("py-psutil@5.8.0:")
        depends_on("py-scikit-learn@0.19.0:")
        depends_on("py-scipy@0.17.0:")
        depends_on("py-pillow@6.2.0:")
        depends_on("py-future")
