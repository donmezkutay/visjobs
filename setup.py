import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="visjobs", # Replace with your own username
    version="0.0.12",
    author="Kutay Donmez & Berkay Donmez",
    author_email="donmezk@outlook.com",
    description="Get The Latest Atmospheric Model Data | Analyse | Visualize Easily",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/donmezkutay/visjobs",
    packages=setuptools.find_packages(),
    install_requires=[
        "xarray",
        "pydap",
        "twine",
        "siphon",
        "pandas",
        "numpy",
        "matplotlib",
        "cartopy",
        "datetime"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
