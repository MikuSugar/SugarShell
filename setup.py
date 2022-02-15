#!/usr/bin/python3
# encoding: utf-8

from setuptools import setup
setup(
    name="sugar_shell",
    version='0.2.1',
    author="mikusugar",
    author_email="syfangjie@live.cn",
    url="https://github.com/MikuSugar/SugarShell",
    description="ssh tools",
    packages=['sugar_shell'],
    include_package_data=True,
    platforms="any",
    install_requires=[],
    python_requires='>=3',
    entry_points={
        'console_scripts': [
            'psh=sugar_shell:ssh_helper'
        ]
    }
)