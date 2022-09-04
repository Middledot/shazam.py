import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()


setuptools.setup(
    name="shazam.py",
    version="1.0.0a",
    license="MIT",
    author="Middledot",
    author_email="middledot.productions@gmail.com",
    description="Fully reverse engeenired shazam api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Numenorean/ShazamAPI",
    install_requires=requirements,
    packages=["shazam"],
    python_requires='>=3.6',
    project_urls={
        #"Documentation": "https://shazampy.readthedocs.io/en/latest/",  # TODO:
        "Issue Tracker": "https://github.com/Middledot/shazam.py/issues",
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        # 'Typing :: Typed',
    ]
)
