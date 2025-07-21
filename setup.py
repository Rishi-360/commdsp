from setuptools import setup, find_packages

setup(
    name='commdsp',  # The name of your top-level package
    version='0.1.0', # Start with a basic version number
    packages=find_packages(), # Automatically find all packages (folders with __init__.py)
    # more metadata here later if you want:
    # author='Your Name',
    # author_email='your.email@example.com',
    # description='A simple communication and DSP library',
    # url='https://github.com/yourusername/commdsp',
    # install_requires=[ # These should also be in requirements.txt
    #     'numpy',
    #     'scipy',
    #     'matplotlib',
    #     'sympy',
    # ],
)