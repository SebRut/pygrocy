import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pygrocy",
    version="0.30.0",
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
        "iso8601~=0.1.16",
        "pytz~=2021.1",
        "tzlocal>=2.1,<3.0",
        "deprecation~=2.1.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
