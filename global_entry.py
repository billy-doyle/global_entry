import time
import requests
from plyer import notification

def fetch(location_id):

    agent = (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/85.0.4183.102 Safari/537.36"
    )
    params = {
        'orderBy': 'soonest',
        'limit': 1,
        'locationId': location_id,
        'minimum': 1
    }
    url = 'https://ttp.cbp.dhs.gov/schedulerapi/slots'
    r = requests.get(url, params=params, headers={'user-agent': agent})
    if not r.ok:
        r.raise_for_status()

    return r.json()

def main(location_id):

    set_ = set()
    ct = 0
    while True:
        ct += 1
        if ct % 100 == 0:
            print(ct, time.ctime())

        try:
            resp = fetch(location_id)
        except requests.RequestException as e:
            print(f'Exception at {time.ctime()}, sleeping...')
            time.sleep(60)

        if len(resp) == 0:
            time.sleep(5)
        else:
            message = 'Global Entry Appt @ ' + resp[0]['startTimestamp']
            if message not in set_:
                print(message)
                notification.notify(title='global_entry.py', message=message, timeout=3)
                set_.add(message)

            time.sleep(5)


if __name__ == '__main__':
    # JFK 5140
    # LAX 2720
    # see airports.json for other locations
    main(5140)
