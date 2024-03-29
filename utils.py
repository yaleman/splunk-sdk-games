""" some common things """

from time import time
from typing import Any, Optional

from splunklib import client  # type: ignore

TEST_SEARCH_TIME_LATEST = round(time(), 3) - 30  # 30 seconds ago
TEST_SEARCH_TIME_EARLIEST = TEST_SEARCH_TIME_LATEST - 300

TEST_SEARCH = f"search index=_internal TERM(INFO) earliest={TEST_SEARCH_TIME_EARLIEST} latest={TEST_SEARCH_TIME_LATEST} | table *"


# pylint: disable=too-few-public-methods
class BaseTestHandler:
    """this allows one to centrally manage things"""

    def __init__(
        self,
        config: Any,
        test_search: str = TEST_SEARCH,
        job_runner: str = "export",
        job_config: Optional[dict[str, Any]] = None,
    ):
        """config is an object with host/username/password"""
        self.service = client.connect(
            host=config.host,
            username=config.username,
            password=config.password,
            autoLogin=True,
        )
        self.test_search = test_search
        self.job_runner = job_runner
        if job_config:
            self.job_config = job_config
        else:
            self.job_config = {
                "adhoc_search_level": "verbose",
                "count": 0,
            }

    def run(self) -> Any:
        """runs the job, set self.job_runner to 'export' or 'create' depending on
        which job handler you want to use
        """
        if self.job_runner == "export":
            return self.service.jobs.export(self.test_search, **self.job_config)
        if self.job_runner == "oneshot":
            return self.service.jobs.oneshot(self.test_search, **self.job_config)
        if self.job_runner == "create":
            return self.service.jobs.create(self.test_search, **self.job_config)
        raise ValueError(f"unsupported job_runner type: {self.job_runner}")


def validate_search(service: client.Service, searchstring: str) -> bool:
    """validates your search"""
    try:
        service.parse(searchstring, parse_only=True)
        return True
    except client.HTTPError as error_message:
        # pylint: disable=raise-missing-from
        raise ValueError(f"query '{TEST_SEARCH}' is invalid:{error_message}")
