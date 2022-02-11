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

job = service.jobs.create(
    'search index=_internal host="*" TERM(INFO) earliest=-1h',
    adhoc_search_level='verbose',
    )
time.sleep(1)
start_time = time.time()
while not job.is_done():
    time.sleep(1)
    print("Still waiting...")
# print(dir(job)
job_done = time.time()

print(json.dumps(job.state, indent=4))
reader = results.ResultsReader(job.events())
for result in reader:
    if isinstance(result, dict):
        print (f"Result: {result}")
    elif isinstance(result, results.Message):
        print(f"Message: {result}")
    print(f"is_preview = {reader.is_preview}")

final_time = time.time()
print(f"Start time:\t{start_time}")
print(f"Job Done:\t{job_done} ({job_done-start_time})")
print(f"All Done:\t{final_time} ({final_time-start_time})")