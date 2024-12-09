import pandas as pd
import numpy as np

import os.path
import datetime as dt
import time

import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as pgo

from PyPDF2 import PdfWriter, PdfReader
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

class UserInputValidation:
    def __init__(self):
        pass
    
#    def validate_input_string(self, user_input):
#        try:
#            user_input = int(user_input)
#        except: user_input('Please enter a string')
#
#        return user_input



class SetParameters:
    def __init__(self):
        pass

    def source_user_input_string(self, user_input_string):
        '''
        Source the inputs from the user and store in a variable to use when 1) creating file paths 2) Labeling charts or tables.
        '''
        result_user_input_string = str(user_input_string.get())
        
        return result_user_input_string

    def define_file_path(self, base_location_value, folder_prefix):
        '''
        Used to create an initial file path based on the passed user inputs.
        '''
        result_file_path = f'{base_location_value}\\{folder_prefix}'
        
        return result_file_path
      
    def define_full_file_path(self, base_location_value, folder_prefix, file_name, file_type):
        '''
        Used to create a complete file path with file names and file types based on the passed user inputs.
        '''
        result_full_file_path = f'{base_location_value}\\{folder_prefix}\\{file_name}.{file_type}'
        
        return result_full_file_path
    
    def define_full_output_file_path(self, base_location_value, folder_prefix, file_name, indicator_1, indicator_2, output_file_type):
        '''
        Used to create a complete file path for output based on the current date and passed user inputs.
        '''
        run_date = run_date = dt.date.today()
        run_date_formatted = run_date.strftime('%Y%m%d')
        result_output_file_path = f'{base_location_value}\\{folder_prefix}\\{file_name}_{indicator_1}_{indicator_2}_{run_date_formatted}.{output_file_type}'

        return result_output_file_path
    
class CreateUserInterface:
    def __init__(self):
        pass

    def test1(self):
        abc = str(baseLocation.get())

    def create_user_interface(self, source_process):
        root = Tk()
        root.title('Soure Economic Data')

        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        ttk.Label(mainframe, text="File Location:").grid(column=1, row=1, sticky=W)

        baseLocation = StringVar()
        baseLocation_entry = ttk.Entry(mainframe, width=50, textvariable=baseLocation)
        baseLocation_entry.grid(column=2, row=1, sticky=(W, E))

        ttk.Label(mainframe, text="File 1 Name:").grid(column=1, row=2, sticky=W)

        inputFile1 = StringVar()
        inputFile1_entry = ttk.Entry(mainframe, width=50, textvariable=inputFile1)
        inputFile1_entry.grid(column=2, row=2, sticky=(W, E))

        ttk.Label(mainframe, text="   File 1 Description:").grid(column=1, row=3, sticky=W)

        inputFileDesc1 = StringVar()
        inputFileDesc1_entry = ttk.Entry(mainframe, width=50, textvariable=inputFileDesc1)
        inputFileDesc1_entry.grid(column=2, row=3, sticky=(W, E))

        ttk.Label(mainframe, text="File 2 Name:").grid(column=1, row=4, sticky=W)

        inputFile2 = StringVar()
        inputFile2_entry = ttk.Entry(mainframe, width=50, textvariable=inputFile2)
        inputFile2_entry.grid(column=2, row=4, sticky=(W, E))

        ttk.Label(mainframe, text="   File 2 Description:").grid(column=1, row=5, sticky=W)

        inputFileDesc2 = StringVar()
        inputFileDesc2_entry = ttk.Entry(mainframe, width=50, textvariable=inputFileDesc2)
        inputFileDesc2_entry.grid(column=2, row=5, sticky=(W, E))

        ttk.Button(mainframe, text="Source Econ Data", command=source_process).grid(column=1, row=6, sticky=W)

        for child in mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

        baseLocation_entry.focus()
        inputFile1_entry.focus()
        inputFile2_entry.focus()
        root.bind("<Return>", source_process)

        root.mainloop()  

class PreProcessData:
    def __init__(self):
        pass

    def convert_wide_to_long(self, df_input, name_column_date, desc_input_variable):
        '''
        Pivot column names to rows to ensure standardized column names are used in code. 
        This allows the user to change the economic indicators used without updating the underlying code.
        Convert the reporting date column from an object to datetime for graphing and calculations.
        Set a variable description based on user input for output presentation, as FRED csv does not include descriptions  
        '''
        df = df_input.copy() # create copy of initial dataframe for transformations, as initial table will be output later for dashboard
        dict_df_columns = df_input.columns
        df = df.melt(id_vars=dict_df_columns[0], value_vars=dict_df_columns[1])
        df['reporting_date'] = pd.to_datetime(df[name_column_date], errors='coerce')
        df['variable_desc'] = str(desc_input_variable)

        return df
    
    def stack_and_format(self, df_1, df_2):
        '''
        Create a stacked dataframe from both data sources for use in the time series chart.
        Update column names to be easily understood by business user's in charts and tables.
        '''
        df_input_stack = pd.concat([df_1, df_2]) # Stack dataframes for plotting
        '''
        SQL Equivalent ->
        SELECT a.* FROM tableA a
        UNION ALL
        SELECT b.* FROM tableB b
        '''
        df_input_stack_formatted = pd.DataFrame() # create empty dataframe to store formatted table
        df_input_stack_formatted['Date'] = df_input_stack['reporting_date'].dt.strftime('%Y-%m-%d')
        df_input_stack_formatted['Index Value'] = df_input_stack['value']
        df_input_stack_formatted['Variable Description'] = df_input_stack['variable_desc']   
        '''
        SQL Equivalent ->
        SELECT 
        a.[reporting_date] as 'Date'
        a.[value] as 'Index Value'
        a.[variable_desc] as 'Variable Description'
        FROM tableA a
        '''
        return df_input_stack_formatted
    
