import os
import sys
import torch
from setuptools import setup, find_packages
from torch.utils.cpp_extension import BuildExtension, CUDAExtension

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

print(PROJECT_ROOT)

def load_requirements(filename):п
    with open(os.path.join(PROJECT_ROOT, filename), "r") as f:
        return f.read().splitlines()

def trt_inc_dir():
    return "/usr/include/aarch64-linux-gnu"

def trt_lib_dir():
    return "/usr/lib/aarch64-linux-gnu"

ext_modules = []

plugins_ext_module = CUDAExtension(
        name='plugins', 
        sources=[
            'torch2trt/plugins/plugins.cpp'
        ],
        include_dirs=[
            trt_inc_dir()
        ],
        library_dirs=[
            trt_lib_dir()
        ],
        libraries=[
            'nvinfer'
        ],
        extra_compile_args={
            'cxx': ['-DUSE_DEPRECATED_INTLIST'] if torch.__version__ < "1.5" else [],
            'nvcc': []
        }
    )
if '--plugins' in sys.argv:
    ext_modules.append(plugins_ext_module)
    sys.argv.remove('--plugins')
    

setup(
    name='torch2trt',
    version='0.2.0',
    description='An easy to use PyTorch to TensorRT converter',
    packages=find_packages(),
    ext_package='torch2trt',
    ext_modules=ext_modules,
    install_requires=load_requirements("requirements.txt"),
    cmdclass={'build_ext': BuildExtension}
)
