import setuptools

setuptools.setup(
    name='NYPDpackage',
    version='1.00',
    license='BSD 2-clause',
    author='Stanisław Grodzki',
    author_email='sg406651@students.mimuw.edu.pl',
    packages=setuptools.find_packages(),
    install_requires=["pandas", "numpy", "openpyxl", "argparse"]
)
