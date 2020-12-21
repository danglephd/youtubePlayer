import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ytplayer-pkg_DANGO", # Replace with your own username
    version="0.0.3",
    author="Mr Dango",
    author_email="danglephd@gmail.com",
    description="A Youtube player server Ad-Free",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/danglephd/youtubePlayer.git",
    packages=['ytplayer_pkg'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "pafy == 0.5.5",
    ],
    python_requires='>=3.6',
)