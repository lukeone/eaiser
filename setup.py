# -*- coding: utf-8 -*-
import re
import ast
from setuptools import setup, find_packages
from pip.req import parse_requirements


_version_re = re.compile(r"__version__\s+=\s+(.*)")

with open("easier/__init__.py", "rb") as f:
    version = str(
        ast.literal_eval(_version_re.search(f.read().decode("utf-8")).group(1))
    )

description = "make work easier, make life easier"

install_reqs = parse_requirements("./requirements.txt", session="hack")
reqs = [str(ir.req) for ir in install_reqs]


setup(
    name="easier",
    author="luke",
    author_email="luo86106@gmail.com",
    version=version,
    license="BSD",
    url="http://xluke.info",
    #packages=find_packages(),
    packages=['easier'],
    description=description,
    long_description=open("README.md").read(),
    install_requires=reqs,
    entry_points="""
        [console_scripts]
        easier=easier.main:main
    """,
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
