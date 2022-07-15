import asyncio
from js import document, console
from pyodide import create_proxy
from io import StringIO
import pandas as pd

upload_file = ''

def clear_data():
    document.getElementById("filename").innerHTML = ''
    document.getElementById("filesize").innerHTML = ''
    document.getElementById('content').innerHTML = ''
    document.getElementById('container').innerHTML = ''

async def process_file(event):
    clear_data()
    fileList = event.target.files.to_py()

    for file in fileList:
        document.getElementById("filename").innerHTML = 'File Name: ' + str(file.name)
        document.getElementById("filesize").innerHTML = 'File Size: ' + str(file.size)
        data = await file.text()
        document.getElementById("content").innerHTML = data
        plot_data(data)
 
def setup_upload_button(IdName):
	# Create a Python proxy for the callback function
	file_event = create_proxy(process_file)
 
	# Set the listener to the callback
	e = document.getElementById(IdName)
	e.addEventListener("change", file_event, False)

def plot_data(data):
    df = pd.read_csv(StringIO(data))
    html = df.to_html()
    document.getElementById("DataFrame").innerHTML = html


 