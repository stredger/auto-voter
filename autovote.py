import httplib
import urllib2

verbose = True

class voter():

    def __init__(self):
        self.host = 'www.wow-one.com'

    def request_resource(self, method, resource, extra_headers={}):
        if verbose:
                print "%s%s" % (self.host, resource),
                
        connection = httplib.HTTPSConnection(self.host)
        connection.request(method, resource, headers=extra_headers)
        response = connection.getresponse()
        connection.close()
        
        if verbose:
                print "%s %s" % (response.status, response.reason)
                
        return response

    def get_image(self, resource, extra_headers={}):
        request = urllib2.Request('http://%s%s' % (self.host, resource))
        for key, val in extra_headers.iteritems():
            request.add_header(key, val)
        resource = urllib2.urlopen(request)
        if resource.getcode() != 200:
            return None
        data = resource.read()
        return data


    def solve_captcha(data):
        pass


    def login(self):
        login_resource = self.request_resource('head', '/account/login')

        if login_resource.status != 200:
            print "Failed to get login page\n%s %s" % (login_resource.status, login_resource.reason)
            return

        login_cookie = login_resource.getheader('set-cookie')
        http_headers = {'Cookie':login_cookie}
        captcha = self.get_image('/themes/default/script/Captcha.php', http_headers)

        f = open('test.png', 'w')
        f.write(captcha)




v = voter()
v.login()

# dat = urllib2.urlopen('http://www.wow-one.com/account/login')
# reqs = dat.info()
# print dat.getcode()
# print reqs
#dat = urllib2.Request('http://www.wow-one.com/themes/default/script/Captcha.php')

