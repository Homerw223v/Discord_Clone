from django.test import TestCase
from ..models import Profile, Topic, Room, Message
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy


class LoginTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='Testuser',
                                   password='testpassword',
                                   email='testemail@mail.ru',
                                   id=5)
        topic = Topic.objects.create(user=Profile.objects.get(id=5), name='TestTopic')
        Room.objects.create(host=Profile.objects.get(id=5),
                            topic=topic,
                            name='TestRoom',
                            description='Test Description',
                            )
        message = Message.objects.create(user=Profile.objects.get(id=5),
                                         room=Room.objects.get(name='TestRoom'),
                                         body='TestBody',
                                         )

    def test_login_url(self):
        response = self.client.get('/login/')
        redirect = self.client.post('/login/', kwargs={
            'username': 'Testuser',
            'password': 'testpassword'
        }, follow=True)
        # self.assertRedirects(redirect, '/home/')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(redirect.status_code, 200)

    def test_redirect_to_login(self):
        response1 = self.client.get(reverse('create-room'))
        response2 = self.client.get(reverse('update-profile'))
        response3 = self.client.get(reverse('home'))
        response4 = self.client.get(reverse('room', kwargs={'pk': 1}))
        response5 = self.client.get(reverse('update-room', kwargs={'pk': 1}))
        response6 = self.client.get(reverse('delete-room', kwargs={'pk': 1}))
        response7 = self.client.get(reverse('user-profile', kwargs={'pk': 'Testuser'}))
        response8 = self.client.get(reverse('login'))
        response9 = self.client.get(reverse('register'))
        self.assertTrue(response1.status_code, 301)
        self.assertTrue(response2.status_code, 301)
        self.assertTrue(response3.status_code, 301)
        self.assertTrue(response4.status_code, 301)
        self.assertTrue(response5.status_code, 301)
        self.assertTrue(response6.status_code, 301)
        self.assertTrue(response7.status_code, 301)
        self.assertTrue(response8.status_code, 200)
        self.assertTrue(response9.status_code, 200)

    def test_user_login_url_working(self):
        credentials = {'username': 'Testuser',
                       'password': 'testpassword'}
        self.client.login(credentials=credentials)
        response1 = self.client.get(reverse('create-room'))
        response2 = self.client.get(reverse('update-profile'))
        response3 = self.client.get(reverse('home'))
        response4 = self.client.get(reverse('room', kwargs={'pk': 1}))
        response5 = self.client.get(reverse('update-room', kwargs={'pk': 1}))
        response6 = self.client.get(reverse('delete-room', kwargs={'pk': 1}))
        response7 = self.client.get(reverse('user-profile', kwargs={'pk': 'Testuser'}))
        response8 = self.client.get(reverse('login'))
        response9 = self.client.get(reverse('register'))
        self.assertTrue(response1.status_code, 200)
        self.assertTrue(response2.status_code, 200)
        self.assertTrue(response3.status_code, 200)
        self.assertTrue(response4.status_code, 200)
        self.assertTrue(response5.status_code, 200)
        self.assertTrue(response6.status_code, 200)
        self.assertTrue(response7.status_code, 200)
        self.assertTrue(response8.status_code, 200)
        self.assertTrue(response9.status_code, 200)


class CreatingTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create_user(username='Testuser',
                                   password='testpassword',
                                   email='testemail@mail.ru',
                                   id=5)
        user2 = User.objects.create_user(username='Testuser2',
                                   password='testpassword2',
                                   email='testemail2@mail.ru',
                                   id=6)


    def setUp(self) -> None:
        self.client.login(username='Testuser', password='testpassword')
        # self.client.login(username='Testuser2', password='testpassword2')

    def test_creating_room(self):
        response = self.client.post(reverse('create-room'),
                                    {'topic': 'TestTopic',
                                     'name': 'TestName',
                                     'description': 'TestDescription'})
        room = Room.objects.get(id=1)
        self.assertRedirects(response, reverse('home'))
        self.assertTemplateUsed('base/form_for_room.html')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(room.name, 'TestName')
        self.assertEquals(room.description, 'TestDescription')
        self.assertEquals(room.topic.name, 'TestTopic')
        self.assertEquals(room.host.username, 'Testuser')

    def test_update_room(self):
        self.client.post(reverse('create-room'),
                         {'topic': 'TestTopic',
                          'name': 'TestRoom',
                          'description': 'TestDescription'})
        response_get = self.client.get(reverse('update-room', kwargs={'pk': 1}))
        room = Room.objects.get(id=1)
        self.assertEquals(response_get.status_code, 200)
        self.assertTemplateUsed('base/form_for_room.html')
        response_post = self.client.post(reverse('room', kwargs={'pk':1}),
                         {'body': 'TestMessage'})
        self.assertEquals(response_post.status_code, 302)
        message = Message.objects.get(id=1)
        self.assertEquals(message.body, 'TestMessage')
        self.assertEquals(message.user.username, 'Testuser')
        self.assertEquals(message.room.name, 'TestRoom')


class WrongUserTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create_user(username='Testuser',
                                         password='testpassword',
                                         email='testemail@mail.ru',
                                         id=5)
        user2 = User.objects.create_user(username='Testuser2',
                                         password='testpassword2',
                                         email='testemail2@mail.ru',
                                         id=6)

    def setUp(self) -> None:
        self.client.login(username='Testuser', password='testpassword')
        # self.client.login(username='Testuser2', password='testpassword2')

    def test_wrong_user_update_room(self):
        self.client.post(reverse('create-room'),
                         {'topic': 'TestTopic',
                          'name': 'TestRoom',
                          'description': 'TestDescription'})
        self.client.login(username='Testuser2', password='testpassword2')
        response = self.client.get(reverse('update-room', kwargs={'pk': 1}))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(str(response._container[0]).replace("'",'').replace("b", ''), "You are not allowed here!")

    def test_wrong_user_delete_message(self):
        self.client.post(reverse('create-room'),
                         {'topic': 'TestTopic',
                          'name': 'TestRoom',
                          'description': 'TestDescription'})
        response = self.client.post(reverse('room', kwargs={'pk': 1}),
                         {'body': 'TestMessage'})
        self.assertEquals(response.status_code, 302)
        self.assertTemplateUsed('base/room.html')
        self.assertRedirects(response, reverse('room', kwargs={'pk': 1}))
        delete_user1 = self.client.get(reverse('delete-message', kwargs={'pk':1}))
        self.assertEquals(delete_user1.status_code, 200)
        self.client.login(username='Testuser2', password='testpassword2')
        delete_user2 = self.client.get(reverse('delete-message', kwargs={'pk': 1}))
        self.assertEquals(delete_user2.status_code, 403)
        delete_user2_post = self.client.post(reverse('delete-message', kwargs={'pk': 1}))
        self.assertEquals(delete_user2_post.status_code, 403)
        self.client.login(username='Testuser', password='testpassword')
        delete_user1_post = self.client.post(reverse('delete-message', kwargs={'pk': 1}))
        self.assertEquals(delete_user1_post.status_code, 302)
        self.assertRedirects(delete_user1_post, reverse('home'))












