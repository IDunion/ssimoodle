# VC-Api

API for LMS-credentials.

## Run

How to run the programm.

### Local

1. Clone repository
2. Go to VC_API/
3. Run (Python Version 3.9.6)

```console
pip install -r requirements.txt
python src/app.py
```

4. Browse <http://localhost:9080/apidocs/>

### Docker

1. Clone repository
2. Go to VC_API/
3. Run

```console
docker build -t vcapi .
docker run -d -p 9080:9080 vcapi
```

4. Browse <http://localhost:9080/apidocs/>

## Run tests

How to run the tests.

1. Clone repository
2. Go to VC_API/
3. Run (Python Version 3.9.6)

```console
pip install -r requirements.txt
python src/test_suite.py
```
