# WIKIDATA VISUALIZATION SERVICE

This small webservice allows a user to visually explore the relationship between different Wikidata entities.

## Dependencies

- Python 3.5+
- Python-VirtualEnv
- Redis

## Installation

- Clone the repository: 

```bash
git clone git@github.com:molguin92/WikidataViz.git
```

- Create a virtual environment to install the Python libraries and activate it:

```bash
cd WikidataViz
virtualenv --python=python3.5 ./venv
source venv/bin/activate
```

- Install the required Python dependencies:

```bash
pip install -r requirements.txt
```

- Run the included tests:

```bash
python ./run_tests.py
```
- Launch the Redis Queue worker process (recommendation: run it in a separate terminal or in a screen session for best results):

```bash
rq worker &
```

- Launch the service using Gunicorn:

```bash
gunicorn --workers 3 --bind 0.0.0.0:5000 wikidataviz.wsgi:app --error-logfile errors.log
```

- Finally, go to to http://0.0.0.0:5000/Q1 to check that the service is running.

