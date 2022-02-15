#!/usr/bin/python3
# encoding: utf-8

from setuptools import setup
setup(
    name="sugar_shell",
    version='0.1',
    author="mikusugar",
    author_email="syfangjie@live.cn",
    url="https://github.com/MikuSugar/SugarShell",
    description="ssh tools",
    packages=['sugar_shell'],
    include_package_data=True,
    platforms="any",
    install_requires=[],
    entry_points={
        'console_scripts': [
            'psh=sugar_shell:ssh_helper'
        ]
    }
)