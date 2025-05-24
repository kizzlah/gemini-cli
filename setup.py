kbc
kizzlah@icloud.com
github: kizzlah
-------------------
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="gemini-cli",
    version="0.1.0",
    author="",
    author_email="",
    description="A command-line interface for interacting with Google's Gemini AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/gemini-cli",
    packages=find_packages(),
    py_modules=["gemini_cli"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "gemini-cli=gemini_cli:main",
        ],
    },
)

