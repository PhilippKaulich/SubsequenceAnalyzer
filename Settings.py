# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 17:28:37 2023

@author: Phili
"""

class Settings:
    
    
    about = """
        Cleavage Analysis TDP
        v.2.0.0 (January, 2023)
        by Philipp T. Kaulich 
        
        Manual: -
        Contact: p.kaulich@iem.uni-kiel.de        
        """
    
    
    aa_list = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 
                    'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
    not_cleaved = "not_cleaved"
    cleaved = "cleaved"
    proteoform_level = ""
    prsm_level = ""
    
    
    
    
    
    ### GUI ###
    gui_title = "Subsequence Analyzer"
    fasta_file_filter = 'Fasta file (*.fasta);; All Files (*)'
    fasta_initialFilter = 'Fasta file (*.fasta)'
    proteoform_file_filter = 'txt file (*.txt);; csv file (*.csv);; All Files (*)'
    proteoform_initialFilter = 'txt file (*.txt)'
    
    database_prosight = "ProSight PD"
    database_toppic = "TopPic"
    database_sequencelist = "Sequence list"
    
    database_sequence = "Sequence"
    database_prsms = "#PrSMs"
    
    
    export_file_filter = 'csv file (*.csv);; All Files (*)'
    export_initialFilter = 'csv file (*.csv)'