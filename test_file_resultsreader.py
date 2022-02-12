""" test using a local file, to take splunk out of the equation

- using the JSONResultsReader test module
streams events and parses them into python dicts
"""
import io
import os
import json

from splunklib.results import ResultsReader, Message  # type: ignore

RESULT_COUNT = 0
PREVIEW_COUNT = 0
LASTRESULT = None

if not os.path.exists("outputfile.xml"):
    raise FileNotFoundError(
        "Please run write_raw_xml.py to generate a test file, or get a XML export from somewhere",
        )

inputdata = io.BytesIO(open("outputfile.xml", 'rb').read())
results = ResultsReader(inputdata)
for result in results:
    if isinstance(result, Message):
        print("message: ",json.dumps(result, indent=4, default=str))
    if results.is_preview:
        PREVIEW_COUNT += 1
    else:
        RESULT_COUNT += 1
    # LASTRESULT = result
print(f"Results: {RESULT_COUNT}")
print(f"Preview results: {PREVIEW_COUNT}")
