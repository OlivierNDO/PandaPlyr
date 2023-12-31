from setuptools import setup, find_packages

setup(
    name="PandaPlyr",
    version="0.1.8",
    author="Nick Olivier",
    author_email="Olivier_N@lynchburg.edu",
    description="The purpose of PandaPlyr is to make chained operations on pandas DataFrames easier and more readable.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/OlivierNDO/PandaPlyr/",
    packages=['PandaPlyr'],
    package_dir={'PandaPlyr': 'src'},
    package_data={'PandaPlyr': ['data/*.csv']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'numpy',
        'pandas',
    ],
    python_requires='>=3.6',
)
