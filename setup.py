from setuptools import setup, find_packages
from typing import List

def get_requirements() -> List[str]:
    """
    this function will return list of requirement

    """
    requirements: List[str] = []
    try:
        with open('requirements.txt') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if line and line!='-e .':
                    requirements.append(line)

        return requirements
    except FileNotFoundError as e:
        print("requirements.txt not found")


setup(
    name='NetworkSecurity',
    version='0.0.1',
    author='Sarvjeet',
    author_email='jha.sarvjeet1@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements(),

)
