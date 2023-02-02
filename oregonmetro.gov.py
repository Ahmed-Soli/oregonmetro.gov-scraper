import requests,string
from bs4 import BeautifulSoup
from time import sleep
from csv_func import SaveHeaders , SaveAsCsv

def get_variables():
    print(f'getting Variables for url {MAIN_URL}...')
    Get_Headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'accept-language': 'en-US,en;q=0.9', 'cache-control': 'max-age=0', 'sec-ch-ua': '"Microsoft Edge";v="107", "Chromium";v="107", "Not=A?Brand";v="24"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', 'sec-fetch-dest': 'document', 'sec-fetch-mode': 'navigate', 'sec-fetch-site': 'none', 'sec-fetch-user': '?1', 'upgrade-insecure-requests': '1', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.56'}
    
    page_source = session.get(MAIN_URL,headers=Get_Headers)
    return  BeautifulSoup(page_source.text, 'html.parser')

def get_token(page_source):
    print('getting form_build_id token')    
    form_build_id         = page_source.find('input', {'name': 'form_build_id'}).get('value')
    print(form_build_id)
    return form_build_id

def GetValue(val):
    try:
        return val.text.strip().rstrip('\n')
    except:
        return ''

def search_link(criteria='a',page=1):
    global form_build_id
    print(f'getting search link page => {page} .. searching with {letter} index {index}/28')
    Get_Headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'accept-language': 'en-US,en;q=0.9', 'referer': 'https://www.oregonmetro.gov/tools-working/regional-contractors-business-license/lookup', 'sec-ch-ua': '"Microsoft Edge";v="107", "Chromium";v="107", "Not=A?Brand";v="24"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', 'sec-fetch-dest': 'document', 'sec-fetch-mode': 'navigate', 'sec-fetch-site': 'same-origin', 'sec-fetch-user': '?1', 'upgrade-insecure-requests': '1', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.56'}

    url_param = {'page':page,'criteria': criteria, 'op': 'Search', 'form_build_id': form_build_id, 'form_id': 'metro_cbl_form'}
    
    resp = session.post(MAIN_URL,params=url_param,headers=Get_Headers)
    return BeautifulSoup(resp.content,'html.parser')

def extract_info(source):
    print(f'Extracting .. searching with {letter} index {index}/28')
    rows = source.select('table[id="cbl-results"] tbody tr')
    for indexx, row in enumerate(rows,1):
        print(f'getting row {indexx}/{len(rows)}')
        columns                 = row.select('td')
        Business_Name           = GetValue(columns[0])
        Business_Address        = GetValue(columns[1])
        Area_Code               = GetValue(columns[2])
        Phone                   = GetValue(columns[3])
        Metro_License_Number    = GetValue(columns[4])
        Metro_Expiration_Date   = GetValue(columns[5])
        OCCB                    = GetValue(columns[6])
        City_License_Number     = GetValue(columns[7])
        headers_lst     = [Business_Name,Business_Address,Area_Code,Phone,Metro_License_Number,Metro_Expiration_Date,OCCB,City_License_Number,letter]
        SaveAsCsv(CSV_Filename,headers_lst)

CSV_Filename    = 'oregonmetro.csv'
page            = 0
headers_lst     = ['Business_Name','Business_Address','Area_Code','Phone','Metro_License_Number','Metro_Expiration_Date','OCCB','City_License_Number','Keyword']
SaveHeaders(CSV_Filename,headers_lst)
MAIN_URL = 'https://www.oregonmetro.gov/tools-working/regional-contractors-business-license/lookup'
with requests.Session() as session:
    page_source         = get_variables()
    form_build_id       = get_token(page_source)
    for index,letter in enumerate(string.ascii_lowercase,1):
        print(f'searching with {letter} index {index}/28')
        source              = search_link(criteria=letter,page=page)
        extract_info(source)
        while source.select_one('li[class="pager-next last"] a'):
            page  += 1
            source = search_link(criteria=letter,page=page)
            extract_info(source)
        
    
print(string.ascii_lowercase)