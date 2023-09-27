# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 13:29:53 2022

@author: Philipp
"""

import csv






def only_one_unique_element_in_list(l):
    number_unique_elements = len(list(set(l)))
    return True if number_unique_elements == 1 else False 
    
    
    
def check_multiple_lists_are_identical(ll):
    if len(ll) == 0: return True
    h1 = []
    l1 = ll[0]
    for l2 in ll[1:]:
        h1.append(sorted(l1) == sorted(l2))
    return False if False in h1 else True


def calculate_overlap_coefficient(l1, l2):
    l1 = set(l1)
    l2 = set(l2)
    overlap = list(set(l1) & set(l2))
    minimal_length = len(l1) if len(l1) < len(l2) else len(l2)
    overlap_coefficient = len(overlap) / minimal_length
    return overlap_coefficient


def save_lists_in_csv(l, file_name):
    """ """
    with open(file_name, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(l)
        
        
def _extract_file_name(file):
    if "Caco__LMW" in file: file_name = "LMW method"
    elif "Caco__HLMW" in file: file_name = "HMW method"
    elif "Caco_1DLC_ACNTEAB_ACNNaCl_8GELFrEE_MWCO30_MWCO50_SPEC18_SPEC4_PEPPIMCW_PEPPIAnExSP_SEC_lysisACNTEAB_lysisACNNaCl__ABC_HMWLMW__ALL_Proteoforms." in file: 
        file_name = "ALL"
    elif "lysis" in file:
        file_name = "lys_ACN_NaCl" if "NaCl" in file else "lys_ACN_TEAB"
        if "R2" in file or "R3" in file:
            file_name += "_" + file.split("Caco_")[1].split("_")[4] 
        else: file_name += "_R1"
        file_name = file_name + file.split("Caco_")[1].split("_")[2]
    else:
        file_name = file.split("Caco_")[1].split("_")[0] + "_" + file.split("Caco_")[1].split("_")[1]  + "_" + file.split("Caco_")[1].split("_")[2] 
    
    return file_name



        
# def save_dict_in_csv(d, file_name, field_names):
#     """ """
#     with open(file_name, "w", newline="") as f:
#         writer = csv.DictWriter(f, fieldnames = field_names)
#         writer.writeheader()
#         writer.writerows(d)