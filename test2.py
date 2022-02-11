""" test working with splunk """
import time
import json

import splunklib.client as client
from splunklib import results

import config

service = client.connect(
    host=config.host,
    username=config.username,
    password=config.password,
    autoLogin=True,
)

job = service.jobs.export(
    'search index=_internal host="*" TERM(INFO) earliest=-1h',
    adhoc_search_level='verbose',
    count=0,
    )
# time.sleep(1)
# start_time = time.time()
# while not job.is_done():
    # time.sleep(1)
    # print("Still waiting...")

# print(dir(job)
# job_done = time.time()

# print(json.dumps(job.state, indent=4))
results_returned = 0
reader = results.ResultsReader(job)
for result in reader:
    results_returned += 1
    if isinstance(result, dict):
        # print (f"Result: {result}")
        print(f"got result {results_returned=}")
    elif isinstance(result, results.Message):
        # print(f"Message: {result}")
        print(f"got message {results_returned=}")
    else:
        print(f"got: {type(result)} {results_returned=}")
    # print(f"is_preview = {reader.is_preview}")

print(f"Results: {results_returned}")
# print(f"Start time:\t{start_time}")
# print(f"Job Done:\t{job_done} ({job_done-start_time})")
# print(f"All Done:\t{final_time} ({final_time-start_time})")