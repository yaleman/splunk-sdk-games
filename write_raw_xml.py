""" this is straight from the splunk SDK

- uses service.jobs.export, for speed
- runs as fast as it can, reading from the stream and writing it to disk as XML

"""

import config
from utils import BaseTestHandler

testhandler = BaseTestHandler(
    config,
    job_runner="export",
)

job = testhandler.run()

data = job.read(10240)
with open("outputfile.xml", "wb") as file_handle:
    while data:
        file_handle.write(data)
        data = job.read(10240)
