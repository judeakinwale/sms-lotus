from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory
from assessment import models, serializers


ANSWER_URL = reverse('assessment:answer-list')

# creating a test request
factory = APIRequestFactory()
request = factory.get('/')
# create serializer context
serializer_context = {'request': Request(request)}


def answer_detail_url(answer_id):
    """return url for the answer detail"""
    return reverse('assessment:answer-detail', args=[answer_id])


def sample_quiz(supervisor, **kwargs):
    """create and return a sample quiz"""
    defaults = {'name': 'Sample Quiz'}
    defaults.update(kwargs)
    return models.Quiz.objects.create(supervisor=supervisor, **defaults)


def sample_question(quiz, **kwargs):
    """create and return a sample question"""
    defaults = {'label': 'Sample Question Label'}
    defaults.update(kwargs)
    return models.Question.objects.create(quiz=quiz, **defaults)


def sample_answer(question, **kwargs):
    """create and return sample answer"""
    defaults = {'text': 'some text'}
    defaults.update(kwargs)
    return models.Answer.objects.create(question=question, **defaults)


# def sample_answer_image(answer, **kwargs):
#     """create and return a sample answer image"""
#     defaults = {
#         'description': 'sample answer image'
#     }
#     defaults.update(kwargs)
#     return models.AnswerImage.create(answer=answer, **defaults)



def test_all_model_attributes(insance, payload, model, serializer):
    """test model attributes against a payload, with instance being self in a testcase class """
    ignored_keys = ['image']
    relevant_keys = sorted(set(payload.keys()).difference(ignored_keys))
    for key in relevant_keys:
        try:
            insance.assertEqual(payload[key], getattr(model, key))
        except:
            insance.assertEqual(payload[key], serializer.data[key])


class PublicAnswerApiTest(TestCase):
    """test public access to the answer api"""

    def setUp(self):
        self.client = APIClient()

    def test_authentication_required(self):
        """test that authentication is required"""
        res = self.client.get(ANSWER_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        # self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateAnswerApiTest(TestCase):
    """test authenticated access to the answer api"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@email.com',
            password='testpass'
        )
        self.client.force_authenticate(self.user)
        self.quiz = sample_quiz(supervisor=self.user)
        self.question = sample_question(quiz=self.quiz)

    def tearDown(self):
        pass

    def test_retrieve_answer(self):
        """test retrieving a list of answers"""
        sample_answer(question=self.question)
        answer = models.Answer.objects.all()
        serializer = serializers.AnswerSerializer(answer, many=True, context=serializer_context)

        res = self.client.get(ANSWER_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    # # TODO:
    # def test_answers_limited_to_question(self):
    #     """test that answers from a specified questions is returned"""
    #     sample_answer(question=self.question)
    #     user2 = get_user_model().objects.create_user(
    #         'test2@test.com',
    #         'testpass2'
    #     )
    #     quiz = sample_quiz(supervisor=user2, name='Test Quiz 3')
    #     question = sample_question(quiz=quiz)
    #     answer = sample_answer(question=question)

    #     specified_question = models.Question.objects.get(answer=answer)
    #     specified_quiz = models.Quiz.objects.get(question=question)

    #     print(f"{question}, {specified_question}")
    #     print(f"{quiz}, {specified_quiz}")
    #     print(quiz.question_set.get(id=question.id).answer_set.all())

    #     answers = models.Answer.objects.filter(question=question)
    #     serializer = serializers.AnswerSerializer(answers, many=True, context=serializer_context)

    #     res = self.client.get(ANSWER_URL)

    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(res.data, serializer.data)
    #     self.assertEqual(question, specified_question)
    #     self.assertEqual(len(res.data), 1)

    def test_retrieve_answer_detail(self):
        """test retrieving an answer's detail"""
        answer = sample_answer(question=self.question)
        serializer = serializers.AnswerSerializer(answer, context=serializer_context)

        url = answer_detail_url(answer_id=answer.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_answer(self):
        """test creating an answer"""
        question_serializer = serializers.QuestionSerializer(self.question, context=serializer_context)
        payload = {
            'question': question_serializer.data['url'],
            'text': 'Test text 2',
            'is_correct': True
        }

        res = self.client.post(ANSWER_URL, payload)

        answer = models.Answer.objects.get(id=res.data['id'])
        answer_serializer = serializers.AnswerSerializer(answer, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        test_all_model_attributes(self, payload, answer, answer_serializer)

    def test_partial_update_answer(self):
        """test partially updating an answer's detail using patch"""
        answer = sample_answer(question=self.question)
        payload = {
            'text': 'An updated text'
        }

        url = answer_detail_url(answer.id)
        res = self.client.patch(url, payload)

        answer.refresh_from_db()
        answer_serializer = serializers.AnswerSerializer(answer, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        test_all_model_attributes(self, payload, answer, answer_serializer)

    def test_full_update_answer(self):
        """test updating an answer's detail using put"""
        answer = sample_answer(question=self.question)
        question = sample_question(quiz=self.quiz, label='Label 2')
        question_serializer = serializers.QuestionSerializer(question, context=serializer_context)
        payload = {
            'question': question_serializer.data['url'],
            'text': 'Test text 3',
            'is_correct': True
        }

        url = answer_detail_url(answer.id)
        res = self.client.put(url, payload)

        answer.refresh_from_db()
        answer_serializer = serializers.AnswerSerializer(answer, context=serializer_context)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        test_all_model_attributes(self, payload, answer, answer_serializer)
