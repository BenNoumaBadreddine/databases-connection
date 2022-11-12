import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    INSTALL_REQUIRES = f.read().splitlines()

setuptools.setup(
    name="dbconnections",
    version="0.0.1",
    install_requires=INSTALL_REQUIRES,
    packages=setuptools.find_packages(),
    author="Badreddine Ben Nouma",
    author_email="badreddine.ben.nouma@gmail.com",
    description="This python tool is used to connect to local and distant database such the aws RDS database",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
