""" test working with splunk - streams events and parses them into python dicts """
import io
import json

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

RESULTS = 0
for line in io.BufferedReader(testhandler.run()).readlines():
    RESULTS = RESULTS + 1
    el = json.loads(line)
print(json.dumps(el, indent=4))
print(f"Total results: {RESULTS}")
