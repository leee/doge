#!/usr/bin/python
import mechanize, sys, os
from BeautifulSoup import BeautifulSoup

from secrets import cams_username
from secrets import cams_password
#from doge import bad_ssl # use if dealing w/ sites with weak security configs.

def main(_, url):
    b = mechanize.Browser()
    b.set_handle_robots(False)
    b.open(url)

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
    print response.read()

if __name__ == '__main__':
    sys.exit(main(*sys.argv))
