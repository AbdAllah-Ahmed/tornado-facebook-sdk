from tornado import testing
from facebook import facebook
from tornado.ioloop import IOLoop
from tests import test_user_id, test_app_key
import datetime

class GraphAPITestCase(testing.AsyncTestCase):

    #TODO: create a test user for each run
    # example: POST 256248457829889/accounts/test-users?installed=true&name=John Doe&permissions=publish_stream&method=POST&access_token=256248457829889|VdsmNePcAFQ6wQrMmU6Qmz2FVnw

    def get_new_ioloop(self):
        return IOLoop.instance()

    def test_get_object(self):
        graph = facebook.GraphAPI(test_app_key)
        graph.get_object(test_user_id, callback=self.stop)
        response = self.wait()
        expected = {
            u'first_name': u'John',
            u'last_name': u'Doe',
            u'name': u'John Doe',
            u'locale': u'pt_BR',
            u'gender': u'female',
            u'link': u'http://www.facebook.com/people/John-Doe/100004430523129',
            u'id': u'100004430523129'
        }
        self.assertDictEqual(expected, response)

    def test_invalid_key_assert_raises_graph_api_error(self):
        with self.assertRaises(facebook.GraphAPIError):
            graph = facebook.GraphAPI('notavalidkey')
            graph.get_object(test_user_id, callback=self.stop)
            self.wait()

    def test_put_object(self):
        #putting on a test user wall is not working
        graph = facebook.GraphAPI(test_app_key)
        graph.put_object(test_user_id,
                "feed",
                self.stop,
                message="Another message in the Wall {}".format(datetime.datetime.now()))
        response = self.wait()
        self.assertIn('id', response)
