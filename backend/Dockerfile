FROM python:3.8.5
WORKDIR /back
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
CMD gunicorn foodgram_.wsgi:application --bind 0.0.0.0:8000