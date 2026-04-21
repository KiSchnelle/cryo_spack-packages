# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack_repo.builtin.build_systems.python import PythonPackage


class PyNapariThreedee(PythonPackage):
    """
        napari-3d is a napari plugin for visualizing 3D data in napari, including support for
    rendering 3D meshes and volumes, as well as interactive slicing and volume rendering.
    """

    homepage = "https://github.com/napari-threedee/napari-threedee"
    pypi = "napari-threedee/napari_threedee-0.0.28.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.0.28",
        sha256="c6e9f9262e2c627473b15dc8de615549b1b4cdbf14744659b5eda5ffe5446c6a",
    )
    version(
        "0.0.21",
        sha256="fb10e0031b45de6ed40d315e1df5e02337c7dca23f08235f465b7b8bf9bda012",
    )

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", type="build")
    depends_on("python@3.8:", type=("build", "run"))

    depends_on("py-einops", type=("build", "run"))
    depends_on("py-imageio@2.5.0:", type=("build", "run"))
    conflicts(
        "^py-imageio@2.11.0",
        msg="py-imageio 2.11.0 is incompatible with py-napari-threedee",
    )
    conflicts(
        "^py-imageio@2.22.1",
        msg="py-imageio 2.22.1 is incompatible with py-napari-threedee",
    )
    depends_on("py-libigl", type=("build", "run"))
    depends_on("py-magicgui", type=("build", "run"))
    depends_on("py-morphosamplers", type=("build", "run"))
    depends_on("py-mrcfile", type=("build", "run"))
    depends_on("py-napari@:4", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-pooch", type=("build", "run"))
    depends_on("py-psygnal", type=("build", "run"))
    depends_on("py-pydantic", type=("build", "run"))
    depends_on("py-qtpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-superqt", type=("build", "run"))
    depends_on("py-vispy", type=("build", "run"))
    depends_on("py-zarr", type=("build", "run"))
