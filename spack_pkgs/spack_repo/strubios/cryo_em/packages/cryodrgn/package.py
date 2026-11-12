# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack_repo.builtin.build_systems.python import PythonPackage


class Cryodrgn(PythonPackage):
    """CryoDRGN is a neural network based algorithm for heterogeneous cryo-EM reconstruction.
    In particular, the method models a continuous distribution over 3D structures by using a
    neural network based representation for the volume"""

    # Full copy of builtin instead of a subclass: builtin caps pandas, numpy, matplotlib,
    # seaborn and ipywidgets for all versions, and a subclass cannot drop those directives.
    # Builtin only has up to 3.4.3, whose caps keep cryodrgn from sharing a py-torch build
    # with the other Python packages in the environment.

    homepage = "https://cryodrgn.cs.princeton.edu/"
    pypi = "cryodrgn/cryodrgn-4.3.1.tar.gz"

    license("GPL-3.0-only")

    version("4.3.1", sha256="ad87aae88aea860b4b9487a0f8e469ce1cf9843625a2368be3f69d0bb14be3ed")
    version("3.4.3", sha256="eadc41190d3c6abe983164db299ebb0d7340840281774eaaea1a12627a80dc10")
    version("2.3.0", sha256="9dd75967fddfa56d6b2fbfc56933c50c9fb994326112513f223e8296adbf0afc")

    depends_on("py-setuptools@61:", type="build")
    depends_on("py-setuptools-scm@6.2:", type="build")

    with default_args(type=("build", "run")):
        depends_on("python@3.10:", when="@4:")
        depends_on("python@3.9:3.11", when="@3.4.3")
        depends_on("python@3.7:3.11", when="@2.3.0")

        depends_on("py-pyyaml")
        depends_on("py-scipy@1.3.1:")
        depends_on("py-scikit-learn")
        depends_on("py-umap-learn")
        depends_on("py-healpy")

        # From pyproject.toml of 4.3.1. No upper bounds; upstream CI tests numpy 1.25 to 2.4.
        with when("@4:"):
            depends_on("py-torch@2:")
            depends_on("py-numpy@1.25:")
            depends_on("py-pandas@2.2:")
            depends_on("py-matplotlib@3.7:")
            depends_on("py-seaborn@0.12.2:")
            depends_on("py-jupyterlab@4:")
            depends_on("py-notebook@6:")
            depends_on("py-ipywidgets@8:")
            depends_on("py-plotly@5:6")
            depends_on("py-igraph")
            depends_on("py-starfile")
            depends_on("py-flask@3:")
            depends_on("py-anywidget")

        # Old versions, constraints as in builtin.
        with when("@:3"):
            depends_on("py-torch@1:")
            depends_on("py-numpy@:1.26")
            depends_on("py-pandas@:1")
            depends_on("py-matplotlib@:3.6")
            depends_on("py-seaborn@:0.11")
            depends_on("py-cufflinks")
            depends_on("py-jupyterlab")
            depends_on("py-ipywidgets@:7")
        depends_on("py-notebook@:6", when="@3.4.3")
