# -*- coding: utf-8 -*-
"""
Created on Sun Sep  5 20:41:57 2021

@author: Phili
"""

import pandas as pd
import sys
import pickle
from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtWidgets import QWidget, QFileDialog, QTextEdit, QVBoxLayout, QScrollArea

from collections import Counter

import AnalyzeCleavageSites
import ReadProteoforms
from Settings import Settings
from MyPlots import create_cleavage_site_plot, truncations_pi_chart, \
    plot_methionin_cleaveage, plot_methionin_cleavaege_absolut, subsequence_visualization


# enable scaling high DPI mode 
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True) 
# if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
#     QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

# if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
#     QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)



# fasta = "Dataset\\PTK_Ecoli_FASTA_all.fasta"
# a = AnalyzeCleavageSites(fasta)
# r = ReadProteoforms.ReadProteoforms(pd_version="v4.0")
# df = r.read_file("Dataset\\test_3_Proteoforms.txt")
# aa_df = a.find_subsequence_termini(df["Sequence"], df["# PrSMs"])



class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('GUI.ui', self)
        title = Settings.gui_title
        self.setWindowTitle(title)
        self.show()
        
        ###

        
    def load_fasta_file(self):
        file_filter = Settings.fasta_file_filter
        initialFilter = Settings.fasta_initialFilter
        self.fasta_file = QFileDialog.getOpenFileName(caption = 'Load Fasta File',
            directory = '', filter = file_filter, initialFilter = initialFilter)[0]
        self.text_fasta_file.setText(self.fasta_file.split("/")[-1])

        
    
    def load_proteoform_file(self):
        file_filter = Settings.proteoform_file_filter
        initialFilter = Settings.proteoform_initialFilter
        self.proteoform_file = QFileDialog.getOpenFileName(caption = 'Load Proteoform File',
            directory = '', filter = file_filter, initialFilter = initialFilter)[0]
        self.text_proteoform_file.setText(self.proteoform_file.split("/")[-1])
    
    
    def change_level(self):
        level = self.combobox_level.currentText()
        print(level)
    
    
    def initialization(self):
        level = self.combobox_level.currentText()
        a = AnalyzeCleavageSites.AnalyzeCleavageSites(self.fasta_file)
        r = ReadProteoforms.ReadProteoforms()
        database_search = self.combobox_search.currentText()
        if database_search == "ProSight PD":
            pd_version = self.combobox_pd_version.currentText()
            print("pd_version", pd_version)
            df = r.read_prosight_results(self.proteoform_file, pd_version=pd_version)
            proteoforms = df["Sequence"]
            prsms = df["# PrSMs"]
            annotated = list(df[r.annotated_confidence])
            subsequence = list(df[r.subsequence_confidence])
            
        elif database_search == "TopPic":
            df = r.read_toppic_results(self.proteoform_file)
            proteoforms = list(set(df["cleanSeq"]))
            prsms = [1 for i in df.index]
            subsequence = False
            annotated = False

        elif database_search == "Sequence list":
            df = r.read_sequence_list(self.proteoform_file)
            proteoforms = list(df["Sequence"])
            prsms = list(df["#PrSMs"])
            subsequence = False
            annotated = False
            
        self.potential_cleavage, self.accession_proteoforms, self.truncations, \
        self.met_cleav = \
                a.find_subsequence_termini(proteoforms, prsms, 
                                           subsequence, annotated, level)
                

 
        #### combobox
        all_accessions = self.accession_proteoforms.keys() 
        #number of proteoforms
        number_of_proteoforms = [len(self.accession_proteoforms[i][1]) for i \
                                 in self.accession_proteoforms]
        number_of_prsms = [sum([self.accession_proteoforms[seq][1][index][3] for \
                    index, _ in enumerate(self.accession_proteoforms[seq][1])]) \
                    for seq in self.accession_proteoforms]
        self.combo_accessions.clear()
        te = ["{}\t{}\t{}".format(acc, nproteoforms, nprsms) for acc, 
              nproteoforms, nprsms in zip(list(all_accessions), 
              number_of_proteoforms, number_of_prsms)]
        self.combo_accessions.addItems(te)
        
    
    def plot_potential_cleavage_site(self):
        create_cleavage_site_plot(self.potential_cleavage)
        print(self.potential_cleavage)
    
    
    def plot_truncations(self):
        print("Truncations", self.truncations)
        truncations_pi_chart(self.truncations)
        
        
        
    def analyze_met_cleavage(self, d):
        #d = {"notcleaved": [], "cleaved": []}
        absolut_cleaved_sum = {}
        notcleaved = Counter(d[Settings.not_cleaved])
        print("Number of not-cleaved Start-Methionins", len(d[Settings.not_cleaved]))
        cleaved = Counter(d[Settings.cleaved])
        print("Number of cleaved Start-Methionins", len(d[Settings.cleaved]))
        ration_cleaved_sum = {}
        print("AA\tCleaved\tNot-Cleaved")
        for aa in Settings.aa_list:
            if aa not in notcleaved and aa not in cleaved: continue
            if aa not in notcleaved: notcleaved[aa] = 0
            if aa not in cleaved: cleaved[aa] = 0
            absolut_cleaved_sum[aa] = [cleaved[aa], notcleaved[aa]]
            print(aa, cleaved[aa], "\t", notcleaved[aa])
            ration_cleaved_sum[aa] = cleaved[aa] / (cleaved[aa] + notcleaved[aa])
        return absolut_cleaved_sum, ration_cleaved_sum
        
        
        
    def plot_methionine_cleavage(self):
        ## Met cleaved
        met_cleav_absolut, met_cleav_ratio = self.analyze_met_cleavage(self.met_cleav)
        plot_methionin_cleaveage(met_cleav_ratio)
        plot_methionin_cleavaege_absolut(met_cleav_absolut)
    
    
    # def plot(self):
    #     level = self.combobox_level.currentText()
    #     a = AnalyzeCleavageSites.AnalyzeCleavageSites(self.fasta_file)
    #     r = ReadProteoforms.ReadProteoforms(pd_version="v4.0")
    #     database_search = self.combobox_search.currentText()
    #     if database_search == "ProSight PD":
    #         df = r.read_prosight_results(self.proteoform_file)
    #         self.potential_cleavage, self.accession_proteoforms, self.truncation = \
    #             a.find_subsequence_termini(df["Sequence"], df["# PrSMs"], level)
    #     elif database_search == "TopPic":
    #         df = r.read_toppic_results(self.proteoform_file)
    #         proteoforms = list(set(df["cleanSeq"]))
    #         self.potential_cleavage, self.accession_proteoforms, self.truncation = \
    #             a.find_subsequence_termini(proteoforms, [1 for i in df.index], level)
    #     elif database_search == "Sequence list":
    #         df = r.read_sequence_list(self.proteoform_file)
    #         proteoforms = list(df["Sequence"])
    #         prsms = list(df["#PrSMs"])
    #         self.potential_cleavage, self.accession_proteoforms, self.truncation = \
    #             a.find_subsequence_termini(proteoforms, prsms, level)
    #     #self.show_about()

    #     #### combobox
    #     all_accessions = self.accession_proteoforms.keys() #sorted(list(self.accession_proteoforms.keys()))
    #     #number of proteoforms
    #     number_of_proteoforms = [len(self.accession_proteoforms[i][1]) for i in self.accession_proteoforms]
    #     number_of_prsms = [sum([self.accession_proteoforms[seq][1][index][3] for index, _ in enumerate(self.accession_proteoforms[seq][1])]) for seq in self.accession_proteoforms]
    #     # for i in range(len(number_of_proteoforms)):
    #     #     print(list(all_accessions)[i], "MMMM", number_of_proteoforms[i], number_of_prsms[i])
    #     self.combo_accessions.clear()
    #     te = ["{}\t{}\t{}".format(acc, nproteoforms, nprsms) for acc, 
    #           nproteoforms, nprsms in zip(list(all_accessions), number_of_proteoforms, number_of_prsms)]
    #     self.combo_accessions.addItems(te)



    def database_analysis(self):
        a = AnalyzeCleavageSites.AnalyzeCleavageSites(self.fasta_file)
        a.analyze_aa_content_in_database()
        
        
        
        
    def analyze_accession(self):
        accession = self.combo_accessions.currentText().split("\t")[0]
        protein_sequence, ll = self.accession_proteoforms[accession]
        # print(accession, protein_length, ll)
        if len(ll) >1:
            subsequence_visualization(ll, protein_sequence, accession)
        


    def export_data(self):
        file_filter = Settings.export_file_filter
        initialFilter = Settings.export_initialFilter
        file_name = QFileDialog.getSaveFileName(caption = 'Save results as',
            directory = '', filter = file_filter, initialFilter = initialFilter)[0]
        self.potential_cleavage.to_csv(file_name)
        print(file_name, "erfolgerich gespeichert")
        
        

    def show_about(self):
        text = Settings.about
        self.w = ResultWindow()
        self.w.textedit.setText(text)
        self.w.show()


class ResultWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(640, 480)
        self.setWindowTitle("")
        layout = QVBoxLayout()
        self.textedit = QTextEdit()
        layout.addWidget(self.textedit)
        self.setLayout(layout)


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()