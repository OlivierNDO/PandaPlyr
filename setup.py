from setuptools import setup, find_packages

setup(
    name="PythonPlyr",
    version="0.0.1",
    author="Nick Olivier",
    author_email="Olivier_N@lynchburg.edu",
    description="The purpose of PyPlyr is to make chained operations on pandas DataFrames easier and more readable.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/OlivierNDO/PythonPlyr/",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'numpy',
        'os',
        'pandas',
        're'
    ],
    python_requires='>=3.6',
)
