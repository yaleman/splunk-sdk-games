""" test using a local file, to take splunk out of the equation

- using the JSONResultsReader test module
streams events and parses them into python dicts
"""
import io
import os

from splunklib.results import ResultsReader, Message  # type: ignore

RESULT_COUNT = 0
PREVIEW_COUNT = 0
MESSAGE_COUNT = 0

if not os.path.exists("outputfile.xml"):
    raise FileNotFoundError(
        "Please run write_raw_xml.py to generate a test file, or get a XML export from somewhere",
    )

with io.BytesIO(open("outputfile.xml", "rb").read()) as inputdata:
    results = ResultsReader(inputdata)
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
