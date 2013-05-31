import requests
import simplecaptcha
from PIL import Image
from cStringIO import StringIO

verbose = True
t_user = 'ElectricEefe'
t_passwd = '444444'

class voter():

    def __init__(self, user, passwd):
        self.session = requests.Session()
        self.user = user
        self.passwd = passwd

    def login(self):
        s = self.session
        s.head('https://www.wow-one.com/account/login')
        r = s.get('https://www.wow-one.com/themes/default/script/Captcha.php')
        captcha = Image.open(StringIO(r.content))
        cap = simplecaptcha.solve_captcha(captcha)
        formdata = {'username':self.user, 'password':self.passwd, 'captcha':cap, 'submit':'Login'}
        r = s.post('https://www.wow-one.com/account/login', data=formdata)
        # check response to see if we logged in
        self.loggedin = True

    def vote(self):
        if not self.loggedin:
            return
        s = self.session
        heads = {'Referer':'https://www.wow-one.com/vote/'}
        # want to make sure 2, 1, 0 links remain in the reqs after
        r = s.get('https://www.wow-one.com/vote/process/1', headers=heads)
        r = s.get('https://www.wow-one.com/vote/process/2', headers=heads)
        r = s.get('https://www.wow-one.com/vote/process/3', headers=heads)

v = voter(t_user, t_passwd)
v.login()
v.vote()
