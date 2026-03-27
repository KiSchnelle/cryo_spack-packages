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
    pypi = "napari-threedee/napari-threedee-0.0.29.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.0.29",
        sha256="478c2522ae79b1fa48341d34dd60cdd6139be7418c176ef9f9228b7eed0d8412",
    )

    depends_on("py-hatchling", type="build")
    depends_on("python@3.10:", type=("build", "run"))

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
    depends_on("py-napari@0.5.0:", type=("build", "run"))
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
