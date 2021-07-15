from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory
from assessment import models, serializers


QUIZTAKER_URL = reverse('assessment:quiztaker-list')

# creating a test request
factory = APIRequestFactory()
request = factory.get('/')
# create serializer context
serializer_context = {'request': Request(request)}


def quiz_taker_detail_url(quiz_taker_id):
    """return url for the quiz_taker detail"""
    return reverse('assessment:quiztaker-detail', args=[quiz_taker_id])


def sample_quiz(supervisor, **kwargs):
    """create and return a sample quiz"""
    defaults = {'name': 'Sample Quiz'}
    defaults.update(kwargs)
    return models.Quiz.objects.create(supervisor=supervisor, **defaults)


def sample_quiz_taker(student, quiz, **kwargs):
    """create and return a sample quiz_taker"""
    defaults = {}
    defaults.update(kwargs)
    quiz_taker = models.QuizTaker.objects.create(student=student, **defaults)
    quiz_taker.quiz.add(quiz)
    return quiz_taker


# def sample_quiz_taker_image(quiz_taker, **kwargs):
#     """create and return a sample quiz_taker image"""
#     defaults = {}
#     defaults.update(kwargs)
#     return models.QuizTakerImage.create(quiz_taker=quiz_taker, **defaults)



def test_all_model_attributes(insance, payload, model, serializer):
    """test model attributes against a payload, with instance being self in a testcase class """
    ignored_keys = ['image']
    relevant_keys = sorted(set(payload.keys()).difference(ignored_keys))
    for key in relevant_keys:
        try:
            insance.assertEqual(payload[key], getattr(model, key))
        except:
            insance.assertEqual(payload[key], serializer.data[key])


class PublicQuizTakerApiTest(TestCase):
    """test public access to the quiz_taker api"""

    def setUp(self):
        self.client = APIClient()

    def test_authentication_required(self):
        """test that authentication is required"""
        res = self.client.get(QUIZTAKER_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        # self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateQuizTakerApiTest(TestCase):
    """test authenticated access to the quiz_taker api"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@email.com',
            password='testpass'
        )
        self.client.force_authenticate(self.user)
        self.quiz = sample_quiz(supervisor=self.user)

    def tearDown(self):
        pass

    def test_retrieve_quiz_taker(self):
        """test retrieving a list of quiz_takers"""
        sample_quiz_taker(student=self.user, quiz=self.quiz)
        quiz_taker = models.QuizTaker.objects.all()
        serializer = serializers.QuizTakerSerializer(quiz_taker, many=True, context=serializer_context)

        res = self.client.get(QUIZTAKER_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    # # TODO:
    # def test_quiz_taker_limited_to_quiz(self):
    #     """test that quiz_taker from a specified quiz is returned"""
    #     sample_quiz_taker(student=self.user, quiz=self.quiz)
    #     user2 = get_user_model().objects.create_user(
    #         'test2@test.com',
    #         'testpass2'
    #     )
    #     quiz = sample_quiz(supervisor=user2, name='Test Quiz 3')
    #     quiz_taker = sample_quiz_taker(student=self.user, quiz=quiz)

    #     quiz_takers = models.QuizTaker.objects.filter(quiz=quiz)
    #     serializer = serializers.QuizTakerSerializer(quiz_takers, many=True, context=serializer_context)
        
    #     res = self.client.get(QUIZTAKER_URL)

    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(res.data, serializer.data)
    #     self.assertEqual(len(res.data), 1)

    def test_retrieve_quiz_taker_detail(self):
        """test retrieving a quiz_taker's detail"""
        quiz_taker = sample_quiz_taker(student=self.user, quiz=self.quiz)
        serializer = serializers.QuizTakerSerializer(quiz_taker, context=serializer_context)
        
        url = quiz_taker_detail_url(quiz_taker_id=quiz_taker.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_quiz_taker(self):
        """test creating a quiz_taker"""
        quiz_serializer = serializers.QuizSerializer(self.quiz, context=serializer_context)
        payload = {
            'student': self.user.id,
            'quiz': [quiz_serializer.data['url'],],
        }

        res = self.client.post(QUIZTAKER_URL, payload)

        quiz_taker = models.QuizTaker.objects.get(id=res.data['id'])
        quiz_taker_serializer = serializers.QuizTakerSerializer(quiz_taker, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        test_all_model_attributes(self, payload, quiz_taker, quiz_taker_serializer)

    def test_partial_update_quiz_taker(self):
        """test partially updating a quiz_taker's detail using patch"""
        quiz_taker = sample_quiz_taker(student=self.user, quiz=self.quiz)
        payload = {
            'completed': True,
        }

        url = quiz_taker_detail_url(quiz_taker.id)
        res = self.client.patch(url, payload)

        quiz_taker.refresh_from_db()
        quiz_taker_serializer = serializers.QuizTakerSerializer(quiz_taker, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        test_all_model_attributes(self, payload, quiz_taker, quiz_taker_serializer)

    def test_full_update_quiz_taker(self):
        """test updating a quiz_taker's detail using put"""
        quiz_taker = sample_quiz_taker(student=self.user, quiz=self.quiz)
        quiz = sample_quiz(supervisor=self.user)
        quiz_serializer = serializers.QuizSerializer(quiz, context=serializer_context)
        payload = {
            'student': self.user.id,
            'quiz': [quiz_serializer.data['url'],]
        }

        url = quiz_taker_detail_url(quiz_taker.id)
        res = self.client.put(url, payload)

        quiz_taker.refresh_from_db()
        quiz_taker_serializer = serializers.QuizTakerSerializer(quiz_taker, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        test_all_model_attributes(self, payload, quiz_taker, quiz_taker_serializer)
