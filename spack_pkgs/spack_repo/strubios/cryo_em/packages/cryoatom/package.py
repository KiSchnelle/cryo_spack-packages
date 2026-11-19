import hashlib
import os
import zipfile

from spack_repo.builtin.build_systems.generic import Package

from spack.package import *


class Cryoatom(Package):
    """CryoAtom: builds atomic models of proteins and nucleic acids into cryo-EM maps.

    CryoAtom is only supported in the conda environment of its linux.yml (Python 3.9,
    PyTorch 2.1 for CUDA 11.8), so this recipe creates that environment in the install
    folder, from two exact package lists, and installs CryoAtom into it.

    The model files are part of the package: the checkpoints of CryoAtom, and the two
    language models it uses, ESM-2 and RNA-FM. Nothing is downloaded when it runs."""

    homepage = "https://github.com/YangLab-SDU/CryoAtom"
    url = "https://github.com/YangLab-SDU/CryoAtom/archive/refs/tags/v2.2.0.tar.gz"

    license("MIT")

    version("2.2.0", sha256="f0ba76a7880fb12c2650272d135b19d5b105bf8d04d645e8b6c4e4e6b3e1b920")

    #: sha256 of the two package lists of each version, (conda, pip). The lists are
    #: the files next to this one:
    #:   conda-linux-64-<version>.txt   as written by "conda list --explicit --sha256"
    #:   pip-linux-64-<version>.txt     pip requirements with a --hash for every package
    #: The checksums stand here because spack only looks at this file: a changed list
    #: then means a new build.
    #:
    #: How the lists of 2.2.0 were made, on Rocky 9 with miniforge3, from the linux.yml
    #: of the release:
    #:   CONDA_OVERRIDE_GLIBC=2.34 CONDA_OVERRIDE_CUDA=11.8 \
    #:       conda create -c pytorch -c nvidia -c conda-forge <the conda part>
    #:   pip install --report report.json <the pip part>
    #: The pip list is name==version and the sha256 of every file in the report.
    package_lists = {
        "2.2.0": (
            "1a53beaa17b4a61d92821c75fdfe80b1c465e74fafdd00a4ad44988c844a0b99",
            "fc6a41e23234f49d5de7eb25c4080bae925d1eaa89e3bef793c96807fcbeb439",
        )
    }

    # The model files are fetched by spack and not unpacked. install.sh of CryoAtom
    # downloads the same files.
    resource(
        name="checkpoints",
        url="https://yanglab.qd.sdu.edu.cn/CryoAtom/download/checkpoints_v2.1.zip",
        sha256="14667161219f1e70e3edfc0e25cc2d2ab342e8428ebc4e5659c66bf84ccc3bfd",
        expand=False,
        placement="checkpoints",
        when="@2.1:",
    )
    resource(
        name="rna-fm",
        url="https://yanglab.qd.sdu.edu.cn/CryoAtom/download/RNA-FM_pretrained.pth",
        sha256="5b5d7d87b37c291ef42c140ef9edf7aea29f255fa2a4fd435f776c52e93d5e99",
        expand=False,
        placement="rna-fm",
    )
    resource(
        name="esm2",
        url="https://dl.fbaipublicfiles.com/fair-esm/models/esm2_t33_650M_UR50D.pt",
        sha256="ea9d0522b335a8778dea6535a65301f10208dece28cd5865482b0b1fc446168c",
        expand=False,
        placement="esm2",
    )
    resource(
        name="esm2-contact-regression",
        url="https://dl.fbaipublicfiles.com/fair-esm/regression/esm2_t33_650M_UR50D-contact-regression.pt",
        sha256="8ffe6edbd4173dc8d45c2cd5cb27d43aad77ec26b4c768200c58ae1f96693575",
        expand=False,
        placement="esm2-contact-regression",
    )

    depends_on("miniforge3", type="build")

    requires("platform=linux", msg="The package lists are for Linux")
    conflicts("target=aarch64:", msg="The package lists are for x86_64")

    sanity_check_is_file = [
        "bin/cryoatom",
        "share/cryoatom/torch_home/hub/checkpoints/esm2_t33_650M_UR50D.pt",
        "share/cryoatom/torch_home/hub/checkpoints/esm2_t33_650M_UR50D-contact-regression.pt",
        "share/cryoatom/torch_home/hub/checkpoints/RNA-FM_pretrained.pth",
    ]

    @property
    def _torch_home(self):
        # ESM-2 and RNA-FM are looked up in <TORCH_HOME>/hub/checkpoints
        return str(self.prefix.share.cryoatom.torch_home)

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

        # The checkpoints have to be in the source before CryoAtom is installed:
        # setup.py takes CryoAtom2/checkpoint/*.pth along as package data.
        with zipfile.ZipFile(find("checkpoints", "*.zip")[0]) as archive:
            archive.extractall(".")

        conda = Executable(spec["miniforge3"].prefix.bin.conda)
        # the downloads and conda's own files stay in the build folder
        with set_env(
            HOME=self.stage.path,
            CONDA_PKGS_DIRS=join_path(self.stage.path, "pkgs"),
            PIP_CACHE_DIR=join_path(self.stage.path, "pip-cache"),
        ):
            # --yes: the install folder exists already, and conda asks before using it
            conda("create", "--yes", "--prefix", prefix, "--file", conda_list)
            python = Executable(prefix.bin.python)
            # --no-deps: the list names every package, pip must not add others
            # --no-build-isolation: ptflops only exists as a source package. pip builds
            # it with the setuptools of the environment and downloads nothing for that.
            pip = ("-m", "pip", "install", "--no-deps", "--no-build-isolation")
            python(*pip, "--require-hashes", "--requirement", pip_list)
            python(*pip, ".")

        package = python("-c", "import CryoAtom2; print(CryoAtom2.__path__[0])", output=str)
        package = package.strip()
        for name in ("CryoNet.pth", "CryoNet_no_seq.pth", "RUNet.pth"):
            if not os.path.isfile(join_path(package, "checkpoint", name)):
                raise InstallError(f"the checkpoint {name} was not installed")
        # install.sh does this too: pip does not keep the executable bit
        set_executable(join_path(package, "utils", "getp"))

        models = join_path(self._torch_home, "hub", "checkpoints")
        mkdirp(models)
        for folder in ("esm2", "esm2-contact-regression", "rna-fm"):
            for model in find(folder, "*"):
                install(model, models)

        # the program starts, with the environment as it was just installed
        Executable(prefix.bin.cryoatom)("--version")

    def setup_run_environment(self, env):
        # spack puts bin/ on PATH itself
        env.set("TORCH_HOME", self._torch_home)
