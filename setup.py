from setuptools import setup, find_packages

setup(
    name='BAC Analyzer',
    version='0.1',
    packages=find_packages(),
    python_requires='>=3.12',
    entry_points={
        'console_scripts': [
            'bac-analyzer = bac_analyzer.main:main',
        ],
    },
)