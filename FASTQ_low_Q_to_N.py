#!/usr/bin/env python
# coding: utf-8

# Author: Cory Dunn
# Contact : cory.david.dunn@gmail.com
# Provided courtesy of GRO Biosciences

# Import the necessary libraries

import gzip
import argparse

# Collect input from user

ap = argparse.ArgumentParser()
ap.add_argument('-i','--input_file',required=True,type=str,help="Input FASTQ (gzipped compressed or uncompressed detected by presence or absence of '.gz' file extension).\n")
ap.add_argument('-o','--output_file',required=True,type=str,help="Output filename.\n")
ap.add_argument('-q','--minimum_quality_cutoff',required=False,type=int,default=25,help="Minimum quality score cutoff applied to all barcode bases (Default is 25).\n")
ap.add_argument('-z','--gzip_flag',required=False,default='0',type=int,help="Input and output are gzipped. Add 0-9, with 1-9 indicating output compression level. (Default = 0 [no compression]).\n")

args = vars(ap.parse_args())

# Set parameters

INPUT_FILENAME = args['input_file']
OUTPUT_FILENAME = args['output_file']
minimum_QS_cutoff = args['minimum_quality_cutoff']
compression_number = args['gzip_flag']

# Extract data from FASTQ file

def import_FASTQ_tags(inputfilename):

    if '.gz' in INPUT_FILENAME : 

        inputfile_F = gzip.open(inputfilename,'rt')

    else : 
    
        inputfile_F = open(inputfilename,'rt')

    list_of_identifiers = []
    list_of_FASTA_lines = []
    list_of_FASTQ_CHAR = []

    # Move through FASTQ entries and save FASTA and quality score for each read
    
    count = 1
    
    for line in inputfile_F:
        
        # Take from the ID line

        if count % 4 == 1:
        
            list_of_identifiers.append(line)

        # Take from the FASTA line
        
        elif count % 4 == 2:
            line_nonl = line.rstrip(line[-1])
            FASTA = line_nonl.upper()
            list_of_FASTA_lines.append(FASTA)

        # Take from the quality character line

        elif count % 4 == 0:
            
            line_nonl = line.rstrip(line[-1])
            QCHAR = line_nonl
            
            list_of_FASTQ_CHAR.append(QCHAR)

        count += 1
    
    inputfile_F.close()
    
    return(list_of_identifiers,list_of_FASTA_lines, list_of_FASTQ_CHAR)

# Check quality score and write new FASTA

def convert_to_N_low_Q(old_FASTA,Q):

    new_FASTA = ""

    for i in range(0, len(Q)):
        Q_convert = ord(str(Q[i]))-33
        if Q_convert < minimum_QS_cutoff:
            new_FASTA = new_FASTA + 'N'
        else: 
            new_FASTA = new_FASTA + old_FASTA[i]

    return new_FASTA

# Save new FASTQ 

if compression_number > 0 : 

    ofile = gzip.open(OUTPUT_FILENAME,'w', compresslevel=compression_number)

else : 

    ofile = open(OUTPUT_FILENAME, 'w')

ID_set, FASTA_set, Q_set = import_FASTQ_tags(INPUT_FILENAME)

new_FASTA_list = []

for j in range(0,len(FASTA_set)):

    converted = convert_to_N_low_Q(FASTA_set[j],Q_set[j])

    new_FASTA_list.append(converted)

for k in range(0,len(ID_set)):

    if compression_number > 0 : 

        ofile.write((ID_set[k].encode('utf-8')))
        ofile.write((new_FASTA_list[k]+'\n').encode('utf-8'))
        ofile.write(('+' + '\n').encode('utf-8'))
        ofile.write((Q_set[k]+'\n').encode('utf-8'))

    else : 

        ofile.write(ID_set[k])
        ofile.write(new_FASTA_list[k]+'\n')
        ofile.write('+' + '\n')
        ofile.write(Q_set[k]+'\n')
    
ofile.close()






