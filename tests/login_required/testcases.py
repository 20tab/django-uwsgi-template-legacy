from __future__ import absolute_import, print_function, unicode_literals

from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django_webtest import WebTest


class LoginRequiredTestCase(WebTest):

    def setUp(self):
        self.user = get_user_model().objects.create(
            username='usertest',
            first_name='John', last_name='Smith',
            email='test@wfp.org',
        )
        self.user_password = 'test'
        self.user.set_password(self.user_password)
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def login(self, url, **kwargs):
        if url != reverse('login'):
            resp = self.app.get(url, **kwargs).follow()
        else:
            resp = self.app.get(url, **kwargs)
        login_form = resp.form
        login_form['username'] = self.user.username
        login_form['password'] = self.user_password
        login_form['next'] = url
        response = login_form.submit(**kwargs).follow()
        return response

    # def test_login(self):
    #     response = self.login('/login/')
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_login_not_valid(self):
    #     resp = self.app.get(reverse('login'))
    #     login_form = resp.form
    #     login_form['username'] = 'user_no'
    #     login_form['password'] = 'fail'
    #     response = login_form.submit()
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_logout(self):
    #     self.login(reverse('login'))
    #     response = self.app.get(reverse('logout')).follow()
    #     self.assertEqual(response.status_code, 302)
