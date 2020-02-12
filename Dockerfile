FROM python:3.7

RUN mkdir /gdat
WORKDIR /gdat

# Add enviroment variables for azure storage
ARG AZURE_STORAGE_CONNECTION_STRING

# pip install via requirements.txt file
ADD requirements.txt /gdat/
RUN pip install -r requirements.txt
ADD . /gdat/

# expose port for connections
EXPOSE 8050

# start gunicorn production server.
CMD ["gunicorn", "-b", "0.0.0.0:8050", "index:application"]
