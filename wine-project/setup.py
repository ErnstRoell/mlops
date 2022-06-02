from setuptools import find_packages, setup
from wine_project import __version__

setup(
    name="wine_project",
    packages=find_packages(exclude=["tests", "tests.*"]),
    setup_requires=["wheel"],
    version=__version__,
    description="",
    author=""
)
