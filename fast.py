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
            def getData(query, id, agent,event_valid,view_state,view_state_gen):
                cookies = {
                    'ASP.NET_SessionId': id,
                    'DISCLAIMER': '1',
                }

                headers = {
                    'User-Agent': agent,
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Referer': 'https://auditor.ashtabulacounty.us/PT/search/commonsearch.aspx?mode=parid',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Origin': 'https://auditor.ashtabulacounty.us',
                    'DNT': '1',
                    'Connection': 'keep-alive',
                    # Requests sorts cookies= alphabetically
                    # 'Cookie': 'ASP.NET_SessionId=ibhnx5dach3twfljh3fw4ed0; DISCLAIMER=1',
                    'Upgrade-Insecure-Requests': '1',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'same-origin',
                    'Sec-Fetch-User': '?1',
                    'Pragma': 'no-cache',
                    'Cache-Control': 'no-cache',
                }

                params = {
                    'mode': 'PARID',
                }

                data = f'ScriptManager1_TSM=%3B%3BAjaxControlToolkit%2C+Version%3D4.1.50731.0%2C+Culture%3Dneutral%2C+PublicKeyToken%3D28f01b0e84b6d53e%3Aen-US%3Af8fb2a65-e23a-483b-b20e-6db6ef539a22%3Aea597d4b%3Ab25378d2%3BTelerik.Web.UI%2C+Version%3D2017.3.913.45%2C+Culture%3Dneutral%2C+PublicKeyToken%3D121fae78165ba3d4%3Aen-US%3A03e3fdef-45f6-40a0-88ab-9645d53a0f37%3A16e4e7cd%3A33715776%3A58366029%3Af7645509%3A24ee1bba%3Af46195d3%3A874f8ea2%3Ab2e06756%3A92fe8ea0%3Afa31b949%3A4877f69a%3Ac128760b%3A19620875%3A490a9d4e&__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE={view_state}&__VIEWSTATEGENERATOR={view_state_gen}&__EVENTVALIDATION={event_valid}&PageNum=&SortBy=PARID&SortDir=+asc&PageSize=15&hdAction=Search&hdIndex=&sIndex=-1&hdListType=PA&hdJur=&hdSelectAllChecked=false&inpParid={query}&selSortBy=PARID&selSortDir=+asc&selPageSize=15&searchOptions%24hdBeta=&btSearch=&RadWindow_NavigateUrl_ClientState=&mode=PARID&mask=&param1=&searchimmediate='

                response = session.post('https://auditor.ashtabulacounty.us/PT/search/CommonSearch.aspx', headers=headers, params=params, cookies=cookies, data=data)

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
                final = f"{address},{owner},{Class},{LndUseCd},{acres},{Psubdiv},{notes},{mail1},{mail2},{address1},{address2},{address3},{comp1},{comp2},{t_year},{delq},{total}"
                #address + owner + Class + LndUseCd + acres + Psubdiv + notes + mail1 + mail2 + address1 + address2 + address3 + comp1 + comp2 + t_year + delq + total
                print(final)
                return {"result":final}
            current = "in"
            session = requests.session()
            homepage = 'https://auditor.ashtabulacounty.us/PT/search/CommonSearch.aspx?mode=PARID'
            headers = {'User-Agent': agent}

            session.headers = headers
            response = session.get(homepage)
            current = "first"
            status = response.status_code

            page = soap(response.text, 'lxml')
            view_state = page.find("input", {'name' : "__VIEWSTATE"})
            view_state_gen = page.find("input", {'name' : "__VIEWSTATEGENERATOR"})
            event_valid =page.find("input", {'name' : "__EVENTVALIDATION"})

            res = requests.get('https://auditor.ashtabulacounty.us/PT/Search/Disclaimer.aspx?FromUrl=../search/commonsearch.aspx?mode=parid',headers = headers )
            cookies = res.cookies
            Id = cookies.get_dict()
            print(Id)
            current = "second"
            data = f"__VIEWSTATE={view_state}&__VIEWSTATEGENERATOR={view_state_gen}&__EVENTVALIDATION={event_valid}&btAgree=&hdURL=..%2Fsearch%2Fcommonsearch.aspx%3Fmode%3Dparid&action="
            response = session.post('https://auditor.ashtabulacounty.us/PT/Search/Disclaimer.aspx?FromUrl=..%2fsearch%2fcommonsearch.aspx%3fmode%3dparid', data = data, cookies={'ASP.NET_SessionId': Id['ASP.NET_SessionId']})
            status = response.status_code
            current = "third"
            if len(str(query)) != 12:

                cookies = {
                    'ASP.NET_SessionId': Id['ASP.NET_SessionId'],
                }

                headers = {
                    'User-Agent': agent,
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Referer': 'https://auditor.ashtabulacounty.us/PT/search/commonsearch.aspx?mode=parid',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Origin': 'https://auditor.ashtabulacounty.us',
                    'DNT': '1',
                    'Connection': 'keep-alive',
                    # Requests sorts cookies= alphabetically
                    # 'Cookie': 'ASP.NET_SessionId=ibhnx5dach3twfljh3fw4ed0; DISCLAIMER=1',
                    'Upgrade-Insecure-Requests': '1',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'same-origin',
                    'Sec-Fetch-User': '?1',
                    'Pragma': 'no-cache',
                    'Cache-Control': 'no-cache',
                }

                params = {
                    'mode': 'PARID',
                }

                data = f'ScriptManager1_TSM=%3B%3BAjaxControlToolkit%2C+Version%3D4.1.50731.0%2C+Culture%3Dneutral%2C+PublicKeyToken%3D28f01b0e84b6d53e%3Aen-US%3Af8fb2a65-e23a-483b-b20e-6db6ef539a22%3Aea597d4b%3Ab25378d2%3BTelerik.Web.UI%2C+Version%3D2017.3.913.45%2C+Culture%3Dneutral%2C+PublicKeyToken%3D121fae78165ba3d4%3Aen-US%3A03e3fdef-45f6-40a0-88ab-9645d53a0f37%3A16e4e7cd%3A33715776%3A58366029%3Af7645509%3A24ee1bba%3Af46195d3%3A874f8ea2%3Ab2e06756%3A92fe8ea0%3Afa31b949%3A4877f69a%3Ac128760b%3A19620875%3A490a9d4e&__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE={view_state}&__VIEWSTATEGENERATOR={view_state_gen}&__EVENTVALIDATION={event_valid}&PageNum=&SortBy=PARID&SortDir=+asc&PageSize=500&hdAction=Search&hdIndex=&sIndex=-1&hdListType=PA&hdJur=&hdSelectAllChecked=false&inpParid={query}&selSortBy=PARID&selSortDir=+asc&selPageSize=500&searchOptions%24hdBeta=&btSearch=&RadWindow_NavigateUrl_ClientState=&mode=PARID&mask=&param1=&searchimmediate='

                response = session.post('https://auditor.ashtabulacounty.us/PT/search/CommonSearch.aspx', headers=headers, params=params, cookies=cookies, data=data)
                html = response.text
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
                for i in new:
                    current = "fourth"
                    getData(i,Id['ASP.NET_SessionId'], agent,event_valid,view_state,view_state_gen)
            else:
                getData(query,Id['ASP.NET_SessionId'], agent,event_valid,view_state,view_state_gen)
    except Exception as e:
        return {
            "Error":e ,
            "stu" : current ,   
            "status": status  ,
            "html" : html
        }
