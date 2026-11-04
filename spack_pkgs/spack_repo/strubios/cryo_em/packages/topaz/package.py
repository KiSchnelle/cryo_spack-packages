# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack_repo.builtin.build_systems.cuda import CudaPackage
from spack_repo.builtin.build_systems.python import PythonPackage


class Topaz(PythonPackage, CudaPackage):
    """topaz: Pipeline for particle picking in cryo-electron microscopy images using
    convolutional neural networks trained from positive and unlabeled examples. Also
    featuring micrograph and tomogram denoising with DNNs."""

    homepage = "https://topaz-em.readthedocs.io/"
    pypi = "topaz-em/topaz_em-0.3.20.tar.gz"

    license("GPL-3.0-or-later")

    version("0.3.20", sha256="839087a9e3b21bf7482b75b2b5ca2e3f742aa092701fa72b2b1f2bf7589489bd")
    # Unpatched baseline to roll back to. Has the KDTree and pi bugs.
    version("0.3.18", sha256="a68a426bea0c0999a714f868694d7a5f07cfb0456098e99ac3e7b33865abcd7b")

    variant("cuda", default=True, description="Build with CUDA")
    conflicts("~cuda", msg="topaz is GPU only on this cluster")
    conflicts("cuda_arch=none", when="+cuda", msg="Must specify cuda_arch")

    # Upstream master fixes with no release yet; the patch header lists the commits.
    patch("topaz_0.3.20_training_fixes.patch", when="@0.3.20")

    depends_on("py-setuptools@61:", type="build")

    for _arch in CudaPackage.cuda_arch_values:
        depends_on(f"py-torch@1: +cuda cuda_arch={_arch}",
                   when=f"+cuda cuda_arch={_arch}", type=("build", "run"))

    with default_args(type=("build", "run")):
        depends_on("python@3.8:3.13.0")  # upstream requires-python <=3.13
        depends_on("py-torchvision")     # imported at memory_mapped_data.py:6, sampler.py:14
        depends_on("py-numpy@1.11:")
        depends_on("py-pandas@0.20.3:")
        depends_on("py-scikit-learn@0.19.0:")
        depends_on("py-scipy@0.17.0:")
        depends_on("py-pillow@6.2.0:")
        depends_on("py-future")
        depends_on("py-tqdm@4.65.0:")
        depends_on("py-h5py@3.7.0:")
        depends_on("py-psutil@5.8.0:", when="@0.3.19:")
