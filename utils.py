""" some common things """

from splunklib import client  # type: ignore

TEST_SEARCH = "search index=_internal TERM(INFO) earliest=1644633000 latest=1644633600 | table *"

# pylint: disable=too-few-public-methods
class BaseTestHandler:
    """this allows one to centrally manage things"""

    def __init__(
        self,
        config,
        test_search=TEST_SEARCH,
        job_runner: str = "export",
        job_config: dict = None,
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

    def run(self):
        """runs the job, set self.job_runner to 'export' or 'create' depending on
        which job handler you want to use
        """
        runner = getattr(self.service.jobs, self.job_runner)
        return runner(self.test_search, **self.job_config)
