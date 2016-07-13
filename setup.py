#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'pylokit==0.8.1',
    'django>=1.9,<1.10',
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='templated_docs',
    version='0.2.5',
    description="Templated-docs generates templated documents in any format supported by LibreOffice",
    long_description=readme + '\n\n' + history,
    author="Alex Morozov",
    author_email='alex@morozov.ca',
    url='https://github.com/alexmorozov/templated-docs',
    packages=[
        'templated_docs',
    ],
    package_dir={'templated_docs':
                 'templated_docs'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='templated_docs',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests.test_app.tests',
    tests_require=test_requirements
)
