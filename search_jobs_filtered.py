# search_jobs_filtered.py
#
# filter the user's jobs

from splunklib import client  # type: ignore

import config

service = client.connect(
    host=config.host,
    username=config.username,
    password=config.password,
    autologin=True,
    app="yaleman_reports",
    owner=config.username,
)

print(f"with isSavedSearch=1: {len(service.jobs.list(search='isSavedSearch=1'))}")
print(f"with eventCount>1000: {len(service.jobs.list(search='eventCount>1000'))}")

print(f"with empty search: {len(service.jobs.list())}")
