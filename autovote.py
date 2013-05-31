import urllib, urllib2
import simplecaptcha
from PIL import Image
from cStringIO import StringIO

verbose = True
t_user = 'ElectricEefe'
t_passwd = '444444'

class voter():

    def __init__(self, user, passwd):
        self.host = 'www.wow-one.com'
        self.user = user
        self.passwd = passwd

    
    def request_resource(self, resource, data={}, extra_headers={}):
        if verbose: print "%s%s" % (self.host, resource),
        data = urllib.urlencode(data)
        request = urllib2.Request('http://%s%s' % (self.host, resource), data, extra_headers)
        resource = urllib2.urlopen(request)
        if verbose: print str(resource.getcode())
        return resource if resource.getcode() == 200 else None


    def login(self):
        login_resource = self.request_resource('/account/login')
        if login_resource is None:
            print "Failed to get login page"
            return
        heads = login_resource.info()
        login_cookie = heads['set-cookie']
        http_headers = {'Cookie':login_cookie}
        img_resource = self.request_resource('/themes/default/script/Captcha.php', extra_headers=http_headers)
        if img_resource is None:
            print "Failed to get captcha"
            return
        # read img into a file like object
        img_data = StringIO(img_resource.read())
        captcha = Image.open(img_data)
        capsolver = simplecaptcha.captchasolver()
        cap = capsolver.solve_captcha(captcha)
        login_params = {'username':self.user, 'password':self.passwd, 'captcha':cap, 'submit':'Login'}
        login_resource = self.request_resource('/account/login', login_params, http_headers)
        print login_resource.info()






#v = voter(t_user, t_passwd)
#v.login()

import requests

s = requests.Session()
s.get('https://www.wow-one.com/account/login')
r = s.get('https://www.wow-one.com/themes/default/script/Captcha.php')
captcha = Image.open(StringIO(r.content))
cap = simplecaptcha.solve_captcha(captcha)
formdata = {'username':t_user, 'password':t_passwd, 'captcha':cap, 'submit':'Login'}
s.post('https://www.wow-one.com/account/login', data=formdata)
r = s.get('https://www.wow-one.com/vote/')
heads = {'Referer':'https://www.wow-one.com/vote/'}
r = s.get('https://www.wow-one.com/vote/process/1', headers=heads)
r = s.get('https://www.wow-one.com/vote/process/2', headers=heads)
r = s.get('https://www.wow-one.com/vote/process/3', headers=heads)

print r.request.headers
print r.headers

# r = requests.get('https://www.wow-one.com/account/login')
# cookies = r.cookies
# r = requests.get('https://www.wow-one.com/themes/default/script/Captcha.php', cookies=cookies)
# captcha = Image.open(StringIO(r.content))
# cap = simplecaptcha.solve_captcha(captcha)
# formdata = {'username':t_user, 'password':t_passwd, 'captcha':cap, 'submit':'Login'}
# r = requests.post('https://www.wow-one.com/account/login', data=formdata, cookies=cookies)
# #print r.cookies
# r = requests.get('https://www.wow-one.com/vote/', cookies=cookies)
# #r = requests.get('https://www.wow-one.com/vote/process/1', cookies=cookies)
# #r = requests.get('https://www.wow-one.com/vote/process/1', cookies=cookies)
# #print r.status_code
# #print requests.codes.ok
# print r.text
# r = requests.get('https://www.wow-one.com/vote/process/1', cookies=cookies)
# print r.text
