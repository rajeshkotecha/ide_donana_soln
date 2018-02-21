# Table of Contents
1. [Introduction](README.md#introduction)
1. [Setup Instructions](README.md#setup-instructions)
1. [Data Structures](README.md#data-structures)
1. [Algorithm](README.md#Algorithm)

# Introduction
This repository contains the solution for political candidates to help analyze loyalty trends in campaign contributions. It identifies repeat donors in various geographies and calculates the donation figures and frequency of donations. 

# Setup Instructions
The solution is developed using Python 2.6 on Linux operating system and requires **blist** package. Below are the details - 

Instructions to download and install blist package on \*nix OS -

$ su - root

$ wget https://pypi.python.org/packages/6b/a8/dca5224abe81ccf8db81f8a2ca3d63e7a5fa7a86adc198d4e268c67ce884/blist-1.3.6.tar.gz

$ tar xvzf blist-1.3.6.tar.gz

$ cd blist-1.3.6

\# *Install the blist package in 'site-packages' directory of Python installation -*

$ python setup.py install

\# *Verify the correct installation and functioning of the package*
\# *The tests require Python 2.5, 2.6, 2.7, 3, 3.1 or 3.2.*

$ python setup.py test

$ cd ..

\# *Cleanup the installation file and directory -*
$ rm -f blist-1.3.6.tar.gz 

$ rm -rf blist-1.3.6/

$ exit


# Data Structures
## Summary
The solution is implemented using two types of data structures - **hash map** and **B-tree**. Hash map is implemented using Python dictionary type and B-tree using Python blist type. Python package **blist** uses Order Statistic B-tree to implement lists with fast insertion at arbitrary location. It also has very efficient retrieval capability. 

The Python **blist** package also provides **sortedlist** type. It (**sortedlist**) provides the same implementation as **blist** but keeps the items on sorted order. Since calculating Percentage Rank requires values in ascending order the **sortedlist** type is the best choice. 

## Details
### Donor Hash Map
A campaign donor is uniquely identified using his name and zip code. The donors list is stored in a hash map implemented as a Python dictionary named **donors\_dict**. Its key is a tuple containing donor's name and zip code. Its value is the earliest year in which the donor contributed to any political campaign. Since we are storing the earliest year in which the donor contributed to any political campaign it helps in determining whether he is a repeat donor. 

```
donors_dict = {(donor name, zip code):earliest donation year}
```

### Receiver Hash Map

```
politicians_dict = {(receiver id, zip code, donation year):(donation count, total donation amount, (donation amount1, donation amount2, donation amount3, ...)}
```

# Algorithm

