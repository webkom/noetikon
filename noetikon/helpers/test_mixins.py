
class LoginRequiredTestMixin(object):

    def assertLoginRequired(self, url, method='get'):
        methods = {
            'get': self.client.get,
            'post': self.client.post,
        }
        assert method in methods
        response = methods[method](url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue('?next={}'.format(url) in response.url)
