from setuptools import setup, find_packages, Extension
import subprocess
import os
import platform

def check_avx2_support():
    try:
        flags = subprocess.check_output(['cat', '/proc/cpuinfo']).decode()
        print("FOUND AVX2!")
        return 'avx2' in flags
    except:
        print("NOT FOUND AVX2!")
        return False

def update_submodules():
    if os.path.exists(".git"):
        try:
            subprocess.check_call(["git", "submodule", "update", "--init", "--recursive"])
        except subprocess.CalledProcessError as e:
            print(f"Failed to update submodules: {e}")
            raise

# Update submodules
update_submodules()

# Check for AVX2 support
has_avx2 = check_avx2_support()

# Base compile arguments
compile_args = ["-O3", "-Wall", "-Wextra"]
link_args = ["-O3", "-Wall", "-Wextra"]

# Add AVX2 flag if supported
if has_avx2:
    compile_args.append("-mavx2")

zipnn_core_extension = Extension(
    "zipnn_core",
    sources=[
        "csrc/zipnn_core_module.c",
        "csrc/zipnn_core.c",
        "csrc/data_manipulation_dtype16.c",
        "csrc/data_manipulation_dtype32.c",
        "include/FiniteStateEntropy/lib/fse_compress.c",
        "include/FiniteStateEntropy/lib/fse_decompress.c",
        "include/FiniteStateEntropy/lib/huf_compress.c",
        "include/FiniteStateEntropy/lib/huf_decompress.c",
        "include/FiniteStateEntropy/lib/entropy_common.c",
        "include/FiniteStateEntropy/lib/hist.c",
    ],
    include_dirs=["include/FiniteStateEntropy/lib/", "csrc/"],
    extra_compile_args=compile_args,
    extra_link_args=link_args,
    define_macros=[('HAS_AVX2', '1')] if has_avx2 else []
)

setup(
    name="zipnn",
    version="0.5.1",
    author="ZipNN Contributors",
    description="A Lossless Compression Library for AI pipelines",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/zipnn/zipnn",
    packages=find_packages(include=["zipnn", "zipnn.*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "numpy",
        "zstandard",
        "torch",
        "safetensors"
    ],
    ext_modules=[zipnn_core_extension],  # Add the C extension module here
)