# VC-Api

API for LMS-credentials.

## Run

How to run the programm.

### Local

1. Clone repository
2. Run VC_API/src/app.py
3. Browse http://localhost:9080/apidocs/

### Docker

1. Clone repository
2. Go to VC_API/
3. Run

```console
docker build -t vcapi .
docker run -d -p 9080:9080 vcapi
```

4. Browse http://localhost:9080/apidocs/
