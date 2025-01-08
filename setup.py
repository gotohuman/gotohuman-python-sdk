from pathlib import Path
from setuptools import find_packages, setup
import re

this_directory = Path(__file__).parent
long_description_mkd = (this_directory / "README.md").read_text()

init_path = Path("gotohuman/_version.py").resolve()
with open(init_path) as f:
    version = re.search(r"__version__ = ['\"]([^'\"]+)['\"]", f.read()).group(1)

setup(
    name='gotohuman',
    packages=find_packages(exclude=['img']),
    version=version,
    description='Python SDK for gotoHuman',
    long_description=long_description_mkd,
    long_description_content_type="text/markdown",
    keywords="gotohuman ai agents llm automation human-in-the-loop",
    url="https://gotohuman.com",
    project_urls={
        "Documentation": "https://docs.gotohuman.com/",
        "Twitter": "https://twitter.com/gotohuman",
    },
    author='gotoHuman',
    author_email='founders@gotohuman.com',
    install_requires=[
      'requests'
    ],
    python_requires=">=3.8",
    license="MIT"
)