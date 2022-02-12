# splunk-sdk-games

## Configuration

Copy `config.py.example` to `config.py` and set the username/password/host fields.

## Usage

Once you've cloned this repository, grab a copy of my fork of the SDK:

```shell
git clone https://github.com/yaleman/splunk-sdk-python/
```

Then install things:

```shell
python -m pip install poetry
poetry install 
```

Either run the poetry shell so you're in the virtualenv:

```shell
poetry shell
python test1.py
```

OR use poetry to wrap it:
```shell
poetry run python test1.py
```
