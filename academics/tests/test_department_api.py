from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory
from academics import models, serializers


DEPARTMENT_URL = reverse('academics:department-list')

# creating a test request
factory = APIRequestFactory()
request = factory.get('/')
# create serializer context
serializer_context = {'request': Request(request)}


def department_detail_url(department_id):
    """return url for the department detail"""
    return reverse('academics:department-detail', args=[department_id])


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


def test_all_model_attributes(insance, payload, model, serializer):
    """test model attributes against a payload, with instance being self in a testcase class """
    ignored_keys = ['image']
    relevant_keys = sorted(set(payload.keys()).difference(ignored_keys))
    for key in relevant_keys:
        try:
            insance.assertEqual(payload[key], getattr(model, key))
        except:
            insance.assertEqual(payload[key], serializer.data[key])


class PublicDepartmentApiTest(TestCase):
    """test public access to the department api"""

    def setUp(self):
        self.client = APIClient()

    def test_authentication_required(self):
        """test that authentication is required"""
        res = self.client.get(DEPARTMENT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        # self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateDepartmentApiTest(TestCase):
    """test authenticated access to the department api"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@email.com',
            password='testpass'
        )
        self.client.force_authenticate(self.user)
        self.faculty =sample_faculty()

    def test_retrieve_department(self):
        """test retrieving a list of departments"""
        sample_department(faculty=self.faculty)
        department = models.Department.objects.all()
        serializer = serializers.DepartmentSerializer(department, many=True, context=serializer_context)

        res = self.client.get(DEPARTMENT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_department_detail(self):
        """test retrieving a department's detail"""
        department = sample_department(faculty=self.faculty)
        serializer = serializers.DepartmentSerializer(department, context=serializer_context)
        
        url = department_detail_url(department_id=department.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_department(self):
        """test creating a department"""
        faculty = sample_faculty(name='Faculty 2')
        serializer = serializers.FacultySerializer(faculty, context=serializer_context)
        payload = {
            'faculty': serializer.data['url'],
            'name': 'Department 2',
            'description': 'some description text',
        }

        res = self.client.post(DEPARTMENT_URL, payload)

        department = models.Department.objects.get(id=res.data['id'])
        department_serializer = serializers.DepartmentSerializer(department, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        test_all_model_attributes(self, payload, department, department_serializer)

    def test_partial_update_department(self):
        """test partially updating a department's detail using patch"""
        department = sample_department(faculty=self.faculty)        
        payload = {
            'description': 'some description text',
        }

        url = department_detail_url(department.id)
        res = self.client.patch(url, payload)

        department.refresh_from_db()
        department_serializer = serializers.DepartmentSerializer(department, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        test_all_model_attributes(self, payload, department, department_serializer)

    def test_full_update_department(self):
        """test updating a department's detail using put"""
        department = sample_department(faculty=self.faculty)
        faculty = sample_faculty(name='Faculty 3')
        faculty_serializer = serializers.FacultySerializer(faculty, context=serializer_context)        
        payload = {
            'faculty': faculty_serializer.data['url'],
            'name': 'Department 3',
            'description': 'some description text',
        }

        url = department_detail_url(department.id)
        res = self.client.put(url, payload)

        department.refresh_from_db()
        department_serializer = serializers.DepartmentSerializer(department, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        test_all_model_attributes(self, payload, department, department_serializer)
