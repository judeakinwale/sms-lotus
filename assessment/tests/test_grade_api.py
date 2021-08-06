# from django.contrib.auth import get_user_model
# from django.test import TestCase
# from django.urls import reverse
# from rest_framework import status
# from rest_framework.request import Request
# from rest_framework.test import APIClient, APIRequestFactory
# from assessment import models, serializers


# GRADE_URL = reverse('assessment:grade-list')

# # creating a test request
# factory = APIRequestFactory()
# request = factory.get('/')
# # create serializer context
# serializer_context = {'request': Request(request)}


# def grade_detail_url(grade_id):
#     """return url for the grade detail"""
#     return reverse('assessment:grade-detail', args=[grade_id])


# def sample_quiz(supervisor, **kwargs):
#     """create and return a sample quiz"""
#     defaults = {'name': 'Sample Quiz'}
#     defaults.update(kwargs)
#     return models.Quiz.objects.create(supervisor=supervisor, **defaults)


# def sample_grade(quiz, **kwargs):
#     """create and return a sample grade"""
#     defaults = {'label': 'Sample Grade Label'}
#     defaults.update(kwargs)
#     return models.Grade.objects.create(quiz=quiz, **defaults)


# # def sample_grade_image(grade, **kwargs):
# #     """create and return a sample grade image"""
# #     defaults = {}
# #     defaults.update(kwargs)
# #     return models.GradeImage.create(grade=grade, **defaults)



# def test_all_model_attributes(insance, payload, model, serializer):
#     """test model attributes against a payload, with instance being self in a testcase class """
#     ignored_keys = ['image']
#     relevant_keys = sorted(set(payload.keys()).difference(ignored_keys))
#     for key in relevant_keys:
#         try:
#             insance.assertEqual(payload[key], getattr(model, key))
#         except:
#             insance.assertEqual(payload[key], serializer.data[key])


# class PublicGradeApiTest(TestCase):
#     """test public access to the grade api"""

#     def setUp(self):
#         self.client = APIClient()

#     def test_authentication_required(self):
#         """test that authentication is required"""
#         res = self.client.get(GRADE_URL)
#         self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
#         # self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


# class PrivateGradeApiTest(TestCase):
#     """test authenticated access to the grade api"""

#     def setUp(self):
#         self.client = APIClient()
#         self.user = get_user_model().objects.create_user(
#             email='test@email.com',
#             password='testpass'
#         )
#         self.client.force_authenticate(self.user)
#         self.quiz = sample_quiz(supervisor=self.user)

#     def tearDown(self):
#         pass

#     def test_retrieve_grade(self):
#         """test retrieving a list of grades"""
#         sample_grade(quiz=self.quiz)
#         grade = models.Grade.objects.all()
#         serializer = serializers.GradeSerializer(grade, many=True, context=serializer_context)

#         res = self.client.get(GRADE_URL)

#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data, serializer.data)

#     # # TODO:
#     # def test_grade_limited_to_quiz(self):
#     #     """test that grade from a specified quiz is returned"""
#     #     sample_grade(quiz=self.quiz)
#     #     user2 = get_user_model().objects.create_user(
#     #         'test2@test.com',
#     #         'testpass2'
#     #     )
#     #     quiz = sample_quiz(supervisor=user2, name='Test Quiz 3')
#     #     grade = sample_grade(quiz=quiz)

#     #     grades = models.Grade.objects.filter(quiz=quiz)
#     #     serializer = serializers.GradeSerializer(grades, many=True, context=serializer_context)
        
#     #     res = self.client.get(GRADE_URL)

#     #     self.assertEqual(res.status_code, status.HTTP_200_OK)
#     #     self.assertEqual(res.data, serializer.data)
#     #     self.assertEqual(len(res.data), 1)

#     def test_retrieve_grade_detail(self):
#         """test retrieving a grade's detail"""
#         grade = sample_grade(quiz=self.quiz)
#         serializer = serializers.GradeSerializer(grade, context=serializer_context)
        
#         url = grade_detail_url(grade_id=grade.id)
#         res = self.client.get(url)

#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data, serializer.data)

#     def test_create_grade(self):
#         """test creating a grade"""
#         quiz_serializer = serializers.QuizSerializer(self.quiz, context=serializer_context)
#         payload = {
#             'quiz': quiz_serializer.data['url'],
#             'label': 'Test label 2',
#         }

#         res = self.client.post(GRADE_URL, payload)

#         grade = models.Grade.objects.get(id=res.data['id'])
#         grade_serializer = serializers.GradeSerializer(grade, context=serializer_context)

#         self.assertEqual(res.status_code, status.HTTP_201_CREATED)
#         test_all_model_attributes(self, payload, grade, grade_serializer)

#     def test_partial_update_grade(self):
#         """test partially updating a grade's detail using patch"""
#         grade = sample_grade(quiz=self.quiz)
#         quiz = sample_quiz(supervisor=self.user)
#         quiz_serializer = serializers.QuizSerializer(quiz, context=serializer_context)
#         payload = {
#             'quiz': quiz_serializer.data['url'],
#             'label': 'An updated label'
#         }

#         url = grade_detail_url(grade.id)
#         res = self.client.patch(url, payload)

#         grade.refresh_from_db()
#         grade_serializer = serializers.GradeSerializer(grade, context=serializer_context)

#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         test_all_model_attributes(self, payload, grade, grade_serializer)

#     def test_full_update_grade(self):
#         """test updating a grade's detail using put"""
#         grade = sample_grade(quiz=self.quiz, label='label2')
#         quiz = sample_quiz(supervisor=self.user)
#         quiz_serializer = serializers.QuizSerializer(quiz, context=serializer_context)
#         payload = {
#             'quiz': quiz_serializer.data['url'],
#             'label': 'Test label 3',
#             'order': 1,
#         }

#         url = grade_detail_url(grade.id)
#         res = self.client.put(url, payload)

#         grade.refresh_from_db()
#         grade_serializer = serializers.GradeSerializer(grade, context=serializer_context)

#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         test_all_model_attributes(self, payload, grade, grade_serializer)
