from setuptools import setup, find_packages

setup(
    name="KuroTik",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "RouterOS-api"
    ],
    author="Kuro",
    author_email="kuro@kuronekosan.web.id",
    description="A Custom Mikrotik Packages for automatic enabled/disabled block script",
    url="https://github.com/SandyMaull/KuroTik",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12',
)