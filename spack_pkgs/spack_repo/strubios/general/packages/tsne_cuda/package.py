# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack_repo.builtin.build_systems.cuda import CudaPackage
from spack_repo.builtin.packages.tsne_cuda.package import TsneCuda as BuiltinTsneCuda


class TsneCuda(BuiltinTsneCuda):
    # 3.0.1 compiles as C++14; CUDA 13's Thrust needs C++17.
    depends_on("cuda@9:12", when="@:3")
    # Builtin does not forward the arch, and faiss 1.14 headers need C++17.
    for _arch in CudaPackage.cuda_arch_values:
        depends_on(
            f"faiss@1.7.2:1.8 +cuda +shared cuda_arch={_arch}",
            when=f"+cuda cuda_arch={_arch}",
            type=("build", "link", "run"),
        )

    def setup_build_environment(self, env):
        env.prepend_path("LIBRARY_PATH", self.spec["cuda"].libs.directories[0])

    def cmake_args(self):
        args = super().cmake_args()
        cuda_lib = self.spec["cuda"].libs.directories[0]
        args.append(self.define("CMAKE_BUILD_RPATH", cuda_lib))
        args.append(self.define("CMAKE_INSTALL_RPATH", cuda_lib))
        return args

    @run_after("install", when="+python")
    def install_python_module(self):
        src = join_path(self.build_directory, "python", "tsnecuda")
        dst = join_path(python_platlib, "tsnecuda")
        install_tree(src, dst)
        force_remove(join_path(dst, "libtsnecuda.so"))
        install(join_path(self.prefix.lib, "libtsnecuda.so"), dst)
