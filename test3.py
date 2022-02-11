""" test working with splunk - writes an XML file to disk s"""
import io
# import json
# import time
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
    'search index=_internal host="*" TERM(INFO) earliest=-10m',
    adhoc_search_level='verbose',
    count=0,
    )

data = job.read(1024)
with open('outputfile.xml', 'wb') as file_handle:
    while data:
        file_handle.write(data)
        data = job.read(1024)
