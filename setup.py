import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="snakecat",
    version="0.1.100",
    author="Alexey Mironov",
    author_email="amironov73@gmail.com",
    description="ctypes wrapper for irbis64_client.dll",
    keywords='IRBIS64',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amironov73/python_wrapper",
    packages=setuptools.find_packages(),
    classifiers=(
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ),
)
