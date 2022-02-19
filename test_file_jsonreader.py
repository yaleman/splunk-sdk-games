""" test using a local file, to take splunk out of the equation

- using the JSONResultsReader test module
streams events and parses them into python dicts
"""
import io
import os

from splunklib.results import JSONResultsReader, Message  # type: ignore

MESSAGE_COUNT = 0
PREVIEW_COUNT = 0
RESULT_COUNT = 0

if not os.path.exists("outputfile.json"):
    raise FileNotFoundError(
        "Please run write_raw_json.py to generate a test file, or get a JSON export from somewhere",
    )

with io.BytesIO(open("outputfile.json", "rb").read()) as inputdata:
    results = JSONResultsReader(inputdata)
    for result in results:
        if isinstance(result, Message):
            MESSAGE_COUNT += 1
            continue
        if results.is_preview:
            PREVIEW_COUNT += 1
        else:
            RESULT_COUNT += 1
print(f"{RESULT_COUNT=}")
print(f"{MESSAGE_COUNT=}")
print(f"{PREVIEW_COUNT=}")
