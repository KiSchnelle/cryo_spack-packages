import os

from spack.package import *
from spack_repo.builtin.build_systems.generic import Package


class Phenix(Package):
    """Phenix: Python-based Hierarchical Environment for Integrated Xtallography"""

    homepage = "https://phenix-online.org/"
    # Point this URL to your downloaded file
    url = "file:////sbdata/software/download/phenix-installer-1.21.2-5419-intel-linux-2.6-x86_64-centos6.tar"

    maintainers = ["your-github-username"]

    version(
        "1.20.1-5419",
        sha256="9fd612dd2b318b7723144845ac92aef3b7b23f7664c41a062995e4833328d150",
    )

    def install(self, spec, prefix):
        installer_dir = self.stage.source_path

        with working_dir(installer_dir):
            # Make sure the install script is executable
            install_sh = os.path.join(installer_dir, "install")
            chmod = which("chmod")
            chmod("+x", install_sh)

            # Run the install script with --prefix=$prefix
            Executable(install_sh)("--prefix={0}".format(prefix))

    def setup_run_environment(self, env):
        # Phenix puts everything into a subdirectory, e.g. $prefix/phenix-1.20.1-4860
        # Find that directory
        subdirs = [d for d in os.listdir(self.prefix) if d.startswith("phenix")]
        if not subdirs:
            raise InstallError("Could not find phenix subdirectory in prefix.")
        phenix_dir = os.path.join(self.prefix, subdirs[0])

        # source the environment file for full setup
        env_file = os.path.join(phenix_dir, "phenix_env.sh")
        if os.path.isfile(env_file):
            env.set("PHENIX_ENV_FILE", env_file)
