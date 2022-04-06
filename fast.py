import requests
from bs4 import BeautifulSoup as soap
from fastapi import FastAPI


app = FastAPI()
@app.get('/')
def myapi():
    agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0"
    queries = ['1234']
    try:
        current = "started"
        for query in queries:
            def getData(query,event_valid,view_state,view_state_gen):
                params = {
                    'mode': 'PARID',
                }

                data = {
                        '__EVENTTARGET': '',
                        '__EVENTARGUMENT': '',
                        '__VIEWSTATE': view_state,
                        '__VIEWSTATEGENERATOR': view_state_gen,
                        '__EVENTVALIDATION': event_valid,
                        'PageNum': '',
                        'SortBy': 'PARID',
                        'SortDir': ' asc',
                        'PageSize': '500',
                        'hdAction': 'Search',
                        'hdIndex': '',
                        'sIndex': '-1',
                        'hdListType': 'PA',
                        'hdJur': '',
                        'hdSelectAllChecked': 'false',
                        'inpParid': query,
                        'selSortBy': 'PARID',
                        'selSortDir': ' asc',
                        'selPageSize': '500',
                        'searchOptions$hdBeta': '',
                        'btSearch': '',
                        'RadWindow_NavigateUrl_ClientState': '',
                        'mode': 'PARID',
                        'mask': '',
                        'param1': '',
                        'searchimmediate': '',
}


                response = session.post('https://auditor.ashtabulacounty.us/PT/search/CommonSearch.aspx', params=params, data=data)

                parse = response.text
                parsed = soap(parse,'lxml')
                address_table = parsed.find("table", {'id' : "Parcel"})
                owner_table = parsed.find("table", {'id' : "Owner"})
                TaxMailingNameAndAddress_table = parsed.find("table", {'id' : "Tax Mailing Name and Address"})
                TaxCharge_table = parsed.find("table", {'id' : "Taxes Charged (Tax Tear 2021)"})

                tr_tag_list = address_table.findAll('tr')
                for tr in tr_tag_list:
                    td = tr.find('td',{'class':'DataletSideHeading'})
                    if td == None:
                        continue
                    if td.getText() == 'Address':
                        address = tr.find('td',{'class':'DataletData'}).getText()
                    if td.getText() == 'Class':
                        Class = tr.find('td',{'class':'DataletData'}).getText()
                    if td.getText() == 'Land Use Code':
                        LndUseCd = tr.find('td',{'class':'DataletData'}).getText()
                    if td.getText() == 'Acres':
                        acres = tr.find('td',{'class':'DataletData'}).getText()
                    if td.getText() == 'Political Subdivsion':
                        Psubdiv = tr.find('td',{'class':'DataletData'}).getText()

                tr_tag_list = owner_table.findAll('tr')
                for tr in tr_tag_list:
                    td = tr.find('td',{'class':'DataletSideHeading'})
                    if td == None:
                        continue
                    if td.getText() == 'Owner':
                        owner = tr.find('td',{'class':'DataletData'}).getText()
                    if td.getText() == 'Notes':
                        notes = tr.find('td',{'class':'DataletData'}).getText()

                tr_tag_list = TaxMailingNameAndAddress_table.findAll('tr')
                mor = False
                for tr in tr_tag_list:
                    td = tr.find('td',{'class':'DataletSideHeading'})
                    if td == None:
                        continue
                    if td.getText() == 'Mailing Name 1':
                        mail1 = tr.find('td',{'class':'DataletData'}).getText()
                    if td.getText() == 'Mailing Name 2':
                        mail2 = tr.find('td',{'class':'DataletData'}).getText()
                    if td.getText() == 'Address 1':
                        address1 = tr.find('td',{'class':'DataletData'}).getText()
                    if td.getText() == 'Address 2':
                        address2 = tr.find('td',{'class':'DataletData'}).getText()
                    if td.getText() == 'Address 3':
                        address3 = tr.find('td',{'class':'DataletData'}).getText()
                    if td.getText() == 'Mortgage Company' and mor == False:
                        mor = True
                        comp1 = tr.find('td',{'class':'DataletData'}).getText()
                    if td.getText() == 'Mortgage Company':
                        comp2 = tr.find('td',{'class':'DataletData'}).getText()
                    if td.getText() == 'Tax Year':
                        t_year = tr.find('td',{'class':'DataletData'}).getText()

                tr_tag_list = TaxCharge_table.findAll('tr')
                for tr in tr_tag_list:
                    tds = tr.findAll('td')
                    for td in tds:
                        if td == None:
                            continue
                        if td.getText().startswith('$') and tds.index(td) == 1:
                            delq = td.getText()
                        if td.text.startswith('$') and tds.index(td) == 4:
                            total = td.getText()
                lstt = f"{address},{owner},{Class},{LndUseCd},{acres},{Psubdiv},{notes},{mail1},{mail2},{address1},{address2},{address3},{comp1},{comp2},{t_year},{delq},{total}"
                #address + owner + Class + LndUseCd + acres + Psubdiv + notes + mail1 + mail2 + address1 + address2 + address3 + comp1 + comp2 + t_year + delq + total
                return lstt
                
            current = "in"
            session = requests.session()
            homepage = 'https://auditor.ashtabulacounty.us/PT/Search/Disclaimer.aspx?FromUrl=../search/commonsearch.aspx?mode=parid'
            headers = {'User-Agent': agent}

            session.headers.update(headers)
            response = session.get(homepage)
            current = "first"
            status = response.status_code
            #res = requests.get('https://auditor.ashtabulacounty.us/PT/Search/Disclaimer.aspx?FromUrl=../search/commonsearch.aspx?mode=parid',headers = headers )
            cookies = response.cookies
            Id = cookies.get_dict()
            print(Id)
            page = soap(response.text, 'lxml')
            view_state = page.find("input", {'name' : "__VIEWSTATE"})
            view_state = view_state["value"]
            view_state_gen = page.find("input", {'name' : "__VIEWSTATEGENERATOR"})
            view_state_gen = view_state_gen["value"]
            event_valid =page.find("input", {'name' : "__EVENTVALIDATION"})
            event_valid = event_valid["value"]
            data = {
    '__VIEWSTATE': view_state,
    '__VIEWSTATEGENERATOR': view_state_gen,
    '__EVENTVALIDATION': event_valid,
    'btAgree': '',
    'hdURL': '../search/commonsearch.aspx?mode=parid',
    'action': '',
}
            response = session.post('https://auditor.ashtabulacounty.us/PT/Search/Disclaimer.aspx?FromUrl=../search/commonsearch.aspx?mode=parid', data=data)
            html = response.text + "hello"
            current = "second"
            status = response.status_code
            page = soap(response.text, 'lxml')
            view_state = page.find("input", {'name' : "__VIEWSTATE"})
            view_state = view_state["value"]
            view_state_gen = page.find("input", {'name' : "__VIEWSTATEGENERATOR"})
            view_state_gen = view_state_gen["value"]
            event_valid =page.find("input", {'name' : "__EVENTVALIDATION"})
            event_valid = event_valid["value"]
            if len(str(query)) != 12:
                params = {
                    'mode': 'PARID',
                }

                data = {
                    '__EVENTTARGET': '',
                    '__EVENTARGUMENT': '',
                    '__VIEWSTATE': view_state,
                    '__VIEWSTATEGENERATOR': view_state_gen,
                    '__EVENTVALIDATION': event_valid,
                    'PageNum': '',
                    'SortBy': 'PARID',
                    'SortDir': ' asc',
                    'PageSize': '500',
                    'hdAction': 'Search',
                    'hdIndex': '',
                    'sIndex': '-1',
                    'hdListType': 'PA',
                    'hdJur': '',
                    'hdSelectAllChecked': 'false',
                    'inpParid': '1234',
                    'selSortBy': 'PARID',
                    'selSortDir': ' asc',
                    'selPageSize': '500',
                    'searchOptions$hdBeta': '',
                    'btSearch': '',
                    'RadWindow_NavigateUrl_ClientState': '',
                    'mode': 'PARID',
                    'mask': '',
                    'param1': '',
                    'searchimmediate': '',
}


                response = session.post('https://auditor.ashtabulacounty.us/PT/search/CommonSearch.aspx', params=params, data=data)
                html = response.text
                current = "here"
                page = soap(response.text,'lxml')
                table = page.find("table", {'id' : "searchResults"})

                td_tag_list = table.findAll(
                                lambda tag:tag.name == "td" and
                                len(tag.text) == 12 )
                new = []
                for i in td_tag_list:
                    try:
                        new.append(int(i.text))
                    except:
                        pass
                final = []
                for i in new:
                    current = "fourth"
                    lstt = getData(i,event_valid,view_state,view_state_gen)
                    final.append(lstt)
                return {"result":final}
            else:
                getData(query,event_valid,view_state,view_state_gen)
    except Exception as e:
        return { "main":
                    {
                    "Error":e ,
                    "stu" : current ,   
                    "status": status
                    },
            "html" : html
        }
