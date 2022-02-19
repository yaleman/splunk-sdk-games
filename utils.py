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
        if self.job_runner == "export":
            return self.service.jobs.export(self.test_search, **self.job_config)
        elif self.job_runner == "oneshot":
            return self.service.jobs.oneshot(self.test_search, **self.job_config)
        elif self.job_runner == "create":
            return self.service.jobs.create(self.test_search, **self.job_config)
        else:
            raise ValueError(f"unsupported job_runner type: {self.job_runner}")

def validate_search(service: client.Service, searchstring: str) -> bool:
    try:
        service.parse(searchstring, parse_only=True)
        return True
    except client.HTTPError as e:
        raise ValueError("query '%s' is invalid:\n\t%s" % (TEST_SEARCH, str(e)), 2)