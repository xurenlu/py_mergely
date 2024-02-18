from setuptools import setup, find_packages

setup(
    name="mergely",
    version="0.1.8",
    packages=find_packages(),
    description="A Python SDK for Mergely",
    author="hg_nohair",
    author_email="<xurenlu@gmail.com>",
    license="MIT",
    install_requires=["requests"],
    python_requires=">=3.9",
)
