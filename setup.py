import setuptools

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
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Linux",
    ],
)
