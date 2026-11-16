import hashlib

from spack_repo.builtin.build_systems.generic import Package

from spack.package import *


class Cryolo(Package):
    """crYOLO: particle picking for cryo-EM.

    crYOLO needs Python 3.8 and NVIDIA's build of TensorFlow 1.15 (CUDA 11), so it gets
    a conda environment of its own in the install folder, from two exact package lists.

    The graphical programs need libGL, libEGL, libXxf86vm and libdrm from the system."""

    homepage = "https://cryolo.readthedocs.io"
    # nothing for spack to download: conda and pip fetch the packages of the lists
    has_code = False

    version("1.9.9")

    #: sha256 of the two package lists of each version, (conda, pip). The lists are
    #: the files next to this one:
    #:   conda-linux-64-<version>.txt   as written by "conda list --explicit --sha256"
    #:   pip-linux-64-<version>.txt     pip requirements with a --hash for every package
    #: The checksums stand here because spack only looks at this file: a changed list
    #: then means a new build.
    #:
    #: How the lists of 1.9.9 were made, in a container with miniforge3:
    #:   conda create -c conda-forge python=3.8 pyqt=5 numpy=1.18.5 'libtiff<4.5'
    #:       wxPython=4.1.1 adwaita-icon-theme 'setuptools<66' pip
    #:   pip install --report report.json 'cryolo[c11]==1.9.9'    (with nvidia_indexes)
    #: libtiff<4.5 is not in crYOLO's instructions: wxPython 4.1.1 needs libtiff.so.5.
    #: The pip list is name==version and the sha256 of every file in the report.
    package_lists = {
        "1.9.9": (
            "5215829b6b94f92b505baab1cfbf64c44f73327caec638bd0bca08762536fe16",
            "94d59af25882afd535aa250e34fff590d33d2845db6a791227bbd666ae0d581d",
        )
    }

    #: Where pip finds NVIDIA's build of TensorFlow 1.15 and what it needs. crYOLO's
    #: instructions use nvidia-pyindex for this, but the address it sets
    #: (pypi.ngc.nvidia.com) is gone.
    nvidia_indexes = [
        "https://developer.download.nvidia.com/compute/redist",
        "https://pypi.nvidia.com",
    ]

    depends_on("miniforge3", type="build")

    requires("platform=linux", msg="The package lists are for Linux")
    conflicts("target=aarch64:", msg="The package lists are for x86_64")

    sanity_check_is_file = ["bin/cryolo_predict.py", "bin/cryolo_gui.py"]

    def _package_list(self, kind, checksum):
        name = f"{kind}-linux-64-{self.version}.txt"
        package_list = join_path(self.package_dir, name)
        with open(package_list, "rb") as f:
            found = hashlib.sha256(f.read()).hexdigest()
        if found != checksum:
            raise InstallError(f"{name} does not have the checksum named in package.py")
        return package_list

    def install(self, spec, prefix):
        checksums = self.package_lists.get(str(self.version))
        if not checksums:
            raise InstallError(f"package.py names no package lists for {self.version}")
        conda_list = self._package_list("conda", checksums[0])
        pip_list = self._package_list("pip", checksums[1])

        conda = Executable(spec["miniforge3"].prefix.bin.conda)
        # the downloads and conda's own files stay in the build folder
        with set_env(
            HOME=self.stage.path,
            CONDA_PKGS_DIRS=join_path(self.stage.path, "pkgs"),
            PIP_CACHE_DIR=join_path(self.stage.path, "pip-cache"),
        ):
            # --yes: the install folder exists already, and conda asks before using it
            conda("create", "--yes", "--prefix", prefix, "--file", conda_list)
            # --no-deps: the list names every package, pip must not add others
            indexes = [f"--extra-index-url={url}" for url in self.nvidia_indexes]
            python = Executable(prefix.bin.python)
            python(
                *("-m", "pip", "install", "--no-deps", "--require-hashes"),
                *indexes,
                *("--requirement", pip_list),
            )
