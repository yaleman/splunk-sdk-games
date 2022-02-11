""" test working with splunk - streams events and parses them into python dicts """
import io
import json
import splunklib.client as client

import config

service = client.connect(
    host=config.host,
    username=config.username,
    password=config.password,
    autoLogin=True,
)

job = service.jobs.export(
    'search index=_internal host="*" TERM(INFO) earliest=-10m',
    adhoc_search_level='verbose',
    count=0,
    output_mode="json",
    enable_lookups=True,
    )

results = 0
for line in io.BufferedReader(job).readlines():
    results += 1
    el = json.loads(line)
print(f"Total results: {results}")
