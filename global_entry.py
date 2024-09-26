# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "plyer>2",
#     "pyobjus>=1.2.3",
#     "requests<3",
# ]
# ///
import argparse
import platform
import subprocess
import time

import requests
from plyer import notification
from requests.adapters import HTTPAdapter, Retry


class CustomHTTPAdapter(HTTPAdapter):
    def __init__(self, timeout=None, *args, **kwargs):
        self.timeout = timeout
        super().__init__(*args, **kwargs)

    def send(self, *args, **kwargs):
        kwargs["timeout"] = self.timeout
        return super().send(*args, **kwargs)


def create_session(
    location_id,
    timeout=10,
    num_retries=5,
    backoff_factor=0.1,
    status_forcelist=(404, 500, 502, 503, 504),
):
    session = requests.Session()
    agent = (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/85.0.4183.102 Safari/537.36"
    )
    session.headers.update({"User-Agent": agent})
    params = {"orderBy": "soonest", "limit": 1, "locationId": location_id, "minimum": 1}
    session.params.update(params)

    retries = Retry(
        total=num_retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )

    session.mount("http://", CustomHTTPAdapter(timeout=timeout, max_retries=retries))
    session.mount("https://", CustomHTTPAdapter(timeout=timeout, max_retries=retries))

    return session


def notify(message):
    if platform.system() == "Darwin":
        subprocess.run(
            [f'osascript -e \'display notification "{message}" with title "global_entry.py"\''],
            shell=True,
        )
    else:
        notification.notify(title="global_entry.py", message=message, timeout=3)


def fetch(session):
    url = "https://ttp.cbp.dhs.gov/schedulerapi/slots"
    r = session.get(url)
    if not r.ok:
        r.raise_for_status()

    return r.json()


def main(location_id):
    set_ = set()
    session = create_session(location_id)
    while True:
        resp = fetch(session)
        if len(resp) != 0:
            message = "Global Entry Appt @ " + resp[0]["startTimestamp"]
            if message not in set_:
                print(message)
                notify(message)
                set_.add(message)

        time.sleep(5)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="default to JFK, see airports.json for other locations (LAX 2720, SFO 5446)"
    )
    parser.add_argument(
        "location_id", nargs="?", default=5140, help="An optional integer value", type=int
    )
    args = parser.parse_args()
    main(args.location_id)
