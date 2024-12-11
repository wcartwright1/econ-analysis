# Economic Analysis Case Study
 
## Overview
The purpose of this project is to create an application in Python (EconAnalysisApp.py) to analyze the relationship between two economic indicators from the Federal Reserve Economic Data (FRED) database. This project includes a Python script to source, transform, and analyze the datasets, as well as create a time-series chart and table to present the results of the analysis. The Python script sits beneath a tkinter user interface to make it easier for business users to use the process. The charts and tables are output as a PDF and an interactive html file. csv and hyper outputs are also included for use in a Tableau dashboard.

## Key Technologies Used
- Python
- Jupyter
- HTML
- Tableau

## Key Features
- Input two datasets from FRED in Date|Value format to run analysis and create time series charts
- User application through tkinter for dynamic user input (e.g. changing datasets, file locations, and time horizons)
- Dynamic column mapping to allow for any dataset from FRED in Date|Value format 
- Interactive HTML charts and tables open automatically in browser once process is completed

## Future Updates
- Change data sourcing from csv to API requests
- Implement additional user input validation
- Collaborate with users to define additional calculations and important predictive analytics
- Improve and combine PDF outputs from Plotly to include additional run information 
- Store detailed results in SQL database for users to access historical reports
- Live connections in Tableau Professional to update dashboard on schedule
- Trigger Python script from Tableau dashboard to allow users to update dashboard with new indicators or observations

## Challenges
- Tableau Public does not allow hyper files for input. The current dashboard only uses csv extracts which need to be updated after the process is run. By using Tableau Professional, hyper files can be automatically sourced after each run or the results can be stored in an SQL database for similar functionality.
- FRED csv extracts do not contain descriptions for the economic indicator. By querying data through the FRED API, descriptions can be automatically added and removed from the required user inputs.

## How-to Guide

### Required folder structure
Base folder with two subfolders:
- 01_Input
- 02_Output

### Steps to create environment and install dependencies:
1. Create new python environment (conda create -n {env_name} python=3.8)
2. Install pandas for data transformation (conda install pandas)
3. Install jupyter for an interactive notebook (conda install jupyter)
4. Install plotly for charts, graphs, and tables (conda install plotly)
5. Install kaleido for image export, specifying version 0.1.0post1 for jupyter integration (pip install kaleido==0.1.0post1)
6. Tkinter should be installed with the basic python installation - no additional packages required

### Steps to run application after environment is created and dependencies are installed
1. Download two csv files from FRED that are structured in the Date|Value format for analysis (https://fred.stlouisfed.org/)
2. Save files in the '01_Input' folder
2. Open Anaconda Prompt
2. _OPTIONAL_ - View available Python environments (conda info --envs)
3. Activate environment (conda activate {env_name})
4. Navigate to path of script (cd {script_path})
5. Run EconAnalysisApp.py (python EconAnalysisApp.py)
6. Input user parameters for file path, file names, file descriptions, and analysis periods (see below for user input documentation and examples)
7. Click 'Run Process'
8. To end process, close messagebox and exit application
9. When complete, close Anaconda Prompt or deactivate environment (conda deactivate)

### User input documentation
- Base Location: Enter the folder location the holds the input and output folders
- File 1 Name: Enter the name of the first file from the FRED csv download. FILE EXTENSIONS SHOULD NOT BE INCLUDED.
- File 1 Description: Enter a description for the first file from the FRED csv download. This will be displayed on the output charts and tables.
- File 2 Name: Enter the name of the second file from the FRED csv download. FILE EXTENSIONS SHOULD NOT BE INCLUDED.
- File 2 Description: Enter a description for the second file from the FRED csv download. This will be displayed on the output charts and tables.
- Lag Periods: Defaults to 6 periods. Enter the number of periods for the lag analysis. Periods are based on frequency of data in tables (e.g. monthly, annually)
- Lead Periods: Defaults to 6 periods. Enter the number of periods for the lead analysis. Periods are based on frequency of data in tables (e.g. monthly, annually)

### User input examples
- Base Location: C:\Users\billy\Documents\00_presentationEcon
- File 1 Name: PNRGINDEXM
- File 1 Description: Global price of Energy index
- File 2 Name: PINDUINDEXM
- File 2 Description: Global price of Industrial Materials index
- Lag Periods: 6
- Lead Periods: 6