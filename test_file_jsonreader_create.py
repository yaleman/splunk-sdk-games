""" test using a local file, to take splunk out of the equation

- using the JSONResultsReader test module
streams events and parses them into python dicts
"""
import io
import os
from pathlib import Path
import json

from splunklib.results import JSONResultsReader, Message  # type: ignore

RESULT_COUNT = 0
PREVIEW_COUNT = 0
LASTRESULT = None

file_to_read = Path("outputfile_create.json")

if not file_to_read.exists():
    raise FileNotFoundError(
        "Please run write_raw_json_job_create.py to generate a test file, or get a JSON export from somewhere",
        )

inputdata = io.BytesIO(file_to_read.open('rb').read())
results = JSONResultsReader(inputdata)
for result in results:
    if isinstance(result, Message):
        print("message: ",json.dumps(result, indent=4, default=str))
        continue
    if result.get("preview"):
        PREVIEW_COUNT += 1
    else:
        RESULT_COUNT += 1
print(f"Results: {RESULT_COUNT}")
print(f"Preview results: {PREVIEW_COUNT}")
