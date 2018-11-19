import os
import setuptools

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename)) 
    return paths

extra_files = package_files('/n_data')

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rcwa",
    version="0.0.2",
    author="Luocheng Huang",
    author_email="luochengcheng@gmail.com",
    description="This is a S4 wrapper to make your life easier",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Luochenghuang/shared_lib",
    packages=setuptools.find_packages(),
    package_data={'', extra_files},
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Linux",
    ],
    include_package_data=True,
)
