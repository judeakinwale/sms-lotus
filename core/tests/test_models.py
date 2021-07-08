import tempfile
from PIL import Image
from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models as cmodels
from information import models as imodels


def sample_user(email='test@email.com', password='testpass'):
    return get_user_model().objects.create_user(email, password)


def sample_scope(description='test', **kwargs):
    return imodels.Scope.objects.create(description=description, **kwargs)


class ModelTest(TestCase):

    def test_scope_str(self):
        """test the scope str representation"""
        scope = imodels.Scope.objects.create(
            description='Test'
        )
        self.assertEqual(str(scope), scope.description)

    def test_information_str(self):
        """test the information str representation"""
        information = imodels.Information.objects.create(
            source=sample_user(),
            scope=sample_scope(),
            title='Test title',
            body='some test text'
        )
        expected_str = f"{information.title} for {information.scope}"
        self.assertEqual(str(information), expected_str)

    def test_notice_str(self):
        """test the notice str representation"""
        notice = imodels.Notice.objects.create(
            source=sample_user(),
            scope=sample_scope(),
            title='Test title',
            message='This is a test notice'
        )
        self.assertEqual(str(notice), notice.title)

    def test_information_image_str(self):
        """test the information image str representation"""
        information = imodels.Information.objects.create(
            source=sample_user(),
            scope=sample_scope(),
            title='Test title',
            body='some test text with an image'
        )
        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            img = Image.new('RGB', (10, 10))
            img.save(ntf, format='JPEG')
            ntf.seek(0)

            info_img = imodels.InformationImage.objects.create(
                information=information,
                image=ntf.name,
                description="A blue 10px image"
            )

        self.assertEqual(str(info_img), info_img.description)
