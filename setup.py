import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pygrocy",
    version="2.0.0",
    author="Sebastian Rutofski",
    author_email="kontakt@sebastian-rutofski.de",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sebrut/pygrocy",
    license="MIT",
    packages=setuptools.find_packages(),
    install_requires=[
        "requests",
        "backports.zoneinfo;python_version<'3.9'",  # backports can be removed when python 3.8 support is dropped
        "deprecation~=2.1.0",
        "pydantic>=1.8.2,<1.11.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
