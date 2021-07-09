from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory
from information import models, serializers


SCOPE_URL = reverse('information:scope-list')

# creating a test request
factory = APIRequestFactory()
request = factory.get('/')
# create serializer context
serializer_context = {'request': Request(request)}


def scope_detail_url(scope_id):
    """return url for the scope detail"""
    return reverse('information:scope-detail', args=[scope_id])


def sample_scope(description='General', **kwargs):
    """create and return a sample scope"""
    defaults = {}
    defaults.update(kwargs)
    return models.Scope.objects.create(description=description, **defaults)


def test_all_model_attributes(insance, payload, model, serializer):
    """test model attributes against a payload, with instance being self in a testcase class """
    ignored_keys = ['image']
    relevant_keys = sorted(set(payload.keys()).difference(ignored_keys))
    for key in relevant_keys:
        try:
            insance.assertEqual(payload[key], getattr(model, key))
        except:
            insance.assertEqual(payload[key], serializer.data[key])


class PublicScopeApiTest(TestCase):
    """test public access to the scope api"""

    def setUp(self):
        self.client = APIClient()

    def test_authentication_required(self):
        """test that authentication is required"""
        res = self.client.get(SCOPE_URL)
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

    def test_retrieve_scopes(self):
        """test retrieving a list of scopes"""
        sample_scope()
        scopes = models.Scope.objects.all()
        serializer = serializers.ScopeSerializer(scopes, many=True, context=serializer_context)

        res = self.client.get(SCOPE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    # # TODO:
    # # test scopes displayed are limited by filters like faculty departmment course programme level
    # def test_scope_limited_to_source(self):
    #     """test that scope from all sources is returned"""
    #     sample_scope(source=self.user)
    #     # user2 = get_user_model().objects.create_user(
    #     #     'test2@test.com',
    #     #     'testpass2'
    #     # )
    #     scope = models.Scope.objects.all()
    #     serializer = serializers.ScopeSerializer(scope, many=True, context=serializer_context)
        
    #     res = self.client.get(SCOPE_URL)

    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(res.data, serializer.data)
    #     # self.assertEqual(len(res.data), 2)

    def test_retrieve_scope_detail(self):
        """test retrieving a scope detail"""
        scope = sample_scope()
        serializer = serializers.ScopeSerializer(scope, context=serializer_context)
        
        url = scope_detail_url(scope_id=scope.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_scope(self):
        """test creating an scope"""
        payload = {
            'description': 'Test Scope',
            'is_general': False,
        }

        res = self.client.post(SCOPE_URL, payload)

        scope = models.Scope.objects.get(id=res.data['id'])
        scope_serializer = serializers.ScopeSerializer(scope, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        test_all_model_attributes(self, payload, scope, scope_serializer)

    def test_partial_update_scope(self):
        """test partially updating a scope's detail using patch"""
        scope = sample_scope()
        payload = {
            'is_general': False,
        }

        url = scope_detail_url(scope.id)
        res = self.client.patch(url, payload)

        scope.refresh_from_db()
        scope_serializer = serializers.ScopeSerializer(scope, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        test_all_model_attributes(self, payload, scope, scope_serializer)

    def test_full_update_scope(self):
        """test updating a scope's detail using put"""
        scope = sample_scope()
        payload = {
            'description': 'Test scope 2',
        }

        url = scope_detail_url(scope.id)
        res = self.client.put(url, payload)

        scope.refresh_from_db()
        scope_serializer = serializers.ScopeSerializer(scope, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        test_all_model_attributes(self, payload, scope, scope_serializer)
