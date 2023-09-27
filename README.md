# TD Potential Cleavage Analyzer

 <p align="center">
<img src="https://img.shields.io/badge/python-3.9.13+-blue.svg" alt="Python Version"> 
<img src="https://img.shields.io/pypi/l/MSDIFF" alt="License">
</p>

**Summary**: The tool analyzes the proteoform termini and graphically displays various properties of the identified termini.

**Input**: Sequence list of identified proteoforms or exported proteoform identifications from ProteomeDiscoverer and fasta file. As

**Output**: Various visualizations for the identified termini and potential cleavage events. 



## Contents

- [Abstract](#abstract)
- [Technical Description](#technical-description)
- [Requirements](#requirements)
    - [Packages](#packages)
- [How to run the Script](#how-to-run-the-script)
- [Input Data](#input-data)
    - [Identified Proteoforms](#identified-proteoforms)
    - [Fasta File](#fasta-file)
- [Graphical User Interface](#graphical-user-interface)
    - [Initialization](#initialization)
    - [Visualization](#visualization)
- [Data Sets for Testing](#data-sets-for-testing)
- [Output](#output)
    - [Potential cleavage analysis of subsequence proteoforms](#potential-cleavage-analysis-of-subsequence-proteoforms)
    - [Analyze Potential Cleavage Fasta File](#analyze-potential-cleavage-fasta-file)
    - [N-terminal Methionine Excision](#n-terminal-methionine-excision)
    - [Number of Annotated and Subsequence Proteoforms](#number-of-annotated-and-subsequence-proteoforms)
    - [Visualization of Identified Proteoforms for Specific Proteins](#visualization-of-identified-proteoforms-for-specific-proteins)
- [Troubleshooting](#troubleshooting)
- [Contributions](#contributions)
- [Changelog](#changelog)
- [References](#references)
- [How to cite](#how-to-cite)
- [License](#license)



## Abstract

Top-down Proteomics identifies intact proteoforms with all their modifications and truncations. Subsequence proteoforms arises from truncations of annotated proteoforms, which can occur, for example, due to proteolytic processing, alternative splicing or (artificial) chemical cleavage. 

The tool analyzes the proteoform termini and graphically displays various properties of the identified termini. The following analyses can be performed:

- Potential cleavage analysis of subsequence proteoforms
- Analysis of N-terminal Methionine Excision
- Analysis of truncation events 
- Visualization of Identified Proteoforms for Specific Proteins

Note that annotated proteoforms are only proteoforms that have the same length as deposited in the fasta file or where only the start methionine has been cleaved. Proteoforms where the signal peptide has been cleaved are considered as N-terminal truncated proteoforms.



## Technical Description

For each proteoform, the tool searches the corresponding full length protein in the fasta database and checks whether it is an N- and/or C-terminal truncated proteoform. The subsequence proteoforms are examined for their possible cleavage sites with respect to the full length protein (**Figure 1**). If the proteoform can be assigned to multiple proteins, the tool checks if the corresponding amino acids N- and C-terminal are the same for all assigned proteins. If this is not the case, the subsequence proteoform is not considered further due to ambiguity. N-terminally non-truncated proteoforms (or with only start methionine cleaved) are used for start methionine cleavage analysis. 

<img src="Various\TechnicalDescription.png" style="zoom:57%" alt="Result_Methionin_Cleavage"/>

**Figure 1**: Determination of potential cleavage sites by analyzing subsequence proteoforms. The tool searches for each proteoform their corresponding full length protein in the fasta file and identifies the potential cleavaes sites. 



## Requirements

- Python 3.9.13 or higher

### Packages 

- Bio==1.5.3
- matplotlib==3.5.1
- pandas==1.4.2
- PyQt5==5.15.7
- pyteomics==4.5
- seaborn==0.11.2

  

## How to run the Script

Installation and use of Anaconda Distribution and its build-in command line prompt is highly recommended. In case you don't use Anaconda, make sure all required packages are installed upfront.

````powershell
$ cd <PATH/TO/SOURCES>
$ python GUI.py
````

 

## Input Data

### Identified Proteoforms

The tool allows different input formats for the identified proteoforms: 

- Sequence list: A csv file containing one column labeled "Sequence" with all identified proteoform sequences. The sequences can be in the format "MKRSSIVLKPRSAADSRP" (ProSight Output-Format) or ".M(Acetyl)KRSS(+79)IVLKPRSAADSRP.D" (TopPic Output-Format). A second column labeled with "'PrSMs" can be added, indicating the number of identified proteoform spectrum matches of the associated proteoforms. 
- Proteome Discoverer database results. Exported proteoform results as txt-files. If the search was performed within Proteome Discoverer, use the "File->Export->To Text" function to export the proteoform results as txt-file.
- TopPic database result. Not yet fully supported. 

### Fasta File

Fasta file, which was also used for database search. If database search was performed against a XML file, download the corresponding Fasta-file from UniProt. 

  

## Graphical User Interface 

<img src="Various\GUI_2.PNG" style="zoom:100%" alt="GUI"/>

**Figure 2**: Graphical User Interface.

### Initialization

1. Fasta File. Opens file dialog to select a Fasta File, see [Input Data](##Input-Data) for details.
2. Proteoform File. Opens file dialog to select a proteoform file, see [Input Data](##Input-Data) for details.
3. Select proteoform file format, see [Input Data](##Input-Data) for details.
4. Select either Proteoform Level or PrSM Level. The PrSM level takes into account the number of PrSMs for each subsequence proteoform, i.e. the results of potential cleavage sites are weighted by the number of PrSMs. The selection has an effect only if the number of PrSMs of the proteoforms are included in the input file. 
5. Initialization: Reading of the input files and initialization of different analysis. This may take a while depending on the size of the input files. The progress of the calculations is displayed in the command line. 
6. Analyze FASTA: The tool calculates all theoretical proteoform termini of all proteins in the database (that is, it basically calculates the number of all dipeptide combinations in the database). The resulting heatmap with histograms is plotted and the heat map data are displayed in the command line window.  

### Visualization

1. Truncations: Generates pie chart of identified proteoforms, with distinction between N-terminal truncated, C-terminal truncated, N- and C-terminal truncated and full length (=not truncated) proteoforms.  
2. Potential Cleavage: Generates heatmap showing the number of amino acids identified in X and X'-Positions of N- and C-terminal truncated subsequence proteoforms. 
3. Methionine Cleavage: Generates plots displaying the N-terminal methionine cleavage excision properties.
4. Export Data: Opens file dialog to select path were all results will be saved as txt-files. 
5. Analyze Accession: Select the protein accession of interest and "Analyze Accession" generates plots to visualize the identified proteoforms in respect to the full length proteoform.  





## Data Sets for Testing

To test the script, you can download the datasets in the Datasets folder, which contains an *E. coli* Fasta file and a Dataset Demo file containing proteoform identifications exported from ProSightPD results. A detailed description of the expected output results after running the script is shown in [Output](##Output). 



 ## Output 

 Settings: 

- Input fasta file "Dataset\\PTK_Ecoli_FASTA_all.fasta" 
- Input proteoform file "DEMO_Proteoforms.txt"
- ProSightPD Search Result
- Proteoform level 

As soon as 'Initalization' is pressed, the analysis starts. The progress of the calculations is displayed in the command line. If there are proteoforms in the input that cannot be assigned to an accession number, these are also output in the command line. 

 All charts can be exported in different file formats. 



### Potential cleavage analysis of subsequence proteoforms

The tool identifies the X and X’ cleavage site of subsequence proteoforms, whereby X represents the N-terminal and X’ the C-terminal cleavage position, respectively. Both N-terminal and/or C-terminal truncated subsequence proteoforms are considered.  

<img src="Various\Result_Heatmap.png" style="zoom:100%" alt="Result_Heatmap"/>

**Figure 3**: Potential cleavage analysis plot. The heatmap shows the potential cleavage sites between two amino acids determined by the subsequence proteoforms, with the X site shown vertically and the X' site shown horizontally. The histograms show the total number of amino acids determined at the X' site (right) or at the X site (top). 


<img src="Various\CMD_Output.PNG" style="zoom:100%" alt="CMD_Output"/>


**Figure 4:** Potential cleavage analysis command line output. The command line shows the loaded input files (fasta- and proteoform txt-file), the number of considered subsequence proteoforms and the number of potential cleavage events.  



### Analyze Potential Cleavage Fasta File

The tool calculates all theoretical proteoform termini of all proteins in the database (that is, it basically calculates the number of all dipeptide combinations in the database). 

<img src="Various\Result_AnalyzeFastaFile.png" style="zoom:95%" alt="Result_AnalyzeFastaFile"/>

**Figure 5**: Theoretical possible cleavage events in the entire fasta file. 



### N-terminal Methionine Excision

The tool identifies all proteoforms whose N-terminus is not truncated, or where only the start methionine is cleaved. The influence of the following amino acid and its size on methionine cleavage is analyzed. 

<img src="Various\Result_Methionin_Cleavage_relativeAndAbsolut.png" style="zoom:57%" alt="Result_Methionin_Cleavage_relative"/>

**Figure 6**: Plots displaying the N-terminal methionine cleavage excision properties. A) bar plot showing the count of amino acids at the N-term if the start methionine is cleaved (red bars, Met cleaved) and in the position after the methionine if the start methionine is not cleaved (black bars, Met not-cleaved). B) shows the percentage of methionine cleavage before a given amino acid, with the amino acid radius shown on the x-axis.  



### Number of Annotated and Subsequence Proteoforms

The tool identifies the number of annotated, N-terminal, C-terminal and N- and C-terminal truncation proteoforms. 





<img src="Various\Result_Truncation_PieChart.png" style="zoom:85%" alt="Result_Proteoform_Truncation_PieChart"/>

**Figure 7**: Percentage of identified C-terminal, N-terminal, C- and N-terminal or non-truncated (full length) proteoforms displayed as a pie chart. 



### Visualization of Identified Proteoforms for Specific Proteins



<img src="Various\Result_ProteoformVisualization.png" style="zoom:75%" alt="Result_ProteoformVisualization"/>

**Figure 8**: Visualization of the identified proteoforms compared to the full-length proteoform. The x-axis shows the amino acid position of the full-length proteoform (as deposited in the fasta file). The identified proteoforms are plotted as bars along the y-axis. If the number of PrSMs is specified in the input file, the proteoforms are color coded with respect to their abundance (#PrSMs). 





<img src="Various\Result_ProteoformVisualization_CMD.png" style="zoom:60%" alt="Result_ProteoformVisualization"/>

**Figure  9**: Visualization of the identified proteoforms compared to the full-length proteoform in the command line window. The first row shows the full-length proteoform (as deposited in the fasta file) and the following rows show the identified proteoforms. The columns show 1) the start amino acid of the proteoform (compared to the full-length proteoform), 2) the end amino acid of the proteoform, 3) the proteoform sequence, and 4) the number of associated PrSMs. 





<img src="Various\Result_ProteoformVisualization_ProteoformsAndPrSMs.png" style="zoom:65%" alt="Result_ProteoformVisualization_ProteoformsAndPrSMs"/>

**Figure 10**: Visualization of the N- and C-termini of the identified proteoforms. Shown are the relative amino acid positions (compared to the full-length proteoform) identified as the N-terminus (gray) or C-terminus (red), and the number of A) PrSMs and B) proteoforms. In addition, the potential cleavage event leading to the N- and C-terminus is shown in the form X|X' above the respective columns. The character '.' describes the canonical N-terminus or C-terminus, which means, for example, that the identified N-terminus '.|M' is the canonical N-terminus. 





## Troubleshooting





## Contributions 

PTK, Python script written, basic ideas 

JR, If a proteoform can be assigned to multiple proteins and they share the same potential cleavage sites, the proteoform can still be considered.

AT, Many ideas for data visualization 





## Changelog

- v1.0.0 (July 2021) First release
- v1.0.1 (January 2022) Minor bugfixes 
- v1.0.2 (November 2022): Included ambiguous subsequence proteoforms (can arise from multiple proteins) if all proteins have the same potential cleavage site
- v1.0.3 (December 2022): Improved visualization, added histograms to heatmap 
- v2.0.1 (January 2023): New Graphical User Interface, added proteoform protein analysis 



## References





 ## How to cite

 

 

## License

The tool is available under the BSD license. See the LICENSE file for more info.

 
