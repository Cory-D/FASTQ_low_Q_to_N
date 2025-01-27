FASTQ_low_Q_to_N

----

Author:

Cory Dunn

Contact: cory.david.dunn@gmail.com

Provided courtesy of GRO Biosciences

----

License:

GPLv3

----

This script simply masks FASTQ characters below the set quality score as 'N'. This approach avoids discarding reads based upon average quality or other aggregate metrics.

----


Requirements:

This script is implemented in Python 3 (current version tested under Python version 3.13.1) 

----

Usage:

FASTQ_low_Q_to_N.py [-h] -i INPUT_FILE -o OUTPUT_FILE [-q MINIMUM_QUALITY_CUTOFF] [-z GZIP_FLAG]

  -i INPUT_FILE, --input_file
                        
	Input FASTQ (gzipped compressed or uncompressed detected by presence or absence of '.gz' file extension).

  -o OUTPUT_FILE, --output_file

	Output filename.

  -q MINIMUM_QUALITY_CUTOFF, --minimum_quality_cutoff

	Minimum quality score cutoff applied to all barcode bases (Default is 25).

  -z GZIP_FLAG, --gzip_flag

	Input and output are gzipped. Add 0-9, with 1-9 indicating output compression level. (Default = 0 [no compression]).