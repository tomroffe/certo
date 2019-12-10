import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='procudo',
    version="0.0.1",
    author="Tom Roffe",
    author_email="tom@altobyte.io",
    description="OpenVPN User Profile Generator API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tomroffe/procudo",
    packages=setuptools.find_packages(),
    classifiers=[
        "Topic :: System :: Networking",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.7"
    ],
    python_requires='>=3.7',
)
