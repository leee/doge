#!/usr/bin/python
import mechanize, sys, os, re
from BeautifulSoup import BeautifulSoup
from prettytable import PrettyTable
import requests

sys.path.append('..')
from secrets import cams_username
from secrets import cams_password
from doge import bad_ssl # use if dealing w/ sites with weak security configs.

# with thanks to http://stackoverflow.com/a/13816975
def check_url(browser, url):
    try:
        response = browser.open(url)
    except (mechanize.HTTPError,mechanize.URLError) as e:
        if isinstance(e,mechanize.HTTPError):
            return e.code < 400
        else:
            return False
    return True

def main():
    b = mechanize.Browser()
    b.set_handle_robots(False)
    b.open('https://floorplans.mit.edu/searchPDF.asp')

    if b.geturl().startswith('https://wayf.mit.edu/'):
        b.select_form(name='IdPList')
        b.form['user_idp']=['https://idp.touchstonenetwork.net/shibboleth-idp']
        b.submit()
        b.select_form(name='loginform')
        b.form['j_username'] = cams_username
        b.form['j_password'] = cams_password
        b.submit()
        b.select_form(nr=0)
        b.submit()

    response = b.response()
    html = response.read()
    soup = BeautifulSoup(html)

    t = PrettyTable(["bldg","floor", "url"])

    table = soup.find('select', attrs={'name':'Bldg'})

    for bldg in table.findAll('option'):
        b.open('https://floorplans.mit.edu/ListPDF.Asp?Bldg='+bldg.text)
        response = b.response()
        html = response.read()
        soup = BeautifulSoup(html)
        for a in soup.findAll('a', href=re.compile('^/pdfs/')):
            url = "https://floorplans.mit.edu"+a['href']
            t.add_row([bldg.text, a.text, url])

            mezz = a.text+"M"
            url = "https://floorplans.mit.edu/pdfs/"+bldg.text+"_"+mezz+".pdf"
            if check_url(b, url):
                t.add_row([bldg.text, mezz, url])

        url = "https://floorplans.mit.edu/pdfs/"+bldg.text+"_R.pdf"
        if check_url(b, url):
            t.add_row([bldg.text, "R", url])

    t.align["bldg"] = "l"
    t.align["floor"] = "l"
    t.align["url"] = "l"
    print t

if __name__ == '__main__':
    sys.exit(main())
