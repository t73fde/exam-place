#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from setuptools import setup, find_packages

if __name__ == "__main__":
    here = os.path.abspath(".")
    README = open(os.path.join(here, 'README.rst')).read()
    # CHANGES = open(os.path.join(here, 'CHANGELOG')).read()

    setup(
        name="exam-place",
        description="Calculate student seat numbers for examination",
        long_description=README,
        version='0.0.1',
        packages=find_packages(),
        install_requires=["xlrd>=0.9.3", "xlwt>=1.0.0"],
        license="APL2",
        url="https://github.com/t73fde/exam-place",
        maintainer="Detlef Stern",
        maintainer_email="mail-examplace@yoyod.de",
        keywords="exam random place",
        classifiers=[
            "Development Status :: 1 - Planning",
            "Environment :: Console",
            "Intended Audience :: Education",
            "License :: OSI Approved :: Apache Software License",
            "Programming Language :: Python :: 3.4",
            "Topic :: Utilities",
        ],
        entry_points={
            'console_scripts': [
                'exam-place = exam_place.main:main',
                ],
        }

    )
