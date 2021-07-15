import tempfile
from PIL import Image
from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models as cmodels
from information import models as imodels
from assessment import models as amodels


def sample_user(email='test@email.com', password='testpass'):
    return get_user_model().objects.create_user(email, password)


def sample_scope(description='test', **kwargs):
    return imodels.Scope.objects.create(description=description, **kwargs)


# def sample_quiz(supervisor=sample_user(), **kwargs):
#     defaults = {
#         'name': 'Test quiz',
#         'description': 'This is a test quiz description',
#     }
#     defaults.update(kwargs)
#     return amodels.Quiz.objects.create(supervisor=supervisor, **defaults)


# def sample_question(quiz=sample_quiz(), **kwargs):
#     defaults = {
#         'label': 'Test title'
#     }
#     defaults.update(kwargs)
#     return amodels.Question.objects.create(quiz=quiz, **defaults)


# def sample_answer(question=sample_question(), **kwargs):
#     defaults = {
#         'text': 'some answer text',
#     }
#     defaults.update(kwargs)
#     return amodels.Answer.objects.create(question=question, **defaults)


# def sample_quiz_taker(student=sample_user(), quiz=sample_quiz(), **kwargs):
#     defaults = {}
#     defaults.update(kwargs)
#     return amodels.QuizTaker.objects.create(student=student, quiz=quiz, **defaults)


class ModelTest(TestCase):

    def setUp(self):
        self.user = sample_user()
    #     self.quiz = sample_quiz()
    #     self.question = sample_question()
    #     self.answer = sample_answer()
    #     self.quiz_taker = sample_quiz_taker()

    def test_scope_str(self):
        """test the scope str representation"""
        scope = imodels.Scope.objects.create(
            description='Test'
        )
        self.assertEqual(str(scope), scope.description)

    def test_information_str(self):
        """test the information str representation"""
        information = imodels.Information.objects.create(
            source=self.user,
            scope=sample_scope(),
            title='Test title',
            body='some test text'
        )
        expected_str = f"{information.title} for {information.scope}"
        self.assertEqual(str(information), expected_str)

    def test_notice_str(self):
        """test the notice str representation"""
        notice = imodels.Notice.objects.create(
            source=self.user,
            scope=sample_scope(),
            title='Test title',
            message='This is a test notice'
        )
        self.assertEqual(str(notice), notice.title)

    def test_information_image_str(self):
        """test the information image str representation"""
        information = imodels.Information.objects.create(
            source=self.user,
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

    def test_quiz_str(self):
        """test the quiz str representation"""
        quiz = amodels.Quiz.objects.create(
            supervisor=self.user,
            name='Test quiz',
            description='This is a test quiz description'
        )
        self.assertEqual(str(quiz), quiz.name)

    def test_question_str(self):
        """test the question str representation"""
        quiz = amodels.Quiz.objects.create(
            supervisor=self.user,
            name='Test quiz',
            description='This is a test quiz description'
        )
        question = amodels.Question.objects.create(
            quiz = quiz,
            label='Test title',
        )
        self.assertEqual(str(question), question.label)

    def test_answer_str(self):
        """test the answer str representation"""
        quiz = amodels.Quiz.objects.create(
            supervisor=self.user,
            name='Test quiz',
            description='This is a test quiz description'
        )
        question = amodels.Question.objects.create(
            quiz = quiz,
            label='Test title',
        )
        answer = amodels.Answer.objects.create(
            question=question,
            text='some answer text',
        )
        self.assertEqual(str(answer), answer.text)

    def test_quiz_taker_str(self):
        """test the quiz_taker str representation"""
        quiz = amodels.Quiz.objects.create(
            supervisor=self.user,
            name='Test quiz',
            description='This is a test quiz description'
        )
        quiz_taker = amodels.QuizTaker.objects.create(
            student=self.user,
        )
        quiz_taker.quiz.add(quiz)
        self.assertEqual(str(quiz_taker), str(quiz_taker.student))

    def test_response_str(self):
        """test the response str representation"""
        quiz = amodels.Quiz.objects.create(
            supervisor=self.user,
            name='Test quiz',
            description='This is a test quiz description'
        )
        quiz_taker = amodels.QuizTaker.objects.create(
            student=self.user,
        )
        question = amodels.Question.objects.create(
            quiz = quiz,
            label='Test title',
        )
        answer = amodels.Answer.objects.create(
            question=question,
            text='some answer text',
        )
        response = amodels.Response.objects.create(
            quiz_taker=quiz_taker,
            question=question,
            answer=answer,
        )
        self.assertEqual(str(response), response.question.label)
