"""this is trying to dump the raw results out of create

- uses service.jobs.create
- writes the raw result to disk

"""

import json
import logging
import os
import time

from splunklib import client  # ty:ignore[unresolved-import]

import config
from utils import TEST_SEARCH

INCREMENT = 10000

logging.basicConfig(level=getattr(logging, os.getenv("LOG_LEVEL", "INFO"), "INFO"))

logger = logging.getLogger(__name__)
logger.debug("Creating search '%s'", TEST_SEARCH)


def main() -> None:
    """main func"""
    service = client.connect(
        host=config.host,
        username=config.username,
        password=config.password,
        autoLogin=True,
    )
    job = service.jobs.create(
        TEST_SEARCH, adhoc_search_level="verbose", max_count=1000000000
    )

    while not (job.is_done() and job.is_ready()):
        time.sleep(1)
        logger.debug("Still waiting...")
    logger.debug("job.is_done()=%s", job.is_done())
    logger.debug("job.is_ready()=%s", job.is_ready())

    # in my test data, there's 113,624 events
    maxresults = int(job.state["content"]["resultCount"])
    logger.debug("looking to get %s results", maxresults)
    with open("outputfile_create.json", "wb") as file_handle:
        offset = 0
        total_results = 0
        while offset < maxresults:
            logger.debug(
                "Working on offset=%s, total_results=%s", offset, total_results
            )
            results = job.results(output_mode="json", offset=offset, count=INCREMENT)
            results_content = results.read().decode("utf-8")
            resultdata = json.loads(results_content)
            if resultdata.get("results") and not resultdata.get("preview"):
                total_results += len(resultdata["results"])
            else:
                logger.debug("No results in this block")

            file_handle.write(f"{results_content}\n".encode())
            offset = offset + INCREMENT


if __name__ == "__main__":
    main()
