""" write out the raw JSON output data to disk
- uses service.jobs.export, for speed
- runs as fast as it can, reading from the stream and writing it to disk

"""

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

job = testhandler.run()

data = job.read(10240)
with open("outputfile.json", "wb") as file_handle:
    while data:
        file_handle.write(data)
        data = job.read(10240)
