import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ytplayer-pkg-DANGO", # Replace with your own username
    version="0.0.1",
    author="Mr Dango",
    author_email="danglephd@gmail.com",
    description="A Youtube player server Ad-Free",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/danglephd/youtubePlayer.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)