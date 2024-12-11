import pandas as pd
import numpy as np

import os.path
import datetime as dt
import time

import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as pgo

from tkinter import *
from tkinter import ttk
from tkinter import messagebox

class SetParameters:
    def __init__(self):
        pass

    def source_user_input_string(self, user_input_string):
        '''
        Source the inputs from the user and store in a variable to use when 1) creating file paths 2) Labeling charts or tables.
        '''
        result_user_input_string = str(user_input_string.get())
        
        return result_user_input_string

    def source_user_input_integer(self, user_input_string):
        '''
        Source the inputs from the user and store in a variable to use when 1) creating file paths 2) Labeling charts or tables.
        '''
        result_user_input_integer = int(user_input_string.get())
        
        return result_user_input_integer
    
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
      
    def define_full_output_file_path_detailed(self, base_location_value, folder_prefix, file_name, indicator_1, indicator_2, output_file_type):
        '''
        Used to create a complete file path for output based on the current date and passed user inputs.
        '''
        run_date = dt.date.today()
        run_date_formatted = run_date.strftime('%Y%m%d')
        result_output_file_path_detailed = f'{base_location_value}\\{folder_prefix}\\{file_name}_{indicator_1}_{indicator_2}_{run_date_formatted}.{output_file_type}'

        return result_output_file_path_detailed
    
    def define_full_output_file_path_generic(self, base_location_value, folder_prefix, file_name, output_file_type):
        '''
        Used to create a complete file path for a generic output for Tableau datasets
        '''
        result_output_file_path_generic = f'{base_location_value}\\{folder_prefix}\\{file_name}.{output_file_type}'

        return result_output_file_path_generic
    
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
        df_long = df_input.copy() # create copy of initial dataframe for transformations, as initial table will be output later for dashboard
        dict_df_columns = df_input.columns
        df_long = df_long.melt(id_vars=dict_df_columns[0], value_vars=dict_df_columns[1])
        '''
        SQL Equivalent ->
        SELECT a.Date, c.variable, c.value
        FROM TableA a
        UNPIVOT
        value for variable IN (columns) as c
        '''
        df_long['reporting_date'] = pd.to_datetime(df_long[name_column_date], errors='coerce')
        df_long['variable_desc'] = str(desc_input_variable)

        return df_long
    
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
        df_input_stack_formatted['Value'] = df_input_stack['value']
        df_input_stack_formatted['Variable Description'] = df_input_stack['variable_desc']   
        '''
        SQL Equivalent ->
        SELECT 
        a.[reporting_date] as 'Date'
        a.[value] as 'Value'
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

    def calc_correlation_lag(self, df, name_column_x, name_column_y, lag_periods, lag_column_x_or_y):
        '''
        Shift dataframe column by -1 * lag_periods to calculate lag correlation.
        The lag column can be defined as x or y.
        '''
        valid_lag_columns = ['x', 'y']

        if lag_column_x_or_y not in valid_lag_columns:
            raise ValueError(f'Lag column value invalid. Valid values are {valid_lag_columns}.')

        if not isinstance(lag_periods, int):
            raise ValueError(f'Lag periods is not an integer.')
                
        if lag_column_x_or_y == 'x':
            df_lag = df[[name_column_x]].shift(-1*abs(lag_periods))
            value_lag_correlation = df_lag[name_column_x].corr(df[name_column_y])
        
        if lag_column_x_or_y == 'y':
            df_lag = df[[name_column_y]].shift(-1)
            value_lag_correlation = df_lag[name_column_y].corr(df[name_column_x])
        
        return value_lag_correlation

    def calc_correlation_lead(self, df, name_column_x, name_column_y, lead_periods, lead_column_x_or_y):
        '''
        Shift defined dataframe column by lead_periods to calculate lead correlation.
        The lead column can be defined as x or y.
        '''
        valid_lead_columns = ['x', 'y']

        if lead_column_x_or_y not in valid_lead_columns:
            raise ValueError(f'Lead column value invalid. Valid values are {valid_lead_columns}.')

        if not isinstance(lead_periods, int):
            raise ValueError(f'Lead periods is not an integer.')
                
        if lead_column_x_or_y == 'x':
            df_lead = df[[name_column_x]].shift(abs(lead_periods))
            value_lead_correlation = df_lead[name_column_x].corr(df[name_column_y])
        
        if lead_column_x_or_y == 'y':
            df_lead = df[[name_column_y]].shift(abs(lead_periods))
            value_lead_correlation = df_lead[name_column_y].corr(df[name_column_x])
        
        return value_lead_correlation
        
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
                                  y='Value',
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
                            cells=dict(values=df.transpose().values.tolist(),
                                        fill_color='slategray',
                                        align='left')
                                )                       
                             ]
                                    )
        
        return fig_simple_table

class TableauOutputPrep():
    def __init__(self):
        pass

    def format_tableau_output(self, df):
        df_tableau_output = df.copy()
        df_tableau_output['run_date'] = pd.to_datetime(dt.date.today()) # Add the current date as a column for filtering in Tableau
        df_tableau_output['created_by'] = os.getlogin() # Add the userID of the person who ran the report for audit trail

        return df_tableau_output
    
### DEFINE CLASSES THAT WILL BE USED IN PROCESS ###
SetParameters = SetParameters()
PreProcessData = PreProcessData()
AnalysisCalculations = AnalysisCalculations()
VisualizationCreation = VisualizationCreation()
TableauOutputPrep = TableauOutputPrep()

### PROCESS DEFINITION ###
def source_econ_data(*args):

    ## FILE LOCATION SETUP ##

    # Source user inputs from app
    base_location = SetParameters.source_user_input_string(baseLocation)
    input_file_1 = SetParameters.source_user_input_string(inputFile1)
    input_file_2 = SetParameters.source_user_input_string(inputFile2)
    input_desc_1 = SetParameters.source_user_input_string(inputFileDesc1)
    input_desc_2 = SetParameters.source_user_input_string(inputFileDesc2)
    lag_periods = SetParameters.source_user_input_integer(lagPeriods)
    lead_periods = SetParameters.source_user_input_integer(leadPeriods)

    # Create file paths from user inputs in app
    input_full_file_path_1 = SetParameters.define_full_file_path(base_location, '01_Input', input_file_1, 'csv')
    input_full_file_path_2 = SetParameters.define_full_file_path(base_location, '01_Input', input_file_2, 'csv')
    output_file_path = SetParameters.define_file_path(base_location, '02_Output')
    
    ###############
    
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

    ###############

    ## CALCULATIONS ##

    # Calculate correlation coefficient and create message for output
    results_correlation = AnalysisCalculations.calc_correlation(df_preproc_joined, 'value_x', 'value_y')
    dict_results_correlation = {'analysis_description': ['Correlation'],
                                'analysis_result': [results_correlation[0]],
                                'result_data_type': ['float']
                                } # add results to dictionary with description and data type
    df_results_correlation = pd.DataFrame.from_dict(dict_results_correlation, orient='columns') # convert dictionary to dataframe for final output

    # Calculate number of time periods available for comparison and in each dataset
    results_time_horizon_1 = AnalysisCalculations.calc_dataset_periods(df_preproc_1, 'reporting_date', input_desc_1)
    results_time_horizon_2 = AnalysisCalculations.calc_dataset_periods(df_preproc_2, 'reporting_date', input_desc_2)

    # Calculate lag and lead correlations based on user input lag and lead periods
    results_lag_correlation_x = AnalysisCalculations.calc_correlation_lag(df_preproc_joined, 'value_x', 'value_y', lag_periods, 'x')
    results_lag_correlation_y = AnalysisCalculations.calc_correlation_lag(df_preproc_joined, 'value_x', 'value_y', lag_periods, 'y')
    dict_results_lag = {'analysis_description': [f'Lag Correlation {input_desc_1}', f'Lag Periods {input_desc_1}', f'Lag Correlation {input_desc_2}', f'Lag Periods {input_desc_2}'],
                        'analysis_result': [results_lag_correlation_x, lag_periods, results_lag_correlation_y, lag_periods],
                        'result_data_type': ['float', 'int', 'float', 'int']
                        } # add results to dictionary with description and data type
    df_results_lag = pd.DataFrame.from_dict(dict_results_lag, orient='columns') # convert dictionary to dataframe for final output

    results_lead_correlation_x = AnalysisCalculations.calc_correlation_lead(df_preproc_joined, 'value_x', 'value_y', lead_periods, 'x')
    results_lead_correlation_y = AnalysisCalculations.calc_correlation_lead(df_preproc_joined, 'value_x', 'value_y', lead_periods, 'y')
    dict_results_lead = {'analysis_description': [f'Lead Correlation {input_desc_1}', f'Lead Periods {input_desc_1}', f'Lead Correlation {input_desc_2}', f'Lead Periods {input_desc_2}'],
                        'analysis_result': [results_lead_correlation_x, lead_periods, results_lead_correlation_y, lead_periods],
                        'result_data_type': ['float', 'int', 'float', 'int']
                        } # add results to dictionary with description and data type
    df_results_lead = pd.DataFrame.from_dict(dict_results_lead, orient='columns') # convert dictionary to dataframe for final output

    ###############

    ## CALCULATION RESULTS FORMATTING ##

    # Create empty dataframe to compile analysis data points into dataframe for csv output
    df_analysis = pd.DataFrame()
    df_analysis['analysis_description'] = str()
    df_analysis['analysis_result'] = str()
    df_analysis['result_data_type'] = str()

    # Add calculation results to dataframe
    df_analysis = pd.concat([df_analysis, df_results_correlation, df_results_lag, df_results_lead])

    ###############

    ## PLOTLY FIGURE CREATION ##

    # Create time series chart plotting the value of each economic indicator over time
    fig_time_series = VisualizationCreation.create_time_series_chart(df_preproc_stack_formatted, input_desc_1, input_desc_2)

    # Create table including the calculated analytics values
    fig_table = VisualizationCreation.create_table(df_analysis)
    
    ###############
    
    ## TABLEAU DASHBOARD PREP ##

    # Add run_date and created_by to stacked table and analysis table for use in tableau time series chart and table
    df_tableau_output_stacked = TableauOutputPrep.format_tableau_output(df_preproc_stack_formatted)
    df_tableau_analysis = TableauOutputPrep.format_tableau_output(df_analysis)

    ###############

    ## OUTPUT STEPS ##

    # Define output file names
    output_file_time_series_PDF = SetParameters.define_full_output_file_path_detailed(base_location, '02_Output', 'timeSeries', input_file_1, input_file_2, 'pdf')
    output_file_time_series_HTML = SetParameters.define_full_output_file_path_detailed(base_location, '02_Output', 'timeSeries', input_file_1, input_file_2, 'html')
    output_file_table_PDF = SetParameters.define_full_output_file_path_detailed(base_location, '02_Output', 'table', input_file_1, input_file_2, 'pdf')
    output_file_table_HTML = SetParameters.define_full_output_file_path_detailed(base_location, '02_Output', 'table', input_file_1, input_file_2, 'html')
    output_file_table_tableau_stacked_csv = SetParameters.define_full_output_file_path_generic(base_location, '02_Output', 'tableau_stacked_table','csv')
    output_file_table_tableau_analysis_csv = SetParameters.define_full_output_file_path_generic(base_location, '02_Output', 'tableau_analysis_table', 'csv')

    # Output HTML files
    fig_time_series.write_html(output_file_time_series_HTML)
    fig_table.write_html(output_file_table_HTML)
    
    # Output PDFs
    pio.write_image(fig_time_series, output_file_time_series_PDF, scale=1, width=1100, height=850)
    pio.write_image(fig_table, output_file_table_PDF, scale=1, width=1100, height=850)

    # Output CSVs
    df_tableau_output_stacked.to_csv(output_file_table_tableau_stacked_csv, sep=',', index=False)
    df_tableau_analysis.to_csv(output_file_table_tableau_analysis_csv, sep=',', index=False)

    # Open HTML in browser for user review
    os.system(f'start {output_file_table_HTML}')
    os.system(f'start {output_file_time_series_HTML}')

    # Show complete status in Anaconda Prompt
    print('Complete')

    # Print output message in application
    messagebox.showinfo(message=f'Comparison between "{input_desc_1}" and "{input_desc_2}" is complete! {results_correlation[1]}')

###############

### USER INTERFACE CREATION ###

root = Tk() # launch the application
root.title('Economic Data Analysis') # set the name for the application

# Create container for user interface
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Create question label and input box for the file location
ttk.Label(mainframe, text='Base Location:').grid(column=1, row=1, sticky=W)

baseLocation = StringVar()
baseLocation_entry = ttk.Entry(mainframe, width=50, textvariable=baseLocation)
baseLocation_entry.grid(column=2, row=1, sticky=(W, E))

# Create question label and input box for the first file name
ttk.Label(mainframe, text='File 1 Name (no file extension):').grid(column=1, row=2, sticky=W)

inputFile1 = StringVar()
inputFile1_entry = ttk.Entry(mainframe, width=50, textvariable=inputFile1)
inputFile1_entry.grid(column=2, row=2, sticky=(W, E))

# Create question label and input box for the description of the indicator in the first file
ttk.Label(mainframe, text='   File 1 Description:').grid(column=1, row=3, sticky=W)

inputFileDesc1 = StringVar()
inputFileDesc1_entry = ttk.Entry(mainframe, width=50, textvariable=inputFileDesc1)
inputFileDesc1_entry.grid(column=2, row=3, sticky=(W, E))

# Create question label and input box for the second file name
ttk.Label(mainframe, text='File 2 Name (no file extension):').grid(column=1, row=4, sticky=W)

inputFile2 = StringVar()
inputFile2_entry = ttk.Entry(mainframe, width=50, textvariable=inputFile2)
inputFile2_entry.grid(column=2, row=4, sticky=(W, E))

# Create question label and input box for the description of the indicator in the second file
ttk.Label(mainframe, text='   File 2 Description:').grid(column=1, row=5, sticky=W)

inputFileDesc2 = StringVar()
inputFileDesc2_entry = ttk.Entry(mainframe, width=50, textvariable=inputFileDesc2)
inputFileDesc2_entry.grid(column=2, row=5, sticky=(W, E))

# Create question label and input box for the lag periods
ttk.Label(mainframe, text='Lag Periods:').grid(column=1, row=6, sticky=W)

lagPeriods = IntVar(value=6) # default to 6-month lag period for current process
lagPeriods_entry = ttk.Entry(mainframe, width=50, textvariable=lagPeriods)
lagPeriods_entry.grid(column=2, row=6, sticky=(W, E))

# Create question label and input box for the lead periods
ttk.Label(mainframe, text='Lead Periods:').grid(column=1, row=7, sticky=W)

leadPeriods = IntVar(value=6) # default to 6-month lead period for current process
leadPeriods_entry = ttk.Entry(mainframe, width=50, textvariable=leadPeriods)
leadPeriods_entry.grid(column=2, row=7, sticky=(W, E))

# Create the button that is clicked to start process
ttk.Button(mainframe, text='Run Process', command=source_econ_data).grid(column=1, row=8, sticky=W)

for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

baseLocation_entry.focus()
inputFile1_entry.focus()
inputFile2_entry.focus()
root.bind('<Return>', source_econ_data)

root.mainloop()