""" test working with splunk

- using the JSONResultsReader test module
streams events and parses them into python dicts
"""
import json

from splunklib.results import JSONResultsReader, Message  # type: ignore

import config
from utils import BaseTestHandler

testhandler = BaseTestHandler(
    config,
    job_runner="export",
    job_config={
        "adhoc_search_level": "verbose",
        "count": 0,
        "output_mode": "json",
    },
)

RESULT_COUNT = 0
LASTRESULT = None
for result in JSONResultsReader(testhandler.run()):
    RESULT_COUNT += 1
    if isinstance(result, Message):
        print("message: ",json.dumps(result, indent=4, default=str))
    LASTRESULT = result
print(f"Results: {RESULT_COUNT}")
