import sys
import argparse
import os

parser = argparse.ArgumentParser(description='Search for arginines or lysines in a roll.', usage='[options]')
parser.add_argument('-F', '--fasta', type=str, required=True, help='fasta archive containing proteins list')
parser.add_argument('-O', '--output', type=str, required=True, help='output file (csv format)')
parser.add_argument('-N', '--number', type=int, required=True, help='Insert wanted number of arginines or lysines')
parser.add_argument('-P', '--finalpos', type=int, default=999999, help='Position of the last aminoacid of each gene to be searched for')
parser.add_argument('-I', '--initialpos', type=int, default=0, help='Position of the last aminoacid of each gene to be searched for')
args = parser.parse_args()

def percent(index, genome_length): # Iterface updating the percentage of the ORFs read
	percentage = 100*index/genome_length
	interface = int(percentage)
	print str(interface) + '% complete\r',
import sys

def get_aa(nt1, nt2, nt3):

	if nt1 == 'C' and nt2 == 'G':
		return True

	if nt1 == 'A':
		if nt2 == 'A' or nt2 == 'G':
			if nt3 == 'A' or nt3 == 'G':
				return True

	return False

################################################################################################

def evaluate(prote, fout, prot_name):
	charge = 0
	sequence = False
	#for each character (does not include the last field size characteres)

	end_pos = len(prote)/3
	if end_pos > args.finalpos:
		end_pos = args.finalpos

	if args.initialpos > end_pos:
		return

	for i in range(args.initialpos, end_pos):

		nt1 = prote[i*3]
		nt2 = prote[i*3 + 1]
		nt3 = prote[i*3 + 2]
		RorK = get_aa(nt1, nt2, nt3)

		if RorK == True:
			charge += 1
			if charge == 1:
				beginning = i*3+1
			
		else:
			if sequence == True:
				fout.write(str(charge))
				sequence = False
			charge = 0

		if charge >= args.number:
			if sequence == False:
				relative = float(i) / float(len(prote))
				fout.write("\n" + str(prot_name) + ";" + str(beginning) + ";" + str(relative) + ';')
				sequence = True

	if sequence == True:
		fout.write(str(charge))

	return



###################################################################################
def main():
	file_in = open(args.fasta, 'r') # Input file
	in_file = file_in.read()

	out_file = open(args.output, 'w') # Output file
	
	actual_path = os.getcwd() # Get file path
	
	header_basic = 'Search for arginines or lysines in a roll.\n'
	header_fasta = 'fasta file:;' + actual_path + '/' + args.fasta + '\n' # Prepare fasta path
	header_difference = 'number of R/K wanted:;' + str(args.number) + '\n'
	header_gene_stretch = 'position of aminoacids in gene:;' + str(args.initialpos) + ' - ' + str(args.finalpos) + '\n\n\n\n\n\n'
	header_data = 'name;position (in nucleotides);relative position;length'
	
	file_header = header_basic + header_fasta + header_difference + header_gene_stretch + header_data # Build header without difference value
	out_file.write(file_header+'\n') # Write header

	proteome_list = in_file.replace('>UniRef100_','>')
	proteome_list = str.split(in_file, '>') # Split genes by '>'

	for i in range(len(proteome_list)): # Repeat for each gene
		percent(i, (len(proteome_list)))

		protein_code = ''

		proteome_list[i] = proteome_list[i].replace('\r', '')
		protein_by_line = str.split(proteome_list[i], '\n') # Split each line
		header = protein_by_line[0] # The first line is the header
		name = str.split(header,' ')[0]
		for j in range(1, len(protein_by_line)):
			protein_code += protein_by_line[j] # Every line (except the first) is part of the code

		protein_aminoacids = list(protein_code) # List of all aminoacids in a gene
		evaluate(protein_aminoacids, out_file, name)
	print '\r100% complete!'

main()