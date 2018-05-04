from setuptools import setup, find_packages

setup(
        name="dilemma",
        version="0.2",
        packages=find_packages(),
        install_requires="attrs",
        package_data={
            "": "config.ini"
            }
     )
