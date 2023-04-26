from setuptools import setup, find_packages

setup(
    name='tio-config',
    version='0.1.0',
    package_dir={"": "tio-config"},

    install_requires=[
        'Click', 
        'click_pathlib'
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
