# Network Destruction

## Requirements

* Python 3.6 or better
* `setuptools` (included in the Python distribution)
* `pip` (included in the Python distribution)
* `venv` (included in the Python distribution)

## Setup

1. Create a new virtualenv with
   ```
   python -m venv env
   ```

2. Activate the virtualenv with
   ```
   source env/bin/activate
   ```

3. Install the package in editable mode
   ```
   pip install --editable .
   ```

## Linting

From the virtualenv:

```
pip install flake8
flake8
```

## Type checking

From the virtualenv:

```
pip install mypy
env/bin/mypy --ignore-missing-imports -p network_destruction
```

## Run ranking experiment

From the virtualenv:

```
python -m network_destruction
```
