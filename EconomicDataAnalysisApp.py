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
        #BASE_LOCATION = input('Please enter base location:')
        baseLocationValue = str(baseLocation.get())
        #BASE_LOCATION = r'xxxxx' # input file location for testing
        #INPUT_FILE = input('Please enter input file name:')
        inputFileValue1 = str(inputFile1.get())
        inputFileValue2 = str(inputFile2.get())
        inputFileDescValue1 = str(inputFileDesc1.get())
        inputFileDescValue2 = str(inputFileDesc2.get())        
        #INPUT_FILE = r'xxxxxxx' # input file name for testing 


        inputFilePath1 = f'{baseLocationValue}\\01_Input\\{inputFileValue1}.csv'
        inputFilePath2 = f'{baseLocationValue}\\01_Input\\{inputFileValue2}.csv'
        outputLocation = f'{baseLocationValue}\\02_Output'

        # Source csv files as pandas dataframes
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

        df_inputStackFormatted = pd.DataFrame()
        df_inputStackFormatted['Date'] = df_inputStack['DATE']
        df_inputStackFormatted['Index Value'] = df_inputStack['value']
        df_inputStackFormatted['Variable Description'] = df_inputStack['variable_desc']

        ## PLOTLY FIGURE CREATION
    
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

        messagebox.showinfo(message='Economic Analysis Chart Complete!')
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

