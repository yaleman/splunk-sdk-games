""" write out the raw JSON output data to disk
- uses service.jobs.export, for speed
- runs as fast as it can, reading from the stream and writing it to disk

config is a python file with the following variables:
- host
- username
- password

"""

from time import time

from splunklib import client  # type: ignore

import config


TEST_SEARCH_TIME_LATEST = round(time(),3)-30 # 30 seconds ago
TEST_SEARCH_TIME_EARLIEST = TEST_SEARCH_TIME_LATEST - 300 # five minutes before that

test_search = (
    f"""search index=_internal TERM(INFO) earliest={TEST_SEARCH_TIME_EARLIEST} latest={TEST_SEARCH_TIME_LATEST}
    | table *
    """
)

# here we start the connection to the splunk server, ensuring that our login works
service = client.connect(
            host=config.host,
            username=config.username,
            password=config.password,
            autoLogin=True,
        )

job_config = {
    # more fields more better
    "adhoc_search_level": "verbose",
    # unlimited results!
    "count": 0,
}

# this is where we start the job
job = service.jobs.oneshot(test_search, **job_config)

# start reading the first block from the response
data = job.read(10240)

with open("outputfile.json", "wb") as file_handle:
    # write to disk in a loop
    while data:
        file_handle.write(data)
        data = job.read(10240)

# done!
