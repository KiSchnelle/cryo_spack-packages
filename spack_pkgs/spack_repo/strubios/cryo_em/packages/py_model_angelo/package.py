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

    variant(
        "weights",
        default=True,
        description="Download all model weight bundles at install time",
    )

    conflicts(
        "cuda_arch=none",
        when="+cuda",
        msg="Must specify CUDA compute capabilities of your GPU, see "
        "https://developer.nvidia.com/cuda-gpus",
    )

    depends_on("py-setuptools", type="build")
    depends_on("python@3.11:", type=("build", "run"))

    # CUDA-aware deps — propagate cuda_arch
    for _arch in CudaPackage.cuda_arch_values:
        depends_on(
            f"py-torch@2:+cuda cuda_arch={_arch}",
            when=f"+cuda cuda_arch={_arch}",
            type=("build", "run"),
        )
    depends_on("py-torch@2:~cuda", when="~cuda", type=("build", "run"))

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

    @run_after("install")
    def download_weights(self):
        if not self.spec.satisfies("+weights"):
            return

        torch_home = self.prefix.share.model_angelo
        mkdirp(torch_home)
        os.environ["TORCH_HOME"] = str(torch_home)

        site_pkgs = join_path(self.prefix, self.spec["python"].package.platlib)
        os.environ["PYTHONPATH"] = (
            site_pkgs + os.pathsep + os.environ.get("PYTHONPATH", "")
        )

        model_angelo = Executable(join_path(self.prefix.bin, "model_angelo"))
        for bundle in (
            "nucleotides",
            "nucleotides_no_seq",
            "original",
            "original_no_seq",
            "small_gpu",
        ):
            model_angelo("setup_weights", "--bundle-name", bundle)