class AnalysisCalculations:
    def __init__(self):
        pass

    def calc_correlation(self, df, name_column_x, name_column_y):
        '''
        Calculate the correlation coefficiant based in the user input datasets.
        Create a message to be output after the application finishes running for the user to quickly view the key results.
        '''
        value_correlation = df[name_column_x].corr(df[name_column_y])
        message_result_correlation = f'Correlation coefficient = {value_correlation:.4f}.'

        return value_correlation, message_result_correlation
    
    def calc_dataset_periods(self, df, name_column_date, desc_input_variable):
        '''
        Calculate the number of periods, beginning year, and ending year for user review.
        Create a message to be output after the application finishes running for the user to quickly view the key results.
        '''
        number_of_periods = len(df)
        year_start = df[name_column_date].min().year
        year_end = df[name_column_date].max().year
        '''
        SQL Equivalent ->
        SELECT
        a.[variable_desc]
        ,COUNT(a.[reporting_date]) as 'number_of_periods'
        ,MIN(YEAR(a.[reporting_date])) as 'year_start'
        ,MAX(YEAR(a.[reporting_date])) as 'year_end'
        FROM tableA a
        GROUP BY a.[variable_desc]
        '''
        message_time_horizon = (f'{desc_input_variable} table has {number_of_periods} records from {year_start} to {year_end}')

        return number_of_periods, year_start, year_end, message_time_horizon
    
class VisualizationCreation:
    def __init__(self):
        pass

    def create_time_series_chart(self, df, desc_input_variable_1, desc_input_variable_2):
        '''
        Create a time series chart based on the indicators in the datasets.
        Each line of the time series chart will be a different color based on the indicator.
        '''
        fig_time_series = px.line(df,
                                  x='Date',
                                  y='Index Value',
                                  color='Variable Description',
                                  title=f'{desc_input_variable_1} & {desc_input_variable_2}'
                                  )
        
        return fig_time_series
    
    def create_table(self, df):
        '''
        Create a simple table to view the input data from FRED.
        '''
        fig_simple_table = pgo.Figure(
                            data=[pgo.Table(
                            header=dict(values=list(df.columns), 
                                        fill_color='skyblue', 
                                        align='left'),
                            cells=dict(values=[df['Date'], df['Index Value'], df['Variable Description']],
                                        fill_color='slategray',
                                        align='left')
                                )                       
                             ]
                                    )
        
        return fig_simple_table

### SET UP CLASSES THAT WILL BE USED IN PROCESS ###
UserInputValidation = UserInputValidation()
SetParameters = SetParameters()
CreateUserInterface = CreateUserInterface()
PreProcessData = PreProcessData()
AnalysisCalculations = AnalysisCalculations()
VisualizationCreation = VisualizationCreation()

