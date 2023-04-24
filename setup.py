from setuptools import setup, find_packages

setup(
    name='tio-config',
    version='0.1.0',
    packages=find_packages(where='tio-config'),
    include_package_data=True,
    package_dir={"": "tio-config"},

    install_requires=[
        'Click',
        'pyTenable',
        'python-dotenv',
        'pandas', 
        'pydantic',
        'openpyxl'

    ],
    entry_points={
        'console_scripts': [
            'tio-config = cli:cli',
        ],
    },
)