
import io

from setuptools import find_packages, setup

with io.open('README.md', 'rt', encoding='utf8') as f:
    readme = f.read()

setup(
    name='requester',
    version='1.0.0',
    url='http://',
    license='BSD',
    maintainer='Onwuka Gideon',
    maintainer_email='dongidomed@gmail.com',
    description='A feature request app',
    long_description=readme,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
    extras_require={
        'test': [
            'pytest',
            'coverage',
        ],
    },
)