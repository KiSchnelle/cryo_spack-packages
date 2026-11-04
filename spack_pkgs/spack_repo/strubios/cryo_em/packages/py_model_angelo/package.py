# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

from spack.package import *
from spack_repo.builtin.build_systems.cuda import CudaPackage
from spack_repo.builtin.build_systems.python import PythonPackage


class PyModelAngelo(PythonPackage, CudaPackage):
    """ModelAngelo is an automatic atomic model building program for cryo-EM maps."""

    homepage = "https://github.com/3dem/model-angelo"
    git = "https://github.com/3dem/model-angelo.git"
    url = "https://github.com/3dem/model-angelo/archive/refs/tags/v1.0.18.tar.gz"

    license("MIT", checked_by="snehring")

    version("main", branch="main")
    version(
        "1.0.18",
        sha256="94f2463df97dbd4911fc77fd09c3c35dfd06e0a28c0e99bf73c5697541fe9fe2",
        preferred=True,
    )

    variant("cuda", default=True, description="Use CUDA")
    conflicts("~cuda", msg="This site builds GPU versions only")

    variant(
        "weights",
        default=True,
        description="Install the nucleotides bundles and ESM-1b (12.1 GB) in the prefix; "
        "py-relion uses ~weights",
    )

    conflicts(
        "cuda_arch=none",
        when="+cuda",
        msg="Must specify CUDA compute capabilities of your GPU, see "
        "https://developer.nvidia.com/cuda-gpus",
    )

    depends_on("py-setuptools", type="build")
    depends_on("python@3.11", type=("build", "run"))

    # CUDA-aware deps — propagate cuda_arch
    for _arch in CudaPackage.cuda_arch_values:
        depends_on(
            f"py-torch@2:+cuda cuda_arch={_arch}",
            when=f"+cuda cuda_arch={_arch}",
            type=("build", "run"),
        )

    depends_on("py-tqdm", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-biopython@1.81:", type=("build", "run"))
    depends_on("py-einops", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-mrcfile", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-fair-esm@1.0.3", type=("build", "run"))
    depends_on("py-pyhmmer@0.7.1", type=("build", "run"))
    depends_on("py-loguru", type=("build", "run"))
    depends_on("py-numpy@:1", type=("build", "run"))
    depends_on("py-psutil", type=("build", "run"))
    depends_on("py-wget", type=("build", "run"))

    def setup_run_environment(self, env):
        if self.spec.satisfies("+weights"):
            env.set("TORCH_HOME", str(self.prefix.share.model_angelo))

    @run_after("install", when="+weights")
    def download_weights(self):
        torch_home = str(self.prefix.share.model_angelo)
        mkdirp(torch_home)
        site_pkgs = join_path(self.prefix, self.spec["python"].package.purelib)
        env = {
            "TORCH_HOME": torch_home,
            "PYTHONPATH": site_pkgs + os.pathsep + os.environ.get("PYTHONPATH", ""),
        }
        model_angelo = Executable(join_path(self.prefix.bin, "model_angelo"))
        # v1.0.18 has model definitions only for the two nucleotides bundles
        for bundle in ("nucleotides", "nucleotides_no_seq"):
            model_angelo("setup_weights", "--bundle-name", bundle, extra_env=env, timeout=4 * 3600)
        # main() turns any TypeError into a help message and exit status 0
        ckpt = join_path(torch_home, "hub", "checkpoints")
        for name, size in (
            ("model_angelo_v1.0/nucleotides/success.txt", None),
            ("model_angelo_v1.0/nucleotides_no_seq/success.txt", None),
            ("esm1b_t33_650M_UR50S.pt", 7828576466),
            ("esm1b_t33_650M_UR50S-contact-regression.pt", 3174),
        ):
            path = join_path(ckpt, name)
            if not os.path.isfile(path) or (size and os.path.getsize(path) != size):
                raise InstallError(f"Missing or bad ModelAngelo weight: {name}")
