from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in next_store/__init__.py
from next_store import __version__ as version

setup(
	name="next_store",
	version=version,
	description="Next",
	author="Next",
	author_email="Next",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