### PROCESS DEFINITION ###
def source_econ_data(*args):

    ## FILE LOCATION SETUP ##

    base_location = SetParameters.source_user_input_string(baseLocation)
    input_file_1 = SetParameters.source_user_input_string(inputFile1)
    input_file_2 = SetParameters.source_user_input_string(inputFile2)
    input_desc_1 = SetParameters.source_user_input_string(inputFileDesc1)
    input_desc_2 = SetParameters.source_user_input_string(inputFileDesc2)

    input_full_file_path_1 = SetParameters.define_full_file_path(base_location, '01_Input', input_file_1, 'csv')
    input_full_file_path_2 = SetParameters.define_full_file_path(base_location, '01_Input', input_file_2, 'csv')
    output_file_path = SetParameters.define_file_path(base_location, '02_Output')

    ## VALIDATE USER INPUT ##
    UserInputValidation.validate_input_string(base_location)
    ## DATA SOURCING AND PRE-PROCESSING ##

    # Source csv files as pandas dataframes. These files can be any downloaded file from FRED with the column format DATE, {some_value}  
    df_input_1 = pd.read_csv(input_full_file_path_1, sep=',')
    df_input_2 = pd.read_csv(input_full_file_path_2, sep=',')
    '''
    SQL EQUIVALENT -> 
    SELECT a.* FROM tableA a;
    SELECT b.* FROM tableB b;
    '''

    # Pre-process data tables
    df_preproc_1 = PreProcessData.convert_wide_to_long(df_input_1, 'DATE', input_desc_1)
    df_preproc_2 = PreProcessData.convert_wide_to_long(df_input_2, 'DATE', input_desc_2)

    # Stack dataframes for plotting and assign formatted values
    df_preproc_stack_formatted = PreProcessData.stack_and_format(df_preproc_1, df_preproc_2)

    # Join dataframes to create a wide-format table for period-specific analysis
    df_preproc_joined = df_preproc_1.merge(df_preproc_2,
                                           on='DATE', # date used as unique key
                                           how='inner' # only output information where the unique key exists in each dataset, as some datasets are either available on different cadences or from different time periods
                                           )
    '''
    SQL Equivalent ->
    SELECT a.*, b.*
    FROM tableA a
    INNER JOIN tableB b
        ON a.DATE = b.DATE
    '''
    ## CALCULATIONS ##

    # Calculate correlation coefficient and create message for output
    results_correlation = AnalysisCalculations.calc_correlation(df_preproc_joined, 'value_x', 'value_y')

    # Calculate number of time periods available for comparison and in each dataset
    results_time_horizon_1 = AnalysisCalculations.calc_dataset_periods(df_preproc_1, 'reporting_date', input_desc_1)
    results_time_horizon_2 = AnalysisCalculations.calc_dataset_periods(df_preproc_2, 'reporting_date', input_desc_2)

    ## PLOTLY FIGURE CREATION

    # Create simple line chart plotting the value of each economic indicator over time
    fig_time_series = VisualizationCreation.create_time_series_chart(df_preproc_stack_formatted, input_desc_1, input_desc_2)

    # Create simple table including the raw values from the data tables
    fig_table = VisualizationCreation.create_table(df_preproc_stack_formatted)

    ## OUTPUT STEPS ##

    # Define output file names
    output_file_time_series_PDF = SetParameters.define_full_output_file_path(base_location, '02_Output', 'timeSeries', input_file_1, input_file_2, 'pdf')
    output_file_time_series_HTML = SetParameters.define_full_output_file_path(base_location, '02_Output', 'timeSeries', input_file_1, input_file_2, 'html')
    output_file_table_PDF = SetParameters.define_full_output_file_path(base_location, '02_Output', 'table', input_file_1, input_file_2, 'pdf')
    output_file_table_HTML = SetParameters.define_full_output_file_path(base_location, '02_Output', 'table', input_file_1, input_file_2, 'html')

    # Output HTML files
    fig_time_series.write_html(output_file_time_series_HTML)
    fig_table.write_html(output_file_table_HTML)
    
    # Output PDFs
    pio.write_image(fig_time_series, output_file_time_series_PDF)
    pio.write_image(fig_table, output_file_table_PDF)

    # Open HTML in browser for user review
    os.system(f'start {output_file_table_HTML}')
    os.system(f'start {output_file_time_series_HTML}')

    # Print output message in application
    messagebox.showinfo(message=f'Comparison between "{input_desc_1}" and "{input_desc_2}" is complete! {results_correlation[1]}')

#cui.create_user_interface(source_econ_data)

### USER INTERFACE CREATION ###
root = Tk() # launch the application
root.title('Economic Data Analysis') # set the name for the application

# Create container for user interface
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Create question label and input box for the file location
ttk.Label(mainframe, text='File Location:').grid(column=1, row=1, sticky=W)

baseLocation = StringVar()
baseLocation_entry = ttk.Entry(mainframe, width=50, textvariable=baseLocation)
baseLocation_entry.grid(column=2, row=1, sticky=(W, E))

# Create question label and input box for the first file name
ttk.Label(mainframe, text='File 1 Name:').grid(column=1, row=2, sticky=W)

inputFile1 = StringVar()
inputFile1_entry = ttk.Entry(mainframe, width=50, textvariable=inputFile1)
inputFile1_entry.grid(column=2, row=2, sticky=(W, E))

# Create question label and input box for the description of the indicator in the first file
ttk.Label(mainframe, text='   File 1 Description:').grid(column=1, row=3, sticky=W)

inputFileDesc1 = StringVar()
inputFileDesc1_entry = ttk.Entry(mainframe, width=50, textvariable=inputFileDesc1)
inputFileDesc1_entry.grid(column=2, row=3, sticky=(W, E))

# Create question label and input box for the second file name
ttk.Label(mainframe, text='File 2 Name:').grid(column=1, row=4, sticky=W)

inputFile2 = StringVar()
inputFile2_entry = ttk.Entry(mainframe, width=50, textvariable=inputFile2)
inputFile2_entry.grid(column=2, row=4, sticky=(W, E))

# Create question label and input box for the description of the indicator in the second file
ttk.Label(mainframe, text='   File 2 Description:').grid(column=1, row=5, sticky=W)

inputFileDesc2 = StringVar()
inputFileDesc2_entry = ttk.Entry(mainframe, width=50, textvariable=inputFileDesc2)
inputFileDesc2_entry.grid(column=2, row=5, sticky=(W, E))

# Create the button that is clicked to start process
ttk.Button(mainframe, text='Run Process', command=source_econ_data).grid(column=1, row=6, sticky=W)

for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

baseLocation_entry.focus()
inputFile1_entry.focus()
inputFile2_entry.focus()
root.bind('<Return>', source_econ_data)

root.mainloop()