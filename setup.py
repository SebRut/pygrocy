import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pygrocy",
    version="0.22.0",
    author="Sebastian Rutofski",
    author_email="kontakt@sebastian-rutofski.de",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sebrut/pygrocy",
    license="MIT",
    packages=setuptools.find_packages(),
    install_requires=["requests", "iso8601", "pytz", "tzlocal"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
