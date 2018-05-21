#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except Exception:
    from distutils.core import setup

setup(
    name='cefp',
    version='0.0.1',
    description='ArcSight CEF Parser',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Atzm Watanabe',
    author_email='atzm@atzm.org',
    entry_points={'console_scripts': ['cefp = cefp:main']},
    license='BSD-2',
    url='https://github.com/atzm/cefp',
    py_modules=['cefp'],
    test_suite='test_cefp',
    tests_require=['ddt'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
    ],
)
