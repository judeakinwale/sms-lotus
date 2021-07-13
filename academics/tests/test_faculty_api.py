from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory
from academics import models, serializers


FACULTY_URL = reverse('academics:faculty-list')

# creating a test request
factory = APIRequestFactory()
request = factory.get('/')
# create serializer context
serializer_context = {'request': Request(request)}


def faculty_detail_url(faculty_id):
    """return url for the faculty detail"""
    return reverse('academics:faculty-detail', args=[faculty_id])


def sample_faculty(**kwargs):
    """create and return a sample faculty"""
    defaults = {'name': 'Faculty 1'}
    defaults.update(kwargs)
    return models.Faculty.objects.create(**defaults)


def test_all_model_attributes(insance, payload, model, serializer):
    """test model attributes against a payload, with instance being self in a testcase class """
    ignored_keys = ['image']
    relevant_keys = sorted(set(payload.keys()).difference(ignored_keys))
    for key in relevant_keys:
        try:
            insance.assertEqual(payload[key], getattr(model, key))
        except:
            insance.assertEqual(payload[key], serializer.data[key])


class PublicFacultyApiTest(TestCase):
    """test public access to the faculty api"""

    def setUp(self):
        self.client = APIClient()

    def test_authentication_required(self):
        """test that authentication is required"""
        res = self.client.get(FACULTY_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        # self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateFacultyApiTest(TestCase):
    """test authenticated access to the faculty api"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@email.com',
            password='testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_faculty(self):
        """test retrieving a list of faculty"""
        sample_faculty()
        faculty = models.Faculty.objects.all()
        serializer = serializers.FacultySerializer(faculty, many=True, context=serializer_context)

        res = self.client.get(FACULTY_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_faculty_detail(self):
        """test retrieving a faculty's detail"""
        faculty = sample_faculty()
        serializer = serializers.FacultySerializer(faculty, context=serializer_context)
        
        url = faculty_detail_url(faculty_id=faculty.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_faculty(self):
        """test creating a faculty"""
        payload = {
            'name': 'Faculty 2',
            'description': 'some description text',
        }

        res = self.client.post(FACULTY_URL, payload)

        faculty = models.Faculty.objects.get(id=res.data['id'])
        faculty_serializer = serializers.FacultySerializer(faculty, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        test_all_model_attributes(self, payload, faculty, faculty_serializer)

    def test_partial_update_faculty(self):
        """test partially updating a faculty's detail using patch"""
        faculty = sample_faculty()        
        payload = {
            'description': 'some description text',
        }

        url = faculty_detail_url(faculty.id)
        res = self.client.patch(url, payload)

        faculty.refresh_from_db()
        faculty_serializer = serializers.FacultySerializer(faculty, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        test_all_model_attributes(self, payload, faculty, faculty_serializer)

    def test_full_update_faculty(self):
        """test updating a faculty's detail using put"""
        faculty = sample_faculty()        
        payload = {
            'name': 'Faculty 3',
            'description': 'some description text',
        }

        url = faculty_detail_url(faculty.id)
        res = self.client.put(url, payload)

        faculty.refresh_from_db()
        faculty_serializer = serializers.FacultySerializer(faculty, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        test_all_model_attributes(self, payload, faculty, faculty_serializer)
