""" testing modification of saved search permissions """
import json
from splunklib import client  # type: ignore

import config


def main() -> None:
    """ does things """
    print("Logging in...")
    splunk = client.connect(
        host=config.host,
        port=8089,
        scheme="https",
        username=config.username,
        password=config.password,
        )

    owner = config.username
    app = config.app
    searchname = "test search"

    acl_modifications = {
        'modifiable': True,
        'app': config.app,
        'owner': owner,
        'sharing': "user",
        "perms.read" : "*",
        }
    print("passing the following:")
    print(json.dumps(acl_modifications, indent=4))

    resp = splunk.post(
        f"/servicesNS/{owner}/{app}/saved/searches/{searchname}/acl",
        body=acl_modifications
        )
    print(f"Response object: {resp}")
    print(f"Response body: {resp.body}")

if __name__ == "__main__":
    main()
