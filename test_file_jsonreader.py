""" test using a local file, to take splunk out of the equation

- using the JSONResultsReader test module
streams events and parses them into python dicts
"""
import io
import os
import json

from splunklib.results import JSONResultsReader, Message  # type: ignore

RESULT_COUNT = 0
PREVIEW_COUNT = 0
LASTRESULT = None

if not os.path.exists("outputfile.json"):
    raise FileNotFoundError(
        "Please run write_raw_json.py to generate a test file, or get a JSON export from somewhere",
        )

inputdata = io.BytesIO(open("outputfile.json", 'rb').read())
results = JSONResultsReader(inputdata)
for result in results:
    if isinstance(result, Message):
        print("message: ",json.dumps(result, indent=4, default=str))
    if result.get("preview"):
        PREVIEW_COUNT += 1
    else:
        RESULT_COUNT += 1
print(f"Results: {RESULT_COUNT}")
print(f"Preview results: {PREVIEW_COUNT}")
