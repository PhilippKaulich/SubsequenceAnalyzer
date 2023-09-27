# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 10:09:40 2022

@author: Philipp
"""


from Bio import SeqIO
import ProteomicTools
from Settings import Settings


class ReadFastaFile:
    def __init__(self):
        pass   
    
    
    def read_fasta_file(self, fasta_file: str) -> dict:
        """ """
        fasta_sequences = SeqIO.parse(open(fasta_file), 'fasta')
        fasta_dict = {}
        for fasta in fasta_sequences:
            name, sequence = fasta.id, str(fasta.seq)
            if not all(substring  in Settings.aa_list for substring in sequence):
                continue
            try:
                accession = name.split("|")[1]
                fasta_dict[accession] = sequence
            except:
                print("A problem occured with the fasta entry", fasta)
                fasta_dict[name] = sequence
        print("Loaded Fasta file", fasta_file)
        return fasta_dict

    def find_sequence(self, fasta_dict: dict, seq: str) -> str:
        acc_list = []
        for acc in fasta_dict:
            if seq in fasta_dict[acc]:
                acc_list.append(acc)
        return acc_list 
                
    
    def find_protein(self, fasta_dict: dict, accession: str) -> str:
        return fasta_dict[accession]

            
    
    
# NICHT VOLLKOMMEN KORREKT
    def simulate_protease(self, fasta_dict, specifity):
        """ specifity zB DP -> between D and P """
        sequences = fasta_dict.values()
        all_peptides = []
        all_peptides_length = []
       #p = ProteomicTools.ProteomicTools()
        for seq in sequences:
            peptides = seq.split(specifity)
            print(peptides)
            all_peptides.extend(peptides)
            all_peptides_length.extend([len(i) for i in peptides])
            
        return all_peptides_length
            
            
            
    
    def number_of_proteins_filter(self, fasta_dict, filter_):
        i = 0
        p = ProteomicTools.ProteomicTools()
        for acc in fasta_dict:
            seq = fasta_dict[acc]
            mass = p.calculate_mass(seq)
            if mass < filter_:
                i += 1
        print("Number of proteins <", filter_, ": ", i)
        return i
    
    

# input_file = "Datasets\\IntactProteinStandard.fasta"
input_file = "Dataset\\20210709_Uniprot_Human_reviewed.fasta"


# f = ReadFastaFile()
# fasta = f.read_fasta_file(input_file)
# n = f.number_of_proteins_filter(fasta, 250_000)
# prots = f.find_sequence(fasta, "PHILI")
# seq = f.find_protein(fasta, "P00390")
# print(prots, seq)