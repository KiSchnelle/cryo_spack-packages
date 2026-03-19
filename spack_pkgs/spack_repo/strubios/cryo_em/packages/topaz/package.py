# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack_repo.builtin.build_systems.python import PythonPackage


class Topaz(PythonPackage):
    """topaz: Pipeline for particle picking in cryo-electron microscopy images using
    convolutional neural networks trained from positive and unlabeled examples. Also
    featuring micrograph and tomogram denoising with DNNs."""

    homepage = "https://topaz-em.readthedocs.io/"
    git = "https://github.com/tbepler/topaz.git"

    license("GPL-3.0-or-later")

    version("0.3.18", tag="v0.3.18")

    depends_on("python@3.8:3.13.0", when="@0.3.18")
    depends_on("py-setuptools", type="build")
    depends_on("py-torch@1:", type=("build", "run"))
    depends_on("py-torchvision", type=("build", "run"))
    depends_on("py-numpy@1.11:", type=("build", "run"))
    depends_on("py-pandas@0.20.3:", type=("build", "run"))
    depends_on("py-scikit-learn@0.19.0:", type=("build", "run"))
    depends_on("py-scipy@0.17.0:", type=("build", "run"))
    depends_on("py-pillow@6.2.0:", type=("build", "run"))
    depends_on("py-future", type=("build", "run"))
    depends_on("py-tqdm@4.65.0:", type=("build", "run"))
    depends_on("py-h5py@3.7.0:", type=("build", "run"))
