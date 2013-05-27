import httplib, urllib, urllib2
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

    def request_resource(self, method, resource, formdata=None, extra_headers={}):
        if verbose:
                print "%s%s" % (self.host, resource),
        connection = httplib.HTTPSConnection(self.host)
        connection.request(method, resource, formdata, extra_headers)
        response = connection.getresponse()
        connection.close()
        if verbose:
                print "%s %s" % (response.status, response.reason)
                
        return response

    def get_image(self, resource, extra_headers={}):
        if verbose:
                print "%s%s" % (self.host, resource),
        request = urllib2.Request('http://%s%s' % (self.host, resource))
        for key, val in extra_headers.iteritems():
            request.add_header(key, val)
        resource = urllib2.urlopen(request)
        if verbose:
                print str(resource.getcode())
        if resource.getcode() != 200:
            return None
        data = resource.read()
        return StringIO(data)


    def login(self):
        login_resource = self.request_resource('get', '/account/login')
        print login_resource.getheaders()
        print login_resource.read()
        if login_resource.status != 200:
            print "Failed to get login page\n%s %s" % (login_resource.status, login_resource.reason)
            return

        login_cookie = login_resource.getheader('set-cookie')
        http_headers = {'Cookie':login_cookie}
        imgdata = self.get_image('/themes/default/script/Captcha.php', http_headers)

        if imgdata is None:
            print "Failed to get captcha"
            return
        
        captcha = Image.open(imgdata)
        capsolver = simplecaptcha.captchasolver()
        cap = capsolver.solve_captcha(captcha)
        loginparams = urllib.urlencode({'username':self.user, 'password':self.passwd, 'captcha':cap, 'submit':'Login'})
        print loginparams
        login_resource = self.request_resource('post', '/account/login', loginparams, http_headers)
        vote_resource = self.request_resource('get', '/vote/', extra_headers=http_headers)
        data = vote_resource.read()
        headers = vote_resource.getheaders()
        print headers
        print data





v = voter(t_user, t_passwd)
v.login()

# dat = urllib2.urlopen('http://www.wow-one.com/account/login')
# reqs = dat.info()
# print dat.getcode()
# print reqs
#dat = urllib2.Request('http://www.wow-one.com/themes/default/script/Captcha.php')

