from setuptools import setup, find_packages

with open("README.md") as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    dependencies = f.read()
    install_requires = dependencies.split("\n")

setup(
    name="mileage",
    version="0.1.0",
    author="Matthieu Marshall",
    author_email="matthieu.marshall@gmail.com",
    description="Dashboard for my running mileage.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="running,mileage,dash,distance",
)
