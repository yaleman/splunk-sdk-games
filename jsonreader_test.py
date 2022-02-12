""" test working with splunk - using the JSONResultsReader test module
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
    if "preview" not in result or result["preview"] is False:
        # print(".", end=".")
        pass
    else:
        print("p")
    # if results % 100 == 0:
    # print("\n")
    if isinstance(result, Message):
        print(json.dumps(result, indent=4))
    LASTRESULT = result
    # sys.stdout.flush()
print(json.dumps(LASTRESULT, indent=4))
print(f"Total results: {RESULT_COUNT}")
