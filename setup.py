import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="panamah-sdk-python",
    version="0.0.1",
    author="Casa Magalhães",
    author_email="contato@casamagalhaes.com.br",
    description="Panamah Software Development Kit for Python",
    long_description="APIs and models for Panamah services",
    long_description_content_type="text/markdown",
    url="https://github.com/casamagalhaes/panamah-sdk-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)