FROM python:3.7

RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app/
RUN pip install -r requirements.txt
ADD . /app/

# port for connections
EXPOSE 8050
# start gunicorn production server. 4 worker threads.
CMD ["gunicorn", "-b", "0.0.0.0:8050", "index:server"]
