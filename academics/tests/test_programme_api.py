from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory
from academics import models, serializers


PROGRAMME_URL = reverse('academics:programme-list')

# creating a test request
factory = APIRequestFactory()
request = factory.get('/')
# create serializer context
serializer_context = {'request': Request(request)}


def programme_detail_url(programme_id):
    """return url for the programme detail"""
    return reverse('academics:programme-detail', args=[programme_id])


def sample_faculty(**kwargs):
    """create and return a sample faculty"""
    defaults = {'name': 'Faculty 1'}
    defaults.update(kwargs)
    return models.Faculty.objects.create(**defaults) 


def sample_department(faculty, **kwargs):
    """create and return a sample department"""
    defaults = {'name': 'Department 1'}
    defaults.update(kwargs)
    return models.Department.objects.create(faculty=faculty, **defaults)


def sample_level(**kwargs):
    """create and return a sample level"""
    defaults = {'code': 100}
    defaults.update(**kwargs)
    return models.Level.objects.create(**defaults)


def sample_programme(department, max_level, **kwargs):
    """create and return a sample programme"""
    defaults = {
        'name': 'Programme 1',
        'max_level': max_level,
    }
    defaults.update(kwargs)
    return models.Programme.objects.create(department=department, **defaults)


def test_all_model_attributes(insance, payload, model, serializer):
    """test model attributes against a payload, with instance being self in a testcase class """
    ignored_keys = ['image']
    relevant_keys = sorted(set(payload.keys()).difference(ignored_keys))
    for key in relevant_keys:
        try:
            insance.assertEqual(payload[key], getattr(model, key))
        except:
            insance.assertEqual(payload[key], serializer.data[key])


class PublicProgrammeApiTest(TestCase):
    """test public access to the programme api"""

    def setUp(self):
        self.client = APIClient()

    def test_authentication_required(self):
        """test that authentication is required"""
        res = self.client.get(PROGRAMME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        # self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateProgrammeApiTest(TestCase):
    """test authenticated access to the programme api"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@email.com',
            password='testpass'
        )
        self.client.force_authenticate(self.user)
        self.faculty = sample_faculty()
        self.department =sample_department(faculty=self.faculty)
        self.level = sample_level()

    def test_retrieve_programme(self):
        """test retrieving a list of programmes"""
        sample_programme(department=self.department, max_level=self.level)
        programme = models.Programme.objects.all()
        serializer = serializers.ProgrammeSerializer(programme, many=True, context=serializer_context)

        res = self.client.get(PROGRAMME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_programme_detail(self):
        """test retrieving a programme's detail"""
        programme = sample_programme(department=self.department, max_level=self.level)
        serializer = serializers.ProgrammeSerializer(programme, context=serializer_context)
        
        url = programme_detail_url(programme_id=programme.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_programme(self):
        """test creating a programme"""
        department = sample_department(faculty=self.faculty, name='Department 2')
        department_serializer = serializers.DepartmentSerializer(department, context=serializer_context)
        level_serializer = serializers.LevelSerializer(self.level, context=serializer_context)
        payload = {
            'department': department_serializer.data['url'],
            'name': 'Programme 2',
            'max_level': level_serializer.data['url'],
            'description': 'some description text',
        }

        res = self.client.post(PROGRAMME_URL, payload)

        programme = models.Programme.objects.get(id=res.data['id'])
        programme_serializer = serializers.ProgrammeSerializer(programme, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        test_all_model_attributes(self, payload, programme, programme_serializer)

    def test_partial_update_programme(self):
        """test partially updating a programme's detail using patch"""
        programme = sample_programme(department=self.department, max_level=self.level)        
        payload = {
            'description': 'some description text',
        }

        url = programme_detail_url(programme.id)
        res = self.client.patch(url, payload)

        programme.refresh_from_db()
        programme_serializer = serializers.ProgrammeSerializer(programme, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        test_all_model_attributes(self, payload, programme, programme_serializer)

    def test_full_update_programme(self):
        """test updating a programme's detail using put"""
        programme = sample_programme(department=self.department, max_level=self.level)
        department = sample_department(faculty=self.faculty, name='Department 3')
        department_serializer = serializers.DepartmentSerializer(department, context=serializer_context)
        level_serializer = serializers.LevelSerializer(self.level, context=serializer_context)
        payload = {
            'department': department_serializer.data['url'],
            'name': 'Programme 3',
            'max_level': level_serializer.data['url'],
            'description': 'some description text',
        }

        url = programme_detail_url(programme.id)
        res = self.client.put(url, payload)

        programme.refresh_from_db()
        programme_serializer = serializers.ProgrammeSerializer(programme, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        test_all_model_attributes(self, payload, programme, programme_serializer)
