# global_entry
Global Entry has notoriously long wait times to schedule an appointment. For popular airports (JFK/LAX/etc.) finding an appointment time can be extremely difficult. All one needs to do is run this script in the background to have a desktop notification pop up when a new appointment becomes available. 

Can help find a scheduled appointment when other appointments are cancelled automatically. Less then 50 sloc!

# Download
```
cd /path/to/desired/folder
git clone https://github.com/billy-doyle/global_entry.git
cd global_entry/
python3 -m venv ./venv
source venv/bin/activate
pip3 install -r requirements.txt
```

# Run
Script defaults to JFK (`locationId = 5140`). Thus for

```
python3 global_entry.py
```

available appointments will be notified for JFK. LAX is `locationId = 2720`, usage for LAX then is:

```
python3 global_entry.py 2720
```

To find other airport `locationId`'s, ctrl+f `airports.json`
