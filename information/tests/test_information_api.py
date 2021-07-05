from decimal import Context
from logging import INFO, info
import re
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.serializers import Serializer
from rest_framework.test import APIClient, APIRequestFactory
from information import models, serializers


INFO_URL = reverse('information:information-list')

# creating a test request
factory = APIRequestFactory()
request = factory.get('/')
# create serializer contexr
from django.db.models.fields import DecimalField
serializer_context = {'request': Request(request)}


def info_detail_url(info_id):
    """return url for the information detail"""
    return reverse('information:information-detail', args=[info_id])


def sample_scope(description='General', **kwargs):
    """create and return a sample scope"""
    defaults = {
        # 'description': 'General',
    }
    defaults.update(kwargs)
    return models.Scope.objects.create(description=description, **defaults)


def sample_information(source, **kwargs):
    """create and return sample information"""
    defaults = {
        'scope': sample_scope(),
        'title': 'Test title',
        'body': 'Lorem ipsum dolor sit amet',
    }
    defaults.update(kwargs)
    return models.Information.objects.create(source=source, **defaults)


def sample_info_image(information, **kwargs):
    """create and return a sample info image"""
    defaults = {
        'description': 'sample information image'
    }
    defaults.update(kwargs)
    return models.InformationImage.create(information=information, **defaults)


class PublicInformationApiTest(TestCase):
    """test public access to the information api"""

    def setUp(self):
        self.client = APIClient()

    def test_authentication_required(self):
        """test that authentication is required"""
        res = self.client.get(INFO_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        # self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateInformationApiTest(TestCase):
    """test authenticated access to the information api"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@email.com',
            password='testpass'
        )
        self.client.force_authenticate(self.user)

    def tearDown(self):
        pass

    def test_retrieve_information(self):
        """test retrieving a list of information"""
        sample_information(source=self.user)
        info = models.Information.objects.all()
        serializer = serializers.InformationSerializer(info, many=True, context=serializer_context)

        res = self.client.get(INFO_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_information_not_limited_to_source(self):
        """test that information from all sources is returned"""
        sample_information(source=self.user)
        user2 = get_user_model().objects.create_user(
            'test2@test.com',
            'testpass2'
        )
        sample_information(source=user2)

        info = models.Information.objects.all()
        serializer = serializers.InformationSerializer(info, many=True, context=serializer_context)
        
        res = self.client.get(INFO_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(len(res.data), 2)

    def test_retrieve_informtion_detail(self):
        """test retrieving an information's detail"""
        info = sample_information(source=self.user)
        serializer = serializers.InformationSerializer(info, context=serializer_context)
        
        url = info_detail_url(info_id=info.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_information(self):
        """test creating an information"""
        serializer = serializers.ScopeSerializer(sample_scope(), context=serializer_context)
        payload = {
            'source': self.user,
            'scope': serializer.data['url'],
            'title': 'Test title 2',
            'body': 'body for test title 2',
        }

        res = self.client.post(INFO_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        info = models.Information.objects.get(id=res.data['id'])
        # for key in payload.keys():
        #     self.assertEqual(payload[key], getattr(info, key))
        self.assertEqual(payload['source'], info.source)
        self.assertEqual(payload['title'], info.title)
        self.assertEqual(payload['body'], info.body)

    def test_partial_update_information(self):
        """test partially updating an information's detail"""
        info = sample_information(source=self.user)
        scope2 = sample_scope(description='Private', is_general=False)
        serializer = serializers.ScopeSerializer(scope2, context=serializer_context)
        payload = {
            'scope': serializer.data['url'],
            'body': 'An updated body'
        }

        url = info_detail_url(info.id)
        res = self.client.patch(url, payload)

        info.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # for key in payload.keys():
        #     self.assertEqual(payload[key], getattr(info, key))
        self.assertEqual(payload['body'], info.body)
