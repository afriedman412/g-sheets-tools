import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="g-sheets-tools",
    version="0.0.8",
    author="Andy Friedman",
    author_email="afriedman412@gmail.com",
    description="Easy wrapper for the Google Sheets API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/afriedman412/g-sheets-tools",
    install_requires=[
        'cachetools==4.1.1',
        'certifi==2020.6.20',
        'chardet==3.0.4',
        'google-api-core==1.22.2',
        'google-api-python-client==1.11.0',
        'google-auth==1.21.1',
        'google-auth-httplib2==0.0.4',
        'google-auth-oauthlib==0.4.1',
        'googleapis-common-protos==1.52.0',
        'httplib2==0.18.1',
        'idna==2.10',
        'numpy<1.19.0',
        'oauthlib==3.1.0',
        'pandas==0.24',
        'protobuf==3.13.0',
        'pyasn1==0.4.8',
        'pyasn1-modules==0.2.8',
        'python-dateutil==2.8.1',
        'pytz==2020.1',
        'requests==2.24.0',
        'requests-oauthlib==1.3.0',
        'setuptools>=40.3',
        'rsa==4.6',
        'six==1.15.0',
        'uritemplate==3.0.1',
        'urllib3==1.25.10'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)