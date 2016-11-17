#!/usr/bin/python
import mechanize, sys, os, re
from BeautifulSoup import BeautifulSoup
from prettytable import PrettyTable

sys.path.append('..')
from secrets import cams_username
from secrets import cams_password
from doge import bad_ssl # use if dealing w/ sites with weak security configs.

def main():
    b = mechanize.Browser()
    b.set_handle_robots(False)
    b.open('https://cogen.mit.edu/systemstatus.cfm')

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

    t = PrettyTable(["tag", "desc", "value"])

    for a in soup.findAll('a', href=re.compile('^tagproperties.cfm\?tag=')):
        tag = a['href']
        value = a.findNext('td')
        t.add_row([tag[22:], a.text, value.text])

    t.add_column("unit", ["MW", "MW", "MW", "KPPH", "KPPH", "RT"])

    b.open('https://cogen.mit.edu/weather.cfm')

    response = b.response()
    html = response.read()
    soup = BeautifulSoup(html)

    for a in soup.findAll('a', href=re.compile('^tagproperties.cfm\?tag=')):
        tag = a['href']
        desc = a.findNext('td')
        value = desc.findNext('td')
        unit = value.findNext('td')
        t.add_row([tag[22:], desc.text, value.text, unit.text])

    t.align["tag"] = "l"
    t.align["desc"] = "l"
    t.align["value"] = "l"
    t.align["unit"] = "l"
    print t

if __name__ == '__main__':
    sys.exit(main())
