# blackrock_fetcher [![Actions Status](https://github.com/ccnmtl/plexus/workflows/build-and-test/badge.svg)](https://github.com/ccnmtl/plexus/actions)
data fetcher and processor for Blackrock forest

### Python compatibility
This fetcher script was originally written to be compatible with
Python 2.6, since that's what was available on cunix at the time.
This script is now deployed using pyenv on cunix, so we no longer have
the Python 2.6 limitation.

Here's how to create a virtualenv for the blackrock fetcher and set
everything up for the cron job:

```
pyenv local 3.6.9
python -m venv ve
./ve/bin/pip install -r requirements.txt
```
