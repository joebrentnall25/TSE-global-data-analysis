COPY requirements.txt /
RUN pip install -r /requirements.txt
 
RUN mkdir /TSE-global-data-analysis
WORKDIR /TSE-global-data-analysis
COPY ./ ./

ENV NAME TSE-GLOBAL-DATA-ANALYSIS
 
EXPOSE 8050
CMD ["python", "./index.py"]
