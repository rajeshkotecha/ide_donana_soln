"""validations.py: This file contains functions to validate various data values according to business rules mentioned in the requirements"""

__author__ = "Rajesh Kotecha"
__copyright__ = "Copyright 2018, The Innovative Solutions"
__credits__ = ["Rajesh Kotecha", "Insight Data Engineering Team"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Rajesh Kotecha"
__email__ = "rkotecha 'at' gmail.com"
__status__ = "Production"


import datetime
import re

def usage_is_valid(args):
    if (len (args) != 4): 
        print ("Usage: python " + 
               args[0] +
               " <InputFile-Donations>" +
               " <InputFile-Percentile>" +
               " <OutputFIle-RepeatDonors>")
        usage = False
    else: 
        usage = True
    return usage
    

def date_is_valid(date_mmddyyyy):
    valid_date = None

#   Date is invalid if it does not contain exactly 8 characters
    if (len(date_mmddyyyy) != 8):
        valid_date = False
        return valid_date
   
#   Date is invalid if it contains a non-numeric character 
    try: 
        year = int(date_mmddyyyy[4:])
        month = int(date_mmddyyyy[:2])
        day = int(date_mmddyyyy[2:4])
    except ValueError:
        valid_date = False
        return valid_date
    
#   Date is invalid if either year, month or day is invalid
    try:
        create_date = datetime.datetime(year, month, day)
        valid_date = True
    except ValueError:
        valid_date = False

    return valid_date


def zip_is_valid(zip_code):
    valid_zip_code = None

#   If zip is null or contains less than 5 characters it is not valid. 
    if (len(zip_code) < 5):
        valid_zip_code = False
    else:
        valid_zip_code = True

    return valid_zip_code
   
def name_is_valid(name):
#   name must contain "<LASTNAME>, <FIRSTNAME>" followed by initials which are optional 
    if (re.match('[A-Z \']*, [A-Z \.,]*$', name)):
        return True
    else:
        return False

def donor_is_indiv_contri(other_id):
    if (not other_id):
        return True
    else:
        return False

def trans_amt_is_valid(amt):
    if (amt):
        return True
    else:
        return False

def recipient_is_valid(recipient_id):
    if (recipient_id):
        return True
    else:
        return False

def percentile_is_valid(percentile_val):
    if ((percentile_val < 1) or (percentile_val > 100)):
        return False
    else:
        return True

def record_is_valid (other_id, transaction_dt, zip_code, 
                     name, cmte_id, transaction_amt):
    if (donor_is_indiv_contri(other_id) and
        date_is_valid(transaction_dt) and
        zip_is_valid(zip_code) and
        name_is_valid(name) and
        recipient_is_valid(cmte_id) and
        trans_amt_is_valid(transaction_amt)):
        return True
    else:
        return False

