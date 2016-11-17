#!/usr/bin/python
import mechanize, sys, os
from BeautifulSoup import BeautifulSoup

sys.path.append('..')
from secrets import cams_username
from secrets import cams_password
#from doge import bad_ssl # use if dealing w/ sites with weak security configs.

def attrs(**kwargs):
    return lambda f: all(getattr(f, k) == v for k, v in kwargs.iteritems())

def main(_, name):
    b = mechanize.Browser()
    b.set_handle_robots(False)
    b.open('https://listmaker.mit.edu/lc/')

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

    b.select_form(predicate=attrs(method='POST', action='https://listmaker.mit.edu/lc/'))
    b['ltype'] = ['1'] # Moira
    b.submit()
    b.select_form(predicate=attrs(method='POST', action='https://listmaker.mit.edu/lc/moira'))
    b['lname'] = name # Name of List
    b['owner'] = 'leee'  # List Owner
    #b['ownertype'] = ['1'] # Check if owner is a list.
    b.find_control("mail").items[0].selected=False # Use to mark list for not mail.
    b.submit()
    b.select_form(predicate=attrs(method='POST', action='https://listmaker.mit.edu/lc/confirm'))
    b.submit()
    os.execlp('blanche', 'blanche', name, '-i')

if __name__ == '__main__':
    sys.exit(main(*sys.argv))
