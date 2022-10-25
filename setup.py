import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='shellformatter',  
     version='0.1',
     scripts=['shellformatter'] ,
     author="Eth0",
     author_email="e@eth0.re",
     description="Convert binary shellcode into various formats",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/eth0-re/shellcode-formatter",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )