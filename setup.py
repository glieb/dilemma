from setuptools import setup, find_packages

setup(
        name="PrisonerEconomy",
        version="0.2",
        packages=find_packages(),
        install_requires="attrs",
        package_data={
            "": "config.ini"
            }
     )
