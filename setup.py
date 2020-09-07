import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="g-sheets-tools-afriedman412", # Replace with your own username
    version="0.0.1",
    author="Andy Friedman",
    author_email="afriedman412@gmail.com",
    description="Convenience wrapper for Google Sheets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)