# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack_repo.builtin.build_systems.python import PythonPackage


class PyDijkstra3d(PythonPackage):
    """
    Dijkstra3d is a Python package that implements Dijkstra's algorithm for finding the shortest paths in a 3D grid.
    It is designed to be efficient and easy to use, making it suitable for applications such as pathfinding in 3D environments, robotics, and computer graphics.
    """

    homepage = "https://github.com/seung-lab/dijkstra3d"
    pypi = "dijkstra3d/dijkstra3d-1.2.0.tar.gz"

    license("GPL-3.0-or-later")

    version(
        "1.2.0",
        sha256="99a586e683cffb08aadb9f60f2c899a45cf9624fe0f3e4b9abce658b6841f8b3",
    )

    depends_on("py-setuptools@42:", type="build")
    depends_on("py-wheel", type="build")
    depends_on("py-cython", type="build")
    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
