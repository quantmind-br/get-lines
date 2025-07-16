from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="get-lines",
    version="1.0.0",
    author="Get Lines",
    author_email="",
    description="A tool to analyze code files and count lines in your project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/get-lines",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.7",
    install_requires=[
        "rich>=10.0.0",
        "chardet>=4.0.0",
        "pathspec>=0.9.0",
    ],
    entry_points={
        "console_scripts": [
            "get-lines=get_lines.main:main",
        ],
    },
)