# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 13:24:13 2022

@author: Philipp
"""


import pandas as pd
import ProteomicTools
import re



proteomic_tools = ProteomicTools.ProteomicTools()



class ReadProteoforms:
    def __init__(self):
        self.mass = 'Theo. Mass [Da]'
        self.sequence = 'Sequence'
        self.residue_cleavage = '% Residue Cleavages'
        self.prsms = '# PrSMs'
        self.c_score = 'Best PrSM C-Score'





    
    def read_prosight_results(self, file: str, pd_version: str = 'ProSight v4.0') -> pd.DataFrame:
        """ return dataframe of subsequence_proteoforms"""
        if pd_version == 'ProSight v4.1':
            self.annotated_confidence = 'Confidence (by Search Engine): ' \
                                    'ProSightPD 4.1 Annotated Proteoform Search'
            self.subsequence_confidence = 'Confidence (by Search Engine): ' \
                                        'ProSightPD 4.1 Subsequence Search'
        elif pd_version == "ProSight v4.0":
            self.annotated_confidence = 'Confidence (by Search Engine): ' \
                                'ProSightPD 4.0 Annotated Proteoform Search Node'
            self.subsequence_confidence = 'Confidence (by Search Engine):' \
                            ' ProSightPD 4.0 Subsequence Search'
        elif pd_version == "ProSight v4.2":
            self.annotated_confidence = 'Confidence (by Search Engine): ProSightPD 4.2 Annotated Proteoform Search'
            self.subsequence_confidence = 'Confidence (by Search Engine): ProSightPD 4.2 Subsequence Search'
        else:
            print ("PD-Version is wrong!", pd_version)
        df = pd.read_csv(file, on_bad_lines="warn", delimiter="\t")
        # df = df[df[self.subsequence_confidence] == 'High']
        # df = df[df[self.annotated_confidence] != 'High']
            # df = df.sort_values(by=["# PrSMs"], ascending=False).head(10)
            # print(list(df["# PrSMs"]))
            # print(list(df["Theo. Mass [Da]"]))
        print ("opened", file)
        print("Number of all identified Proteoforms:", len(df.index))
        return df
    
    
    
    def clear_sequences(self, sequences):
        """ sequence format M.KSDSDPRTSIIV.K """
        clear_sequences = []
        aa_list = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 
                        'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
        for seq in sequences :
            # remove all numbers between brackets [] (contains mass shift)
            seq = re.sub("[\[].*?[\]]", "", seq)
            try:
                n_term_from_cleavage, sequence, c_term_from_cleavage = seq.split(".")
                sequence = [i for i in sequence if i  in aa_list]
                clear_sequences.append("".join(sequence))
            except: 
                print("something is wrong the sequence", seq)
        return clear_sequences

    
    
    
    def read_toppic_results(self, file: str) -> pd.DataFrame:
        df = pd.read_csv(file, on_bad_lines="warn", delimiter=",")
        # df = df[df[]]
        print ("opened", file)
        print("Number of Proteoforms:", len(df.index))
        print("Analysis is sequence-based! Modified Proteoforms with the same \
              amino acid sequence are not count multiple times")
        return df
    
    
    
    def read_sequence_list(self, file:str) -> pd.DataFrame:
        """ column name: Sequence """
        try:
            df = pd.read_csv(file, on_bad_lines="warn", sep=None, engine="python")# sep='\s+')
            df["Sequence"][0]
        except:
            try:
                df = pd.read_csv(file, on_bad_lines="warn", sep=",", engine="python")# sep='\s+')
                df["Sequence"][0]
            except:
                print("Error during loading the file. File Structure correct?")
        print(df)
        if "." in df["Sequence"][0]: 
            df["Sequence"] = self.clear_sequences(df["Sequence"])
        if "#PrSMs" not in df.columns:
            print("No #PrSMs column!")
            df["#PrSMs"] = [1 for i in df.index]
        return df



    def extract_properties_multiple_data(self, all_data_dict_df: dict,
                                         c_score_filter: int = 0) -> dict:
        """
        Parameters
        ----------
        all_data_dict_df : dict
            read_multiple_data output.

        Returns
        -------
        dict_data : dict
            Dictionary .

        """
        files = all_data_dict_df.keys()
        dict_data = {"file_names":[], "sequences":[], "masses":[], "seq_mass":[],
                     "gravys":[], "pis":[], "annotated":[], "subsequence":[], 
                     "residue_cleavage":[], "c_score":[], "prsms":[]}
        for file in files:
            file_name = file #_extract_file_name(file)
            data = all_data_dict_df[file]  # dataframe for each file
            data = data[data[self.c_score] > c_score_filter]
            # data = data[data[read_proteoforms.annotated_confidence] == 'High']
            masses = list(data[self.mass])
            sequences = list(data[self.sequence])
            pis = [proteomic_tools.calculate_pI(seq) for seq in sequences]
            gravys = [proteomic_tools.calculate_gravy(seq) for seq in sequences]
            annotated = list(data[self.annotated_confidence])
            subsequence = list(data[self.subsequence_confidence])
            residue_cleavage = list(data[self.residue_cleavage])
            c_score = list(data[self.c_score])
            prsms = list(data[self.prsms])

            dict_data["file_names"].append([file_name, file])
            dict_data["sequences"].append(gravys)
            dict_data["masses"].append(masses)
            dict_data["seq_mass"].append(list(zip(sequences, masses)))
            dict_data["gravys"].append(gravys)
            dict_data["pis"].append(pis)
            dict_data["annotated"].append(annotated)
            dict_data["subsequence"].append(subsequence)
            dict_data["residue_cleavage"].append(residue_cleavage)
            dict_data["c_score"].append(c_score)
            dict_data["prsms"].append(prsms)
            
            
        return dict_data
    
    
    