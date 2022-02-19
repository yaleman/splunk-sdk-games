""" this is trying to dump the raw results out of create

- uses service.jobs.create
- writes the raw result to disk

"""
import json
import logging
import os
import time


from splunklib import client

import config
from utils import TEST_SEARCH

service = client.connect(
        host=config.host,
        username=config.username,
        password=config.password,
        autoLogin=True,
    )

logging.basicConfig(level=getattr(logging, os.getenv("LOG_LEVEL","INFO"),"INFO"))

logging.debug(f"Creating search '{TEST_SEARCH}'")
job = service.jobs.create(TEST_SEARCH,adhoc_search_level="verbose",max_count=1000000000)

while not (job.is_done() and job.is_ready()):
    time.sleep(1)
    logging.debug("Still waiting...")
logging.debug(f"{job.is_done()=}")
logging.debug(f"{job.is_ready()=}")

increment = 10000
offset = 0

# in my test data, there's 113,624 events
maxresults = int(job.state["content"]["resultCount"])
total_results = 0
logging.debug(f"looking to get {maxresults} results")
with open("outputfile_create.json", "wb") as file_handle:
    while offset < maxresults:
        logging.debug(f"Working on {offset=}, {total_results=}")
        results = job.results(output_mode="json", offset=offset, count=increment)
        results_content = results.read().decode('utf-8')
        resultdata = json.loads(results_content)
        if resultdata.get("results") and not resultdata.get("preview"):
            total_results += len(resultdata["results"])
        else:
            logging.debug("No results in this block")

        file_handle.write(f"{results_content}\n".encode("utf-8"))
        offset += increment
