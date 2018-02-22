# Table of Contents
1. [Introduction](README.md#introduction)
1. [Setup Instructions](README.md#setup-instructions)
1. [Data Structures](README.md#data-structures)
1. [Algorithm](README.md#Algorithm)

# Introduction
This repository contains the solution for political candidates to help analyze loyalty trends in campaign contributions. It identifies repeat donors in various geographies and calculates the donation figures and frequency of donations. 

# Setup Instructions
The solution is developed using **Python 2.6.6** on **Linux** operating system and requires **blist** package. Below are the details - 

Instructions to download and install **blist** package on \*nix OS -

```
$ su - root
```

```
$ wget https://pypi.python.org/packages/6b/a8/dca5224abe81ccf8db81f8a2ca3d63e7a5fa7a86adc198d4e268c67ce884/blist-1.3.6.tar.gz
```

```
$ tar xvzf blist-1.3.6.tar.gz
```

```
$ cd blist-1.3.6
```

\# *Install the blist package in 'site-packages' directory of Python installation -*

```
$ python setup.py install
```

\# *Verify the correct installation and functioning of the package. The tests require Python 2.5, 2.6, 2.7, 3, 3.1 or 3.2.*

```
$ python setup.py test
```

```
$ cd ..
```

\# *Cleanup the installation file and directory -*

```
$ rm -f blist-1.3.6.tar.gz 
```

```
$ rm -rf blist-1.3.6/
```

```
$ exit
```


# Data Structures
## Summary
The solution is implemented using two types of data structures - **hash map** and **B-tree**. Hash map is implemented using Python dictionary type and B-tree using Python blist type. Python package **blist** uses Order Statistic B-tree to implement lists with fast insertion at arbitrary location. It also has very efficient retrieval capability. 

The Python **blist** package also provides **sortedlist** type. It (**sortedlist**) provides the same implementation as **blist** but keeps the items on sorted order. Since calculating Percentage Rank requires values in ascending order the **sortedlist** type is the best choice. 

## Details
### Donor Hash Map
A campaign donor (or contributor) is uniquely identified using his name and zip code. The donors list is stored in a hash map implemented as a Python dictionary named **donors\_dict** in the code. Its key is a tuple containing donor's name and zip code. Its value is the earliest year in which the donor contributed to any political campaign. Since we are storing the earliest year in which the donor contributed to any political campaign it helps in determining whether he is a repeat donor when we encounter another donation made by the same contributor. 

```
donors_dict = {(donor name, zip code):earliest donation year}
```

### Receiver Hash Map
The politicians (or receivers) list is also stored in a hash map implemented as a Python dictionary named **politicians\_dict** in the code. Its key is a tuple containing receiver id, zip code and donation year. Its value is also a tuple containing running donation count, running total donation amount and a list of individual donation amounts sorted in ascending order. 

```
politicians_dict = {(receiver id, zip code, donation year):(donation count, total donation amt, 
                                                           [donation amt1, donation amt2, donation amt3, ...]}
```

# Algorithm

## Data Processing Steps -

  1) Read next record from the input (individual contributions) file. 
  2) If the donation is not from an individual or any business rule data validations fail \-
     - Skip the record. 
     - Go to step \#1. 
  3) Check if the contributor (name + zip) exists in the donors list \-  
     - If the contributor (name + zip) exists \- 
       - Check if the donation is in chronological order \-
         - If in chronological order \- 
           - Mark the current contributor as a _**repeat donor**_.
         - If not in chronological order \-
           - The record is in reverse chronological order.
           - Update the earliest year for the contributor to the current record's year in the donors list.
           - Go to step \#1. 
     - If the contributor (name + zip) does not exist,
       - Add the contributor (name + zip) and year to the donors list.
       - Go to step \#1.
  4) If the contributor (name + zip) is a _**repeat donor**_ \-
     - Check if the recipient exists in the politicians list \-
       - If exists \- 
         - Add 1 to the running donation count for this recipient, zip code and donation year. 
         - Add current contribution amount to the running donation total for this recipient, zip code and donation year. 
         - Add current contribution amount to the list of donation amounts for this recipient, zip code and donation year.
       - If does not exist \-
         - Add the recipient to the politicians list. Initialize the running donation count (to 1), running donation total (to the current donation amount)  and list of donation amounts (to a list containing the current donation amount).  
  5) Calculate the percentile rank using the standard formula. 
  6) Write the record with recipient details (ID, zip code and donation year), percentile rank of this contribution to the recipient, running donation count for this recipient, and running donation total for this recipient to the output file. 
  7) If end of input file reached, stop the processing.
  8) Go to step #1.
 
