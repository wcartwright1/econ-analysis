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

def sourceEconData(*args):
    try:
        ## FILE LOCATION SETUP ##

        # Source base location from user input in application
        baseLocationValue = str(baseLocation.get())
        # Source input file 1 name from user input in application
        inputFileValue1 = str(inputFile1.get())
        # Source input file 2 name from user input in application
        inputFileValue2 = str(inputFile2.get())
        # Label input file 1 descriptions from user input in application --> flows into final charts
        inputFileDescValue1 = str(inputFileDesc1.get())
        # Label input file 2 descriptions from user input in application --> flows into final charts
        inputFileDescValue2 = str(inputFileDesc2.get())

        # Define file paths based on user input in application. Input files and output files are stored in seperate folders.
        inputFilePath1 = f'{baseLocationValue}\\01_Input\\{inputFileValue1}.csv'
        inputFilePath2 = f'{baseLocationValue}\\01_Input\\{inputFileValue2}.csv'
        outputLocation = f'{baseLocationValue}\\02_Output'

        ## DATA SOURCING AND PRE-PROCESSING ##

        # Source csv files as pandas dataframes. These files can be any downloaded file from FRED with the column format DATE, {some_value} 
        df_1input = pd.read_csv(inputFilePath1, sep=',')
        df_2input = pd.read_csv(inputFilePath2, sep=',')

        # Pre-process data tables
        df_1inputPreproc = df_1input.copy() # create copy of initial dataframe for transformations, as initial table will be output later for dashboard
        dict_df1Columns = df_1inputPreproc.columns # return column list in dictionary to determine variables
        df_1inputPreproc = df_1inputPreproc.melt(id_vars=dict_df1Columns[0], value_vars=dict_df1Columns[1]) # update data model from wide to long to allow for the use of different economic indicators
        df_1inputPreproc['variable_desc'] = inputFileDescValue1 # add additional column for economic indicator variable name for presentation

        df_2inputPreproc = df_2input.copy() # create copy of initial dataframe for transformations, as initial table will be output later for dashboard 
        dict_df2Columns = df_2inputPreproc.columns # return column list in dictionary to determine variables
        df_2inputPreproc = df_2inputPreproc.melt(id_vars=dict_df2Columns[0], value_vars=dict_df2Columns[1]) # update data model from wide to long to allow for the use of different economic indicators
        df_2inputPreproc['variable_desc'] = inputFileDescValue2 # add additional column for economic indicator variable name for presentation

        # Stack dataframes for plotting and assign formatted values
        df_inputStack = pd.concat([df_1inputPreproc, df_2inputPreproc])

        df_inputStackFormatted = pd.DataFrame() # create empty dataframe to store formatted table
        df_inputStackFormatted['Date'] = df_inputStack['DATE']
        df_inputStackFormatted['Index Value'] = df_inputStack['value']
        df_inputStackFormatted['Variable Description'] = df_inputStack['variable_desc']

        # Join dataframes to create a wide-format table for period-specific analysis
        df_inputJoin = df_1inputPreproc.merge(df_2inputPreproc,
                                              on='DATE', # date used as unique key
                                              how='inner' # only output information where the unique key exists in each dataset, as some datasets are either available on different cadences or from different time periods
                                              )
        
        ## Calculations ##

        # Calculate correlation coefficient (r)
        result_correlation = df_inputJoin['value_x'].corr(df_inputJoin['value_y']) # in numpy --> np.corrcoef(df_inputJoin['value_x'], df_inputJoin['value_y'])[0,1]
        message_result_correlation = f'Correlation coefficient = {result_correlation:.4f}.' # format the correlation results (to 4 decimal places) for output message

        # Calculate number of time periods available for comparison and in each dataset
        #len_df1 = len(df_1inputPreproc)
        #minYear_df1 = df_1inputPreproc['DATE'].min().year
        #maxYear_df1 = df_1inputPreproc['DATE'].max().year
        #len_df2 = len(df_2inputPreproc)
        #minYear_df2 = df_2inputPreproc['DATE'].min().year
        #maxYear_df2 = df_2inputPreproc['DATE'].max().year
        #len_dfJoined = len(df_inputJoin)
        #minYear_dfJoined = df_inputJoin['DATE'].min().year
        #maxYear_dfJoined = df_inputJoin['DATE'].max().year
        
       # message_timeHorizon = (f'''{inputFileDescValue1} table has {len_df1} records from {minYear_df1} to {maxYear_df1}.
        #                       {inputFileDescValue2} table has {len_df2} records from {minYear_df2} to {maxYear_df2}.
         #                      Joined table has {len_dfJoined} records from {minYear_dfJoined} to {maxYear_dfJoined}.
          #                     '''
           #                    )
        # Combine messages for final results message.
        message_outputComplete = f'{message_result_correlation}'

        ## PLOTLY FIGURE CREATION ##
    
        # Create simple line chart plotting the value of each economic indicator over time
        fig_simpleLineChart = px.line(df_inputStackFormatted, 
                                    x='Date', 
                                    y='Index Value', 
                                    color='Variable Description', 
                                    title=f'{inputFileDescValue1} & {inputFileDescValue2}'
                                    )
        
        # Create simple table including the raw values from the data tables
        fig_simpleTable = pgo.Figure(
                        data=[pgo.Table(
                        header=dict(values=list(df_inputStackFormatted.columns), 
                                    fill_color='skyblue', 
                                    align='left'),
                        cells=dict(values=[df_inputStackFormatted['Date'], df_inputStackFormatted['Index Value'], df_inputStackFormatted['Variable Description']],
                                    fill_color='slategray',
                                    align='left')
                                )                       
                             ]
                                    )
        
        ## OUTPUT STEPS
        # Define output file names
        outputPDF_simpleLineChart = f'{outputLocation}\\simpleLineChart.pdf'
        outputHTML_simpleLineChart = f'{outputLocation}\\simpleLineChart.html'
        outputPDF_simpleTable = f'{outputLocation}\\simpleTable.pdf'
        outputHTML_simpleTable = f'{outputLocation}\\simpleTable.html'

        # Output interactive simple line chart to html
        fig_simpleLineChart.write_html(outputHTML_simpleLineChart)

        # Output interactive table to html
        fig_simpleTable.write_html(outputHTML_simpleTable)
                
        # Output simple line chart image to PDF
        pio.write_image(fig_simpleLineChart, outputPDF_simpleLineChart)

        # Output simple table image to PDF
        pio.write_image(fig_simpleTable, outputPDF_simpleTable)

        # Open html in browser
        #time.sleep(5)
        os.system(f'start {outputHTML_simpleTable}')
        os.system(f'start {outputHTML_simpleLineChart}')

        messagebox.showinfo(message=message_outputComplete)
        print('Complete')
    except:
        messagebox.showinfo(message='Error - please confirm file path and file name')
        print('ErrorCheck')


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

ttk.Button(mainframe, text="Source Econ Data", command=sourceEconData).grid(column=1, row=6, sticky=W)

for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

baseLocation_entry.focus()
inputFile1_entry.focus()
inputFile2_entry.focus()
root.bind("<Return>", sourceEconData)

root.mainloop()

