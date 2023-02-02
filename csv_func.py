import csv , os , json 
import pandas as pd

def SaveAsCsv(CSV_FILE_NAME,list_of_rows):
    try:
        list_of_rows = [str(item).replace('\n','').replace('  ',' ').strip() for item in list_of_rows]
        print('\nSaving CSV Result')
        with open(CSV_FILE_NAME, 'a',  newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(list_of_rows)
            print("rsults saved successully")
    except PermissionError:
        print("Please make sure outputV3.csv is closed \n")
        
def CSVTOJSON(csv_file_name,format_text = False,delimiter=','):
    try:
        print('Converting CSV to Json')
        with open(csv_file_name, encoding='utf-8') as f:
            rows = [[val.strip() for val in r.split(delimiter)] for r in f.readlines()]
        json_obj = []
        headers = rows[0]
        for row in rows[1:]:
            if format_text:
                json_obj.append({rows[0][i]:row[i].strip() for i in range(0,len(row))})
            else:
                json_obj.append({rows[0][i]:row[i].strip() for i in range(0,len(row))})
        return headers , json_obj
    except Exception as e:
        print(e)

def SaveAsText(info,FILE_NAME,mode='a'):
    try:
        print('Saving Results To Text File')
        with open(FILE_NAME, mode=mode) as f:
            f.write(info + '\n') if mode == 'a' else f.write(info)
    except PermissionError:
        print("Please make sure {} is closed \n".format(FILE_NAME))
    except UnicodeEncodeError:
        print('Saving Results with encoding')
        with open(FILE_NAME, mode=mode,encoding='utf-8') as f:
            f.write(info + '\n') if mode == 'a' else f.write(info)

def SaveAsJson(CSV_FILE_NAME):
    print('Saving CSV to Json')
    FILE_NAME       = CSV_FILE_NAME.replace('.csv','.json')
    final           = CSVTOJSON(CSV_FILE_NAME)
    with open(FILE_NAME,'w') as f:
        f.write(json.dumps(final))
        

def SaveHeaders(CSV_FILE_NAME,header_list):    
    if os.path.isfile(CSV_FILE_NAME) and os.access(CSV_FILE_NAME, os.R_OK):
        print('File {} Already exists appending new data .. '.format(CSV_FILE_NAME))
    else:
        print('Saving CSV Header')
        SaveAsCsv(CSV_FILE_NAME,header_list)

def file_to_list(file_name):
    path = os.path.join( os.getcwd() , file_name)
    if os.path.isfile(path) and os.access(path, os.R_OK):
        with open (path) as f:
            return list(map(str.strip ,f.readlines()))
    else:return []

def deep_join(li,default='|'):
    new_li = []
    if type(li) == list:
        for i in li:
            if i:new_li.append(i)
        return default.join(new_li)
    elif li == '[]':return ''
    elif type(li) == str: return li
 
def deep_get(d, path, default='',splitter='.'):
    # d is the Json dictionary that has the data
    # path is the selector in the dictionary
    keys = path.split(splitter)
    acum = {} if d is None else d
    for k in keys:
        if acum is not None :
            acum = acum.get(k, default)
            if acum is '': break
    if type(acum) == int or type(acum) == str or acum is not None and type(acum) != list:
        return str(acum).replace('\n','').replace(',',' ').replace('  ',' ').replace('None','').strip()
    elif acum is None :return ''
    else :return acum
    
    
def csv_to_json_with_pandas(csv_file_name=None,sep = ",",csv_location=None):
    # This program assumes the csv file has a header. 
    # In case of missing header in the csv file, we have to pass it explicitly to the program    
    if not csv_location :  csv_location      = os.path.join('output' , f'{csv_file_name}.csv')
    df = pd.DataFrame(pd.read_csv(csv_location, sep = sep, header = 0, index_col = False, na_filter=False))
    headers = df.columns.values.tolist()
    data = df.values.tolist()
    data_list = []
    for  row in data:
        data_dict = {}
        for index, item in enumerate(row,0) :
            data_dict[headers[index]] = item
        data_list.append(data_dict)
    return headers , data_list