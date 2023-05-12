# Script Guide - WT versus AD comparison

**_Date: May 2023_**

- **Author:** Mohammed Salim Dason
- **Supervisors:** Prof. Davide Cora, Prof. Francesco Favero
- **Institution:** Bioinformatics Unit, Università del Piemonte Orientale (UPO) - CAAD


This script was developed to first take the matrix file (output of a different script I created)
in tab delimited format that can be fed into [Microbiome Analyst](https://www.microbiomeanalyst.ca/) and then from the output of 
single factor analysis at the species taxonomic level, identify the different species that are
statistically significant:

- Absolute log2FC score  > 1
- FDR score < 0.05

Once the statistically significant species have been identified, the script creates temporary files
that contain these statically species (see the TEMP folder). 

The next step is to lookup each statically significant specie in the input Matrix file, and extract
the columns that apply. For example, if the aim is to construct a heatmap of 2 months WT versus 2 months AD,
we will extract only the values for samples belonging to this group as shown below (extract from input matrix file):


| Name                               | 2WT-2m_S1 | 3WT-2m_S1 | 5WT-2m_S2 | 8WT-2m_S3 | 9WT-2m_S4 | 10WT-2m_S5 | 2AD-2m_S6 | 4AD-2m_S2 | 5AD-2m_S7 | 8AD-2m_S8 | 9AD-2m_S9 | 10AD-2m_S10 |
|------------------------------------|-----------|-----------|-----------|-----------|-----------|-------------|------------|------------|------------|------------|------------|--------------|
| s__Akkermansia_muciniphila         | 0         | 2884      | 2822      | 0         | 9190      | 0           | 76         | 512772     | 360726     | 160650     | 0          | 0            |
| s__Parasutterella_excrementihominis | 0         | 884       | 2822      | 89        | 93489     | 0           | 76         | 270        | 36026      | 150        | 10         | 0            |
| s__GGB31312_SGB44628                | 112       | 1321      | 212       | 12        | 34        | 222         | 76         | 512        | 360726     | 1260       | 233        | 131          |
| s__GGB30466_SGB43544                | 67        | 27884     | 2822      | 0         | 0         | 0           | 76         | 772        | 3072       | 1650       | 131        | 0            |

Once the significant species have been extracted from the corresponding samples, the script will then 
create a heatmap using a script written in R. This present script uses a python wrapper (util.py)  that wraps around
the R script that dynamically generates the different heatmaps for the different groups. 

# Requirements

Before using this script, make sure you have the following requirements:

- Python 3.7 or higher
- Pip package manager
- Input Matrix file for Microbiome Analyst in tab delimited format (Place in data folder)
- Results of single factor analysis (best to use same naming structure I used)
- R scripts (3 in total i.e. two_months_heatmap.R, six_months_heatmap.R, twelve_months_heatmap.R)

# How to Use

In the create_heatmap.py file, make the following change:

    if __name__ == "__main__":
        x = CreateHeatmap("data/{putMatrixFileNameHere}")
        x.start()

Once this is done, run:

$ python create_heatmap.py

# Sample Output

![image](https://github.com/salimdason/MicrobiomeAnalyst-Univariate-Analysis-heatmaps/assets/71772022/bd366623-b37b-4e52-aa6a-64863ed630ba)




