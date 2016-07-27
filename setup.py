
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()


setup(
    name='vivo-maintenance-queries',
    version='0.1',
    packages=find_packages(),
    install_requires=required,
    include_package_data=True,
    entry_points='''
        [console_scripts]
        vmaintq=vmaintq.command:main
    ''',
)
