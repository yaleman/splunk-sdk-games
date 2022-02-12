""" this is straight from the splunk SDK

- uses service.jobs.create, which makes the search head write the results to disk, THEN return them
- uses results.ResultsReader
    - uses all your CPU

"""
import time
import json

from splunklib import results  # type: ignore

import config
from utils import BaseTestHandler

testhandler = BaseTestHandler(
    config,
    job_runner="create",
)

job = testhandler.run()
time.sleep(1)
start_time = time.time()
while not job.is_done():
    time.sleep(1)
    print("Still waiting...")
job_done = time.time()

print(json.dumps(job.state, indent=4))
reader = results.ResultsReader(job.events())
for result in reader:
    if isinstance(result, dict):
        print(f"Result: {result}")
    elif isinstance(result, results.Message):
        print(f"Message: {result}")
    print(f"is_preview = {reader.is_preview}")

final_time = time.time()
print(f"Start time:\t{start_time}")
print(f"Job Done:\t{job_done} ({job_done-start_time})")
print(f"All Done:\t{final_time} ({final_time-start_time})")
