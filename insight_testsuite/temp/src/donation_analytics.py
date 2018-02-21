#!/usr/bin/env python

"""donation_analytics.py: This file contains solution to determine repeat donors who contributed funds for political campaigns"""

__author__ = "Rajesh Kotecha" 
__copyright__ = "Copyright 2018, The Innovative Solutions"
__credits__ = ["Rajesh Kotecha", "Insight Data Engineering Team"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Rajesh Kotecha"
__email__ = "rkotecha 'at' gmail.com"
__status__ = "Production"

import sys
import math
from blist import sortedlist
import validations

def get_percentile_value (percentile_file):
    try:
        percentile_fp = open (percentile_file, 'r')
        firstline = percentile_fp.readline()
        percentile_value = int(firstline)

    except IOError:
        print ("Unable to open or read from file " + percentile_file)
        raise
    except ValueError:
        print ("Invalid percentile value in file " + percentile_file)
        raise
    else:
        percentile_fp.close()
        return percentile_value


def get_percentile_rank(percentile_val, amt_count):
#   To know more details about the formula to calculate Percentile Rank
#   please visit https://en.wikipedia.org/wiki/Percentile 
    index_value = int(math.ceil((percentile_val/100.0)*amt_count) - 1)
    return index_value


def get_year_from_date (date_mmddyyyy):
    return (int(date_mmddyyyy[4:]))


def get_rounded_amt (transaction_amt):
#   Business rule: If the amount is less than 50 cents ignore it, else
#                  round it to the next dollar amount. 
    if (transaction_amt < 0.50):
       return 0
    else:
       return (int(math.ceil(transaction_amt)))


def write_to_op_file (donana_op_fp, percentile, 
                      cmte_id, zip_code, 
                      year, politicians_dict):
    percentile_index = get_percentile_rank(percentile, 
                       politicians_dict[(cmte_id, zip_code, year)][0])
    percentile_amt = politicians_dict[(cmte_id, zip_code, year)][2][percentile_index]
    total_amt = politicians_dict[cmte_id, zip_code, year][1]
    count_amt = politicians_dict[cmte_id, zip_code, year][0]
    op_record = (cmte_id + '|' + 
                 zip_code + '|' +
                 str(year) + '|' +
                 str(percentile_amt) + '|' +
                 str(total_amt) + '|' +
                 str(count_amt) + '\n')
    try:
        donana_op_fp.write(op_record)
    except IOError: 
        print ("Unable to write following record to the output file:\n" + 
               "cmte_id = " + cmte_id + "\n" +
               "zip_code = " + zip_code + "\n" +
               "year = " + str(year) + "\n")
        return False
    else:
        return True
    


def process_donations(cont_ip_fp, percentile, donana_op_fp):
    donors_dict = {} # Hashmap containing donors. 
                     # Key is donor name and zip code.
                     # Value is the earliest year the donor contributed to
                     # any campaign.
    politicians_dict = {} # Hashmap containing donation recipients.
                          # Key is recipient id, zip code and year.
                          # Value is running total number of donation, 
                          #       running total donation amount, and
                          #       sorted binary tree list containing individual
                          #       donation amounts. 
    for line in cont_ip_fp:
        fields = line.split('|')
        cmte_id = fields[0]
        name = fields[7]
        zip_code = fields[10][:5] # Need first five characters
        transaction_dt = fields[13]
        try:
            transaction_amt = float(fields[14])
        except ValueError:
            continue
        other_id = fields[15]

        if (not validations.record_is_valid (other_id, transaction_dt, zip_code,
                     name, cmte_id, transaction_amt)): 
            continue

        year = get_year_from_date(transaction_dt)

        if ((name, zip_code) in donors_dict):
            if (donors_dict[(name, zip_code)] >= year):
                # This donation is out of order chronologically, 
                # so we update the year in the donors hashmap and move on. 
                donors_dict[(name, zip_code)] = year
                continue
        else:
            # This donor is encountered for the first time, so we just add
            # him in the donors hashmap and move on. 
            donors_dict[(name, zip_code)] = year
            continue

        # Now it is guaranteed that the donor is a repeat donor, so we
        # add the donation details in the politicians hashmap and also
        # write to the output file. 
        amt_rounded = get_rounded_amt(transaction_amt)
        if ((cmte_id, zip_code, year) in politicians_dict):
            if (amt_rounded <> 0):
                politicians_dict[(cmte_id, zip_code, year)][0] += 1
                politicians_dict[(cmte_id, zip_code, year)][1] += amt_rounded
                politicians_dict[(cmte_id, zip_code, year)][2].add(amt_rounded)
        else:
            politicians_dict[(cmte_id, zip_code, year)] = [1, amt_rounded, sortedlist([amt_rounded])]
     
        if (not write_to_op_file (donana_op_fp, percentile, 
                                  cmte_id, zip_code, 
                                  year, politicians_dict)):
            return False
                          
    return True


def donation_analytics (debug=False):

    if (not validations.usage_is_valid(sys.argv)):
        sys.exit(1)
    cont_ip_fn = sys.argv[1]
    percentile_ip_fn = sys.argv[2]
    donana_op_fn = sys.argv[3]
    
    percentile = get_percentile_value(percentile_ip_fn)
    if (not validations.percentile_is_valid(percentile)):
        print ("The percentile value in " + percentile_ip_fn + 
               " must be between 1 and 100 inclusive.")
        sys.exit(1)

    try:
        cont_ip_fp = open(cont_ip_fn, 'r')
    except IOError:
        print ("Unable to open " + cont_ip_fn)
        sys.exit(1)

    try:
        donana_op_fp = open(donana_op_fn, 'w')
    except IOError:
        cont_ip_fp.close()
        print ("Unable to open " + donana_op_fn)
        sys.exit(1)
    
    if (not process_donations(cont_ip_fp, percentile, donana_op_fp)):
        print ("Error occurred while processing donations.")
        cont_ip_fp.close()
        donana_op_fp.close()
        sys.exit(1)

    cont_ip_fp.close()
    donana_op_fp.close()
    sys.exit (0)


if __name__ == '__main__':
    donation_analytics (debug=False)

