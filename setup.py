from importlib.metadata import entry_points
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='ShellcodeFormatter',
     version='1.0.3',
     author="Eth0",
     author_email="e@eth0.re",
     description="Transform binary shellcode into various formats",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/eth0-re/ShellcodeFormatter",
     download_url="https://github.com/eth0-re/ShellcodeFormatter/archive/refs/tags/v1.0.3.tar.gz",
     packages=['ShellcodeFormatter'],
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
     entry_points={'console_scripts': ['ShellcodeFormatter = ShellcodeFormatter.ShellcodeFormatter:main']},
 )