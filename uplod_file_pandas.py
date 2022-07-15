import asyncio
import js
from js import document, FileReader
from pyodide import create_proxy

def read_complete(event):
# event is ProgressEvent
    content = document.getElementById("content");
    content.innerText = event.target.result


async def process_file(x):
    fileList = document.getElementById('upload').files

    for f in fileList:
        # reader is a pyodide.JsProxy
        reader = FileReader.new()

        # Create a Python proxy for the callback function
        onload_event = create_proxy(read_complete)

        #console.log("done")

        reader.onload = onload_event

        reader.readAsText(f)

    return

def main():
# Create a Python proxy for the callback function
    file_event = create_proxy(process_file)

    # Set the listener to the callback
    e = document.getElementById("upload")
    e.addEventListener("change", file_event, False)
