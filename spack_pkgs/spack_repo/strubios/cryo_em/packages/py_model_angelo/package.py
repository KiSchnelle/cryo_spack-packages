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

    license("MIT", checked_by="snehring")

    version("main", branch="main", preferred=True)

    variant(
        "weights",
        default=True,
        description="Download model weights (nucleotides + nucleotides_no_seq) at install time",
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

    depends_on("py-torchvision", type=("build", "run"))
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

    def setup_run_environment(self, env):
        env.set("TORCH_HOME", str(self.prefix.share.model_angelo))

    @run_after("install")
    def download_weights(self):
        if not self.spec.satisfies("+weights"):
            return

        torch_home = self.prefix.share.model_angelo
        mkdirp(torch_home)

        os.environ["TORCH_HOME"] = str(torch_home)
        model_angelo = Executable(join_path(self.prefix.bin, "model_angelo"))
        model_angelo("setup_weights", "--bundle-name", "nucleotides")
        model_angelo("setup_weights", "--bundle-name", "nucleotides_no_seq")
