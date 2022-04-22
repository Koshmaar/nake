import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='nake',
    version='0.0.1',
    author='Hubert "Koshmaar" Rutkowski',
    author_email='do.not@email.me',
    description="nifty nool for nunning scripts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Information Technology',
    ],
    python_requires='>=3.5.0',
    dependency_links=[],
    install_requires=[],
    license='MIT',
    entry_points={
        "console_scripts": [
            "nake = main:main",
        ],
    },
)


