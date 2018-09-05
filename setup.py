#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'pylokit==0.8.1',
    'django>=1.8,<1.11',
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='templateddocs',
    version='0.3.2',
    description=('Generate PDF, MS Word and Excel documents from templates '
                 'in Django.'),
    long_description=readme + '\n\n' + history,
    author="Sian Lerk Lau",
    author_email='kiawin@gmail.com',
    url='https://github.com/kiawin/templated-docs',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='templateddocs',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    test_suite='tests.test_app.tests',
    tests_require=test_requirements
)
