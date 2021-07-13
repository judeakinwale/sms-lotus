from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory
from academics import models, serializers


LEVEL_URL = reverse('academics:level-list')

# creating a test request
factory = APIRequestFactory()
request = factory.get('/')
# create serializer context
serializer_context = {'request': Request(request)}


def level_detail_url(level_id):
    """return url for the level detail"""
    return reverse('academics:level-detail', args=[level_id])


def sample_level(**kwargs):
    """create and return a sample level"""
    defaults = {'code': 400}
    defaults.update(kwargs)
    return models.Level.objects.create(**defaults)


def test_all_model_attributes(insance, payload, model, serializer):
    """test model attributes against a payload, with instance being self in a testcase class """
    ignored_keys = ['image']
    relevant_keys = sorted(set(payload.keys()).difference(ignored_keys))
    for key in relevant_keys:
        try:
            insance.assertEqual(payload[key], getattr(model, key))
        except:
            insance.assertEqual(payload[key], serializer.data[key])


class PublicLevelApiTest(TestCase):
    """test public access to the level api"""

    def setUp(self):
        self.client = APIClient()

    def test_authentication_required(self):
        """test that authentication is required"""
        res = self.client.get(LEVEL_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        # self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateLevelApiTest(TestCase):
    """test authenticated access to the level api"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@email.com',
            password='testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_level(self):
        """test retrieving a list of level"""
        sample_level()
        level = models.Level.objects.all()
        serializer = serializers.LevelSerializer(level, many=True, context=serializer_context)

        res = self.client.get(LEVEL_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_level_detail(self):
        """test retrieving a level's detail"""
        level = sample_level()
        serializer = serializers.LevelSerializer(level, context=serializer_context)
        
        url = level_detail_url(level_id=level.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_level(self):
        """test creating a level"""
        payload = {
            'code': 400,
        }

        res = self.client.post(LEVEL_URL, payload)

        level = models.Level.objects.get(id=res.data['id'])
        level_serializer = serializers.LevelSerializer(level, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        test_all_model_attributes(self, payload, level, level_serializer)

    def test_partial_update_level(self):
        """test partially updating a level's detail using patch"""
        level = sample_level()        
        payload = {
            'code': 300,
        }

        url = level_detail_url(level.id)
        res = self.client.patch(url, payload)

        level.refresh_from_db()
        level_serializer = serializers.LevelSerializer(level, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        test_all_model_attributes(self, payload, level, level_serializer)

    def test_full_update_level(self):
        """test updating a level's detail using put"""
        level = sample_level()        
        payload = {
            'code': 200,
        }

        url = level_detail_url(level.id)
        res = self.client.put(url, payload)

        level.refresh_from_db()
        level_serializer = serializers.LevelSerializer(level, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        test_all_model_attributes(self, payload, level, level_serializer)
