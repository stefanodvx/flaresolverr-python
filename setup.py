import setuptools

setuptools.setup(
    name="flaresolverr",
    version="1.0",
    install_requires=["httpx"],
    packages=setuptools.find_packages(),
    python_requires=">=3.11",
)