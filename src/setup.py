# -*- coding: utf-8 -*-
"""
:Authors: cykooz
:Date: 25.06.2015
"""
import os
import sys

from setuptools import find_packages, setup


HERE = os.path.abspath(os.path.dirname(__file__))
sys.path.append(HERE)

import version


README = open(os.path.join(HERE, 'README.rst'), 'rt').read()
CHANGES = open(os.path.join(HERE, 'CHANGES.rst'), 'rt').read()


def cli_cmd(app_name, command_name, func_name=None):
    func_name = func_name or command_name
    tpl = '{cmd} = cykooz.testing.{app}.commands.{cmd}:{func}.cli'
    return tpl.format(cmd=command_name, app=app_name, func=func_name)


setup(
    name='cykooz.testing',
    version=version.get_version(),
    description='Collection of helper utilities for testing.',
    long_description=README + '\n\n' + CHANGES,
    long_description_content_type='text/x-rst',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Testing',
        'License :: OSI Approved :: MIT License',
    ],
    keywords='',
    author='Cykooz',
    author_email='cykooz@gmail.com',
    url='https://github.com/Cykooz/cykooz.testing',
    package_dir={'': '.'},
    packages=find_packages(),
    namespace_packages=['cykooz'],
    include_package_data=True,
    package_data={},
    zip_safe=False,
    extras_require={
        'test': [
            'pytest',
        ],
    },
    install_requires=[
        'setuptools',
        'six',
    ],
    entry_points={
        'console_scripts':
            [
                'tests = cykooz.testing.runtests:runtests [test]',
            ]
    },
)
