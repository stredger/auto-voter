import urllib2
import urllib
import os
import simplecaptcha
from PIL import Image
from cStringIO import StringIO
from cookielib import CookieJar

verbose = True
t_users = ['ElectricEefe', 'NickJays', 'NickJays1', 'NickJays2', 'NickJays3']
t_proxies = [{'https':'http://199.48.166.27:3128'}, 
            {'https':'http://174.140.166.54:8080'}, 
            {'https':'http://213.133.141.197:8080'}, 
            {'https':'http://50.115.173.178:7808'}, 
            {'https':'http://23.254.134.208:8080'}]
t_passwd = ''

class voter():

    def __init__(self, user, passwd, proxy={}):
        self.opener = urllib2.build_opener(urllib2.ProxyHandler(proxy), urllib2.HTTPCookieProcessor(CookieJar()))
        self.user = user
        self.passwd = passwd

    def open(self, url, data=None):
        r = None
        while not r:
            try: r = self.opener.open(url, data=data)
            except urllib2.URLError, e: pass
        assert r.getcode() in (200, 302), 'Return code: %s' % (r.getcode())    
        return r

    def login(self):
        self.open('https://www.wow-one.com/account/login/')        
        r = self.open('https://www.wow-one.com/themes/default/script/Captcha.php')
        if verbose: print 'Got captcha'
        captcha = Image.open(StringIO(r.read()))
        cap = simplecaptcha.solve_captcha(captcha)
        if verbose: print 'Captcha solved: %s' % (cap)
        formdata = urllib.urlencode({'username':self.user, 'password':self.passwd, 'captcha':cap, 'submit':'Login'})
        r = self.open('https://www.wow-one.com/account/login/', data=formdata)
        if 'You are successfully logged in!' in r.read():
            self.loggedin = True
            if verbose: print 'Successfully logged in'
        else:
            print 'Failed to log in'

    def vote(self):
        if not self.loggedin:
            return
        r = self.open('https://www.wow-one.com/vote/')
        self.opener.addheaders.append(('Referer','https://www.wow-one.com/vote/'))
        # TODO: make sure 3, 2, 1, 0 links remain in the reqs after
        # get the vote page as we get a new cookie, and for each get after
        r = self.open('https://www.wow-one.com/vote/process/1')
        if verbose: print 'Vote 1'
        r = self.open('https://www.wow-one.com/vote/process/2')
        if verbose: print 'Vote 2'
        r = self.open('https://www.wow-one.com/vote/process/3')
        if verbose: print 'Vote 3'

for usr, proxy in zip(t_users, t_proxies):
    v = voter(usr, t_passwd, proxy)
    v.login()
    v.vote()
