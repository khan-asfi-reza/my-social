from faker import Faker
from factory.django import DjangoModelFactory
from apps.accounts import User
from pytest_factoryboy import register

faker = Faker()


class UserFactory(DjangoModelFactory):
    username = faker.user_name()
    first_name = faker.first_name()
    last_name = faker.last_name()
    password = faker.uuid4(str)
    phone_number = faker.phone_number()
    email = faker.email()

    class Meta:
        model = User


register(UserFactory, "users")
