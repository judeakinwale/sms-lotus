from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory
from information import models, serializers


NOTICE_URL = reverse('information:notice-list')

# creating a test request
factory = APIRequestFactory()
request = factory.get('/')
# create serializer context
serializer_context = {'request': Request(request)}


def notice_detail_url(notice_id):
    """return url for the notice detail"""
    return reverse('information:notice-detail', args=[notice_id])


def sample_scope(description='General', **kwargs):
    """create and return a sample scope"""
    defaults = {}
    defaults.update(kwargs)
    return models.Scope.objects.create(description=description, **defaults)


def sample_notice(source, **kwargs):
    """create and return sample notice"""
    defaults = {
        'scope': sample_scope(),
        'title': 'Test title',
        'message': 'Lorem ipsum dolor sit amet',
    }
    defaults.update(kwargs)
    return models.Notice.objects.create(source=source, **defaults)


# def sample_notice_image(notice, **kwargs):
#     """create and return a sample notice image"""
#     defaults = {
#         'description': 'sample notice image'
#     }
#     defaults.update(kwargs)
#     return models.NoticeImage.create(notice=notice, **defaults)



def test_all_model_attributes(insance, payload, model, serializer):
    """test model attributes against a payload, with instance being self in a testcase class """
    ignored_keys = ['image']
    relevant_keys = sorted(set(payload.keys()).difference(ignored_keys))
    for key in relevant_keys:
        try:
            insance.assertEqual(payload[key], getattr(model, key))
        except:
            insance.assertEqual(payload[key], serializer.data[key])


class PublicNoticeApiTest(TestCase):
    """test public access to the notice api"""

    def setUp(self):
        self.client = APIClient()

    def test_authentication_required(self):
        """test that authentication is required"""
        res = self.client.get(NOTICE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        # self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateNoticeApiTest(TestCase):
    """test authenticated access to the notice api"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@email.com',
            password='testpass'
        )
        self.client.force_authenticate(self.user)

    def tearDown(self):
        pass

    def test_retrieve_notice(self):
        """test retrieving a list of notice"""
        sample_notice(source=self.user)
        notice = models.Notice.objects.all()
        serializer = serializers.NoticeSerializer(notice, many=True, context=serializer_context)

        res = self.client.get(NOTICE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_notice_not_limited_to_source(self):
        """test that notices from all sources is returned"""
        sample_notice(source=self.user)
        user2 = get_user_model().objects.create_user(
            'test2@test.com',
            'testpass2'
        )
        sample_notice(source=user2)

        notice = models.Notice.objects.all()
        serializer = serializers.NoticeSerializer(notice, many=True, context=serializer_context)
        
        res = self.client.get(NOTICE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(len(res.data), 2)

    def test_retrieve_notice_detail(self):
        """test retrieving a notice's detail"""
        notice = sample_notice(source=self.user)
        serializer = serializers.NoticeSerializer(notice, context=serializer_context)
        
        url = notice_detail_url(notice_id=notice.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_notice(self):
        """test creating a notice"""
        scope_serializer = serializers.ScopeSerializer(sample_scope(), context=serializer_context)
        payload = {
            'source': self.user.id,
            'scope': scope_serializer.data['url'],
            'title': 'Test title 2',
            'message': 'message for test title 2',
        }

        res = self.client.post(NOTICE_URL, payload)

        notice = models.Notice.objects.get(id=res.data['id'])
        notice_serializer = serializers.NoticeSerializer(notice, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        test_all_model_attributes(self, payload, notice, notice_serializer)

    def test_partial_update_notice(self):
        """test partially updating a notice's detail using patch"""
        notice = sample_notice(source=self.user)
        scope = sample_scope(description='Private', is_general=False)
        scope_serializer = serializers.ScopeSerializer(scope, context=serializer_context)
        payload = {
            'scope': scope_serializer.data['url'],
            'message': 'An updated message'
        }

        url = notice_detail_url(notice.id)
        res = self.client.patch(url, payload)

        notice.refresh_from_db()
        notice_serializer = serializers.NoticeSerializer(notice, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        test_all_model_attributes(self, payload, notice, notice_serializer)

    def test_full_update_notice(self):
        """test updating a notice's detail using put"""
        notice = sample_notice(source=self.user)
        scope = sample_scope(description='Private test', is_first_year=True)
        scope_serializer = serializers.ScopeSerializer(scope, context=serializer_context)
        payload = {
            'source': self.user.id,
            'scope': scope_serializer.data['url'],
            'title': 'Test title 3',
            'message': 'An updated message'
        }

        url = notice_detail_url(notice.id)
        res = self.client.put(url, payload)

        notice.refresh_from_db()
        notice_serializer = serializers.NoticeSerializer(notice, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        test_all_model_attributes(self, payload, notice, notice_serializer)
