# Web traffic generator

## About
This project aims to boost target websites' traffic via artificial visits. Multiple asyncio tasks will be forked, each of which simulates an actual web visit. The key components are:
- `targets.txt`: Sample target URLs. One line, one URL.
- `proxies.txt`: Sample web proxy configuration, with a format of `ip address:port`. One line, one config.
- `agents.txt`: User agent simulating the visit. One line, one UA definition.

## Instalation
1. Install `uv` from [official website](https://docs.astral.sh/uv/getting-started/installation/).
2. Setup the project by synchronizing the dependency: `uv sync`. This will create a virtual environment `.venv` at root folder, then install required packages.
3. Run the script: `uv run xtraffic.py [opts]`. See the Usage.

## Usage
```
xtraffic.py [-h] [--url-file URL_FILE] [--proxy-file PROXY_FILE] [--ua-file UA_FILE] [--stealth] [--proxy] [--debug] T N
```
where:
- `T`: total duration (in Seconds).
- `N`: total traffic visits to be generated.
- `url-file`: target URL config. file.
- `proxy-file`: proxy config. file.
- `ua-file`: user agent config. file. 
- `--proxy`: if set, then use proxied connection.
- `--stealth`: if set, then use `selenium-stealth`.
- `--debug`: if set, then print verbose debug messages.

### Example:
To generate 2 reqs/seconds proxied-traffic for 60 seconds:
```
uv run xtraffic.py 60 120 --url-file targets.txt --proxy-file proxies.txt --proxy
```