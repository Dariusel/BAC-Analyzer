from setuptools import setup, find_packages

setup(
    name='bac-analyzer',
    version='0.1',
    packages=find_packages(),
    python_requires='>=3.12',
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'bac-analyzer = bac_analyzer.main:main',
        ],
    },
)