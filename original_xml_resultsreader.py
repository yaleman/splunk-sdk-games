""" this is straight from the splunk SDK

- uses service.jobs.export, for speed
- runs as fast as it can, reading from the stream and writing it to disk as XML

"""
import json

from splunklib.results import Message, ResultsReader

import config
from utils import BaseTestHandler

testhandler = BaseTestHandler(
    config,
    job_runner="export",
    job_config={
        "adhoc_search_level": "verbose",
        "count": 0,
    },
)


RESULT_COUNT = 0
LASTRESULT = None
for result in ResultsReader(testhandler.run()):
    RESULT_COUNT += 1
    if isinstance(result, Message):
        print(json.dumps(result, indent=4, default=str))
    LASTRESULT = result
print(f"Results: {RESULT_COUNT}")
