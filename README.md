# global_entry

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-312/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

Global Entry has notoriously long wait times to schedule an appointment. For popular airports (JFK/LAX/etc.) finding an appointment time can be extremely difficult. All one needs to do is run this script in the background to have a desktop notification pop up when a new appointment becomes available.

Can help find a scheduled appointment when other appointments are cancelled automatically. Less then 100 sloc!

# Installation
Python is installed via uv as are this projects dependencies:

```bash
billy@sa ~/global_entry % uv sync
```

# Run
Script defaults to JFK (`locationId = 5140`). Thus for

```bash
billy@sa ~/global_entry % uv run global_entry.py
```

available appointments will be notified for JFK. LAX is `locationId = 2720`, usage for LAX then is:

```bash
billy@sa ~/global_entry % uv run global_entry.py 2720
```

To find other airport `locationId`'s, ctrl+f `airports.json`
