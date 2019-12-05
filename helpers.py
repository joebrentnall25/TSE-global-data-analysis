import base64
import io
import pandas as pd


def parse_file_to_df(contents, filename, delim):
    """ Read a csv or xls file by content string, filename and delimitter, 
    and return the result as a pandas dataframe""" 
    content_type, content_string = contents.split(delim)
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
    return df
