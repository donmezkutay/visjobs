import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="visjobs", # Replace with your own username
    version="0.0.1",
    author="Kutay Donmez",
    author_email="donmezk@outlook.com",
    description="Get Latest Atmospheric Model Data | Analyse | Visualize Easily",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/donmezkutay/visjobs",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
