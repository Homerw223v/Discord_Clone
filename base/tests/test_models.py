from django.test import TestCase
from ..models import Profile, Topic, Message, Room
from django.contrib.auth.models import User


class ProfileTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='Testuser',
                                   password='testpassword',
                                   email='testemail@mail.ru',
                                   id=5)

    def test_name(self):
        profile = Profile.objects.get(id=5)
        field_label = profile._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_email(self):
        profile = Profile.objects.get(id=5)
        field_label = profile._meta.get_field('email').verbose_name
        self.assertEquals(field_label, 'email')

    def test_profile_image(self):
        profile = Profile.objects.get(id=5)
        field_label = profile._meta.get_field('profile_image').verbose_name
        self.assertEquals(field_label, 'profile image')

    def test_bio(self):
        profile = Profile.objects.get(id=5)
        field_label = profile._meta.get_field('bio').verbose_name
        self.assertEquals(field_label, 'About')

    def test_profileid_userid(self):
        profile = Profile.objects.get(id=5)
        id = profile._meta.get_field('id')
        self.assertEquals(5, profile.id)


class TopicTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='Testuser',
                                   password='testpassword',
                                   email='testemail@mail.ru',
                                   id=5)
        topic = Topic.objects.create(user=Profile.objects.get(id=5),
                                     name='TestTopic')

    def test_user(self):
        topic = Topic.objects.get(id=1)
        verbose_name = topic._meta.get_field('user').verbose_name
        self.assertEquals(verbose_name, 'user')

    def test_name(self):
        topic = Topic.objects.get(id=1)
        verbose_name = topic._meta.get_field('name').verbose_name
        self.assertEquals(verbose_name, 'name')
        self.assertEquals(topic.name, 'TestTopic')


class RoomTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='Testuser',
                                   password='testpassword',
                                   email='testemail@mail.ru',
                                   id=5)
        topic = Topic.objects.create(user=Profile.objects.get(id=5), name='TestTopic')
        room = Room.objects.create(host=Profile.objects.get(id=5),
                                   topic=topic,
                                   name='TestRoom',
                                   description='Test Description',
                                   )

    def test_host(self):
        room = Room.objects.get(id=1)
        verbose_name = room._meta.get_field('host').verbose_name
        self.assertEquals('Testuser', room.host.username)
        self.assertEquals(verbose_name, 'host')

    def test_topic(self):
        room = Room.objects.get(id=1)
        verbose_name = room._meta.get_field('topic').verbose_name
        self.assertEquals('TestTopic', room.topic.name)
        self.assertEquals(verbose_name, 'topic')

    def test_name(self):
        room = Room.objects.get(id=1)
        verbose_name = room._meta.get_field('name').verbose_name
        self.assertEquals('TestRoom', room.name)
        self.assertEquals(verbose_name, 'name')

    def test_description(self):
        room = Room.objects.get(id=1)
        verbose_name = room._meta.get_field('description').verbose_name
        self.assertEquals('Test Description', room.description)
        self.assertEquals(verbose_name, 'description')

    def test_participants(self):
        room = Room.objects.get(id=1)
        verbose_name = room._meta.get_field('participants').verbose_name
        self.assertEquals(verbose_name, 'participants')

    def test_updated(self):
        room = Room.objects.get(id=1)
        verbose_name = room._meta.get_field('updated').verbose_name
        self.assertEquals(verbose_name, 'updated')

    def test_created(self):
        room = Room.objects.get(id=1)
        verbose_name = room._meta.get_field('created').verbose_name
        self.assertEquals(verbose_name, 'created')


class MessageTestCase(TestCase):
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

    def test_user(self):
        message = Message.objects.get(id=1)
        verbose_name = message._meta.get_field('user').verbose_name
        self.assertEquals('Testuser', message.user.username)
        self.assertEquals(verbose_name, 'user')

    def test_room(self):
        message = Message.objects.get(id=1)
        verbose_name = message._meta.get_field('room').verbose_name
        self.assertEquals('TestRoom', message.room.name)
        self.assertEquals(verbose_name, 'room')

    def test_body(self):
        message = Message.objects.get(id=1)
        verbose_name = message._meta.get_field('body').verbose_name
        self.assertEquals('TestBody', message.body)
        self.assertEquals(verbose_name, 'body')

    def test_created(self):
        message = Message.objects.get(id=1)
        verbose_name = message._meta.get_field('created').verbose_name
        self.assertEquals(verbose_name, 'created')

    def test_updated(self):
        message = Message.objects.get(id=1)
        verbose_name = message._meta.get_field('updated').verbose_name
        self.assertEquals(verbose_name, 'updated')
