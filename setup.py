"""A setuptools based setup module."""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pyserialem',  # Required
    version='0.1.0',  # Required
    description='Python module to read/write SerialEM .nav files.',  
    long_description=long_description,  
    long_description_content_type='text/markdown',  
    url='https://github.com/stefsmeets/pyserialem',  
    author='Stef Smeets',  
    author_email='s.smeets@tudelft.nl',  
    classifiers=[  
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GPLv3 License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='serialem electron-microscopy navigator',  
    # package_dir={'': 'src'},  
    packages=find_packages(where='.'),  # Required
    python_requires='>=3.6',
    install_requires=['matplotlib',
                'numpy',
                'matplotlib',
                ],  
    # extras_require={  
    #     'dev': ['check-manifest'],
    #     'test': ['coverage'],
    # },
    # package_data={  
    #     'sample': ['package_data.dat'],
    # },
    # data_files=[('my_data', ['data/data_file'])],  

    # entry_points={  
    #     'console_scripts': [
    #         'pyserialem=pyserialem:main',
    #     ],
    # },
    project_urls={  
        'Bug Reports': 'https://github.com/stefsmeets/pyserialem/issues',
        'Source': 'https://github.com/stefsmeets/pyserialem/',
    },
)
