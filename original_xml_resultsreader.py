""" this is straight from the splunk SDK

- uses service.jobs.export, for speed
- runs as fast as it can, reading from the stream and writing it to disk as XML

"""

from splunklib import results  # type: ignore

import config
from utils import BaseTestHandler


testhandler = BaseTestHandler(
    config,
    job_runner="export",
)

RESULTS_COUNT = 0
reader = results.ResultsReader(testhandler.run())
for result in reader:
    RESULTS_COUNT += 1
    if isinstance(result, dict):
        # print(f"got result {results_returned=}")
        pass  # got a result
    elif isinstance(result, results.Message):
        print(f"got message {RESULTS_COUNT=}")
    else:
        print(f"got: {type(result)} {RESULTS_COUNT=}")

print(f"Results: {RESULTS_COUNT}")
