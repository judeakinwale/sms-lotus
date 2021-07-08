from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory
from information import models, serializers
import tempfile
from PIL import Image


INFO_IMG_URL = reverse('information:informationimage-list')

# creating a test request
factory = APIRequestFactory()
request = factory.get('/')
# create serializer context
serializer_context = {'request': Request(request)}


def info_image_detail_url(info_img_id):
    """return url for the information detail"""
    return reverse('information:informationimage-detail', args=[info_img_id])


def sample_scope(description='General', **kwargs):
    """create and return a sample scope"""
    defaults = {}
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


def sample_information_image(information, **kwargs):
    """create and return a sample information image"""
    defaults = {
        'description': 'Test description'
    }
    defaults.update(kwargs)
    return models.InformationImage.objects.create(information=information, **defaults)


def test_all_model_attributes(insance, payload, model, serializer):
    """test model attributes against a payload, with instance being self in a testcase class """
    ignored_keys = ['image']
    relevant_keys = sorted(set(payload.keys()).difference(ignored_keys))
    for key in relevant_keys:
        try:
            insance.assertEqual(payload[key], getattr(model, key))
        except:
            insance.assertEqual(payload[key], serializer.data[key])


class PublicInformationImageApiTest(TestCase):
    """test public access to the information image api"""

    def setUp(self):
        self.client = APIClient()

    def test_authentication_required(self):
        """test that authentication is required"""
        res = self.client.get(INFO_IMG_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateInformationApiTest(TestCase):
    """test authenticated access to the information image api"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@email.com',
            password='testpass'
        )
        self.client.force_authenticate(self.user)
        self.image = models.InformationImage.objects.create(
            information=sample_information(self.user),
            description='test image'
        )
        self.info = sample_information(self.user)

    def tearDown(self):
        pass

    def test_retrieve_information_images(self):
        """test retrieving a list of information image"""
        sample_information_image(information=self.info)
        info_img = models.InformationImage.objects.all()
        serializer = serializers.InformationImageSerializer(info_img, many=True, context=serializer_context)

        res = self.client.get(INFO_IMG_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    # def test_information_images_limited_to_information(self):
    #     """test that only information images from linked information is returned"""
    #     user2 = get_user_model().objects.create_user(
    #         'test2@test.com',
    #         'testpass2'
    #     )
    #     info2 = sample_information(source=user2)
    #     sample_information_image(information=self.info)
    #     sample_information_image(information=info2)
        
    #     res = self.client.get(INFO_IMG_URL)

    #     images = models.InformationImage.objects.filter(information=self.info)
    #     serializer = serializers.InformationImageSerializer(images, many=True, context=serializer_context)

    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(res.data, serializer.data)
    #     self.assertEqual(len(res.data), 2)

    def test_retrieve_informtion_image_detail(self):
        """test retrieving an information image detail"""
        info_img = sample_information_image(information=self.info)
        serializer = serializers.InformationImageSerializer(info_img, context=serializer_context)
        
        url = info_image_detail_url(info_img_id=info_img.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_simple_information_image(self):
        """test creating an information image without an image file"""
        info_serializer = serializers.InformationSerializer(self.info, context=serializer_context)
        payload = {
            'information': info_serializer.data['url'],
        }

        res = self.client.post(INFO_IMG_URL, payload)

        info_img = models.InformationImage.objects.get(id=res.data['id'])
        info_img_serializer = serializers.InformationImageSerializer(info_img, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        test_all_model_attributes(self, payload, info_img, info_img_serializer)

    def test_create_full_information_image(self):
        """test creating an information image with an image file"""
        info_serializer = serializers.InformationSerializer(self.info, context=serializer_context)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            img = Image.new('RGB', (10, 10), 'blue')
            img.save(ntf, format='JPEG')
            ntf.seek(0)

            payload = {
                'information': info_serializer.data['url'],
                'image': ntf,
                'description': 'Test image description'
            }

            res = self.client.post(INFO_IMG_URL, payload)

        info_img = models.InformationImage.objects.get(id=res.data['id'])
        info_img_serializer = serializers.InformationImageSerializer(info_img, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn('image', res.data)
        test_all_model_attributes(self, payload, info_img, info_img_serializer)

    def test_partial_update_information_image(self):
        """test partially updating an information image's detail using patch"""
        info_img = sample_information_image(information=self.info)
        payload = {
            'description': 'Test image description'
        }

        url = info_image_detail_url(info_img.id)
        res = self.client.patch(url, payload)

        info_img.refresh_from_db()
        info_img_serializer = serializers.InformationImageSerializer(info_img, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        test_all_model_attributes(self, payload, info_img, info_img_serializer)

    def test_full_update_information(self):
        """test updating an information's detail using put"""
        info_img = sample_information_image(information=self.info)
        info_serializer = serializers.InformationSerializer(self.info, context=serializer_context)
        url = info_image_detail_url(info_img.id)

        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            img = Image.new('RGB', (10, 10), 'blue')
            img.save(ntf, format='JPEG')
            ntf.seek(0)
            
            payload = {
                'information': info_serializer.data['url'],
                'image': ntf,
                'description': 'Test image description'
            }

            res = self.client.put(url, payload)

        info_img.refresh_from_db()
        info_img_serializer = serializers.InformationImageSerializer(info_img, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)
        test_all_model_attributes(self, payload, info_img, info_img_serializer)

    def test_upload_invalid_image_fails(self):
        """test updating an information image with an invalid image file"""
        info_img = sample_information_image(information=self.info)
        payload = {
            'image': 'invalid',
            'description': 'Test image description'
        }

        url = info_image_detail_url(info_img.id)
        res = self.client.patch(url, payload)

        info_img.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
