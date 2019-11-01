Arg-lys sequence

Finds the location of stretches containing only arginines and/or lysines in a protein, and the order of K and R does not matter.

Usage:

python arg_lys_sequence.py -F proteome.fasta -O output.csv -N 6 -P 999999 -I 0

-F [required]: Fasta archive containing proteins list

-O [required]: Output file in csv format

-N [required]: Insert wanted number of arginines or lysines

-P [optional]: Position of the last amino acid of each protein to be searched for

-I [optional]: Position of the last amino acid of each protein to be searched for
