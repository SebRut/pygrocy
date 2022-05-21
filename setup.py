import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pygrocy",
    version="1.2.1",
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
        "iso8601>=0.1.16,<1.1.0",
        "pytz>=2021.1,<2023.0",
        "tzlocal>=2.1,<5.0",
        "deprecation~=2.1.0",
        "pydantic>=1.8.2,<1.10.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
