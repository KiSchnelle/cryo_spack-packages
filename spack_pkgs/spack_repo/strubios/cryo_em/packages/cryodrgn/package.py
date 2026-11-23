# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class Cryodrgn(PythonPackage):
    """CryoDRGN is a neural network based algorithm for heterogeneous cryo-EM reconstruction.
    In particular, the method models a continuous distribution over 3D structures by using a
    neural network based representation for the volume"""

    homepage = "https://cryodrgn.cs.princeton.edu/"
    pypi = "cryodrgn/cryodrgn-4.3.1.tar.gz"

    license("GPL-3.0-only")

    # Builtin only has up to 3.4.3.
    version("4.3.1", sha256="ad87aae88aea860b4b9487a0f8e469ce1cf9843625a2368be3f69d0bb14be3ed")

    depends_on("py-setuptools@61:", type="build")
    depends_on("py-setuptools-scm@6.2:", type="build")

    with default_args(type=("build", "run")):
        # from pyproject.toml of 4.3.1
        depends_on("python@3.10:")
        depends_on("py-scikit-learn")
        depends_on("py-torch@2:")
        depends_on("py-numpy@1.25:")
        depends_on("py-scipy@1.3.1:")
        depends_on("py-pandas@2.2:")
        depends_on("py-healpy")
        depends_on("py-umap-learn")
        depends_on("py-igraph")
        depends_on("py-starfile")
        depends_on("py-pyyaml")
        depends_on("py-matplotlib@3.7:")
        depends_on("py-seaborn@0.12.2:")
        depends_on("py-flask@3:")
        depends_on("py-jupyterlab@4:")
        depends_on("py-notebook@6:")
        depends_on("py-ipywidgets@8:")
        depends_on("py-plotly@5:6")
        depends_on("py-anywidget")
