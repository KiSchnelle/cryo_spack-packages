import os

from spack.package import *
from spack_repo.builtin.build_systems.generic import Package

# The installers cannot be downloaded without a login, so spack fetches them from a
# place of our own. LOCAL_INSTALLER_LINK is the address in front of the installer's
# file name, for example the download address of a shared folder; the file name is
# appended to it. Read once, when spack loads this file.
_LOCAL_INSTALLER_LINK = os.environ.get("LOCAL_INSTALLER_LINK", "")


class Phenix(Package):
    """Phenix: Python-based Hierarchical Environment for Integrated Xtallography.

    Installs the prebuilt binary distribution. For 2.x this is the CUDA 12 installer."""

    homepage = "https://phenix-online.org/"
    manual_download = True

    version(
        "2.2.1-6174",
        sha256="5afdc9b7c56f6b1d76ba011e58c1e4c0b3dac8a76b965da3dd30f0ad472d9ade",
        expand=False,
    )
    version(
        "1.21.2-5419",
        sha256="9fd612dd2b318b7723144845ac92aef3b7b23f7664c41a062995e4833328d150",
        extension="tar",
    )

    #: File name of the installer of each version.
    installers = {
        "2.2.1-6174": "Phenix-2.2.1-6174-CUDA12-Linux-x86_64.sh",
        "1.21.2-5419": "phenix-installer-1.21.2-5419-intel-linux-2.6-x86_64-centos6.tar",
    }

    requires("platform=linux", msg="Only the Linux installers are packaged")
    conflicts("target=aarch64:", msg="Phenix installers are x86_64 binaries")

    @property
    def _phenix_dir(self):
        return join_path(self.prefix, f"phenix-{self.version}")

    @property
    def sanity_check_is_file(self):
        return [join_path(f"phenix-{self.version}", "phenix_env.sh")]

    def url_for_version(self, version):
        name = self.installers[str(version)]
        # Without the link: spack's convention for manual downloads, the installer is
        # expected in the directory spack is run from.
        return (_LOCAL_INSTALLER_LINK or f"file://{os.getcwd()}/") + name

    @property
    def download_instr(self):
        return (
            f"The installer {self.installers[str(self.version)]} cannot be downloaded "
            "without a login. Set LOCAL_INSTALLER_LINK to the address it can be fetched "
            "from (the file name is appended to it) and install again."
        )

    def setup_build_environment(self, env):
        # The link is a secret. The installer does not need it, and spack writes the
        # build environment to a file that CI keeps when a build fails.
        env.unset("LOCAL_INSTALLER_LINK")

    def install(self, spec, prefix):
        if spec.satisfies("@2:"):
            self._install_conda_style()
        else:
            self._install_legacy(prefix)

    def _install_conda_style(self):
        # The installer runs files it extracts to TMPDIR, so that must not be noexec,
        # and the docs ask for ~25 GB of temporary space. Use the stage instead of /tmp.
        with set_env(TMPDIR=self.stage.path):
            # spack names the downloaded file after its address, which can contain
            # characters like ? and &. Run the installer under its own name.
            installer = join_path(self.stage.path, self.installers[str(self.version)])
            if not os.path.lexists(installer):
                os.symlink(self.stage.archive_file, installer)
            # The docs require the phenix-<version> subdirectory below the prefix.
            bash = which("bash", required=True)
            bash(installer, "-b", "-p", self._phenix_dir)

    def _install_legacy(self, prefix):
        # Creates $prefix/phenix-<version>
        with working_dir(self.stage.source_path):
            set_executable("install")
            Executable("./install")(f"--prefix={prefix}")

    def setup_run_environment(self, env):
        # phenix_env.sh sets PHENIX, PHENIX_PREFIX, PHENIX_VERSION and PATH.
        env.extend(
            EnvironmentModifications.from_sourcing_file(
                join_path(self._phenix_dir, "phenix_env.sh")
            )
        )
