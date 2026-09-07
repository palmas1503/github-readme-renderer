"""
Setup configuration for GitHub README Renderer
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="github-readme-renderer",
    version="2.0.0",
    author="palmas1503",
    description="Flask application to render GitHub README files as HTML with webhook support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/palmas1503/github-readme-renderer",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Flask",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "Flask>=2.3.0",
        "httpx>=0.24.0",
        "python-dotenv>=1.0.0",
        "gunicorn>=20.1.0",
        "markdown>=3.4.0",
        "Pygments>=2.16.0",
        "requests>=2.31.0",
    ],
    entry_points={
        "console_scripts": [
            "github-readme-renderer=app:app",
        ],
    },
)
