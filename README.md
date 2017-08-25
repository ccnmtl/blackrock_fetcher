# blackrock_fetcher [![Build Status](https://travis-ci.org/ccnmtl/blackrock_fetcher.svg?branch=master)](https://travis-ci.org/ccnmtl/blackrock_fetcher)
data fetcher and processor for Blackrock forest

### Python compatibility
This fetcher script was originally written to be compatible with
Python 2.6, since that's what's available on the cunix CentOS system.
I've started using pyenv on cunix, so we no longer have the Python 2.6
limitation.

Here's how to create a virtualenv for the blackrock fetcher and set
everything up for the cron job:

```
pyenv shell 2.7.13
python virtualenv.py --extra-search-dir=requirements/virtualenv_support ve
./ve/bin/pip install -r requirements.txt
```
