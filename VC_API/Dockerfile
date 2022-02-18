FROM python:3

WORKDIR /app

# Install packages 
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./src /app/src

CMD [ "python", "src/app.py" ]