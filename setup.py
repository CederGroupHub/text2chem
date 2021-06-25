from setuptools import setup, find_packages

setup(
    name='text2chem',
    packages=find_packages(),
    version='0.0.1',
    author='Ceder Research Group',
    author_email='cedergroup-ml-team@lbl.gov',
    description='RegEx-based text parser that converts chemical terms and material entities into chemical datastructure.',
    zip_safe=False,
    install_requires=[
        "regex",
        "pubchempy",
        "sympy"
    ],
    include_package_data=True
)
