import hashlib

from spack_repo.builtin.build_systems.generic import Package

from spack.package import *


class Eman2(Package):
    """EMAN2: image processing for cryo-EM and cryo-ET.

    EMAN2 is only supported inside a conda environment, so this recipe creates that
    environment in the install folder, from an exact package list."""

    homepage = "https://eman2.org"
    # nothing for spack to download: conda fetches the packages of the list
    has_code = False

    version("2.99.86")

    #: sha256 of the package list of each version. The list is the file
    #: conda-linux-64-<version>.txt next to this one, as written by
    #: "conda list --explicit --sha256". The checksum stands here because spack only
    #: looks at this file: a changed list then means a new build.
    #:
    #: How the list of 2.99.86 was made, in a container with miniforge3:
    #:   CONDA_OVERRIDE_CUDA=12.8 CONDA_OVERRIDE_GLIBC=2.34 \
    #:       conda create -c cryoem -c conda-forge eman-dev=2.99.86
    #: With CONDA_OVERRIDE_CUDA conda takes the CUDA build of TensorFlow.
    package_lists = {"2.99.86": "adafca6b4cb5de9f0cbc99fa9052d24a0b7cfe98d8378a7e9da01422607f5889"}

    depends_on("miniforge3", type="build")

    requires("platform=linux", msg="The package lists are for Linux")
    conflicts("target=aarch64:", msg="The package lists are for x86_64")

    sanity_check_is_file = ["bin/e2version.py"]

    def install(self, spec, prefix):
        name = f"conda-linux-64-{self.version}.txt"
        package_list = join_path(self.package_dir, name)
        with open(package_list, "rb") as f:
            checksum = hashlib.sha256(f.read()).hexdigest()
        if checksum != self.package_lists.get(str(self.version)):
            raise InstallError(f"{name} does not have the checksum named in package.py")

        conda = Executable(spec["miniforge3"].prefix.bin.conda)
        # conda's downloads and its own files stay in the build folder
        with set_env(HOME=self.stage.path, CONDA_PKGS_DIRS=join_path(self.stage.path, "pkgs")):
            # --yes: the install folder exists already, and conda asks before using it
            conda("create", "--yes", "--prefix", prefix, "--file", package_list)

    def setup_run_environment(self, env):
        # spack puts bin/ on PATH itself. EMAN2's docs and examples use CONDA_PREFIX.
        env.set("CONDA_PREFIX", self.prefix)
