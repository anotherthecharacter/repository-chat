import pytest
from uuid import uuid4

from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from chat.models import Base, Chat, User, UserChat, UserMessage
from chat.repositories import ChatRepository, UserRepository


eric_id = uuid4()
john_id = uuid4()
daniel_id = uuid4()


@pytest.fixture(scope="module")
def testdb():
    engine = create_engine(f"postgresql://{config('DB_USER')}:{config('DB_PASSWORD')}@127.0.0.1:5432/test_repository_chat")
    Base.metadata.create_all(bind=engine)

    yield engine
    
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def testsession(testdb):
    Session = sessionmaker(bind=testdb)

    with Session() as session:
        user1 = User(
            id=eric_id,
            username="Eric"
        )
        user2 = User(
            id=john_id,
            username="John",
            photo_url="https://moonvillageassociation.org/wp-content/uploads/2018/06/default-profile-picture1.jpg"
        )
        user3 = User(
            id=daniel_id,
            username="Daniel"
        )
        chat1 = Chat(id=1, name="EricJohn", status=1, updated_at=0)
        chat2 = Chat(id=2, name="EricDaniel", status=0, updated_at=0)
        user_chat1 = UserChat(id=1, user=eric_id, chat=1)
        user_chat2 = UserChat(id=2, user=john_id, chat=1)
        user_chat3 = UserChat(id=3, user=eric_id, chat=2)
        user_message1 = UserMessage(id=1, sender=eric_id, receiver=john_id, text="Hello", is_delivered=True)
        user_message2 = UserMessage(id=2, sender=john_id, receiver=eric_id, text="Hi")

        session.add_all((
            user1, user2, user3, chat1,
            chat2, user_chat1, user_chat2, user_chat3,
            user_message1, user_message2
        ))
        session.commit()

    yield Session


def test_get_all_users(testdb, testsession):
    user_repository = UserRepository(testsession)
    users = user_repository.get_all_users()

    assert len(users) == 3


def test_get_user(testdb, testsession):
    user_repository = UserRepository(testsession)
    user1 = user_repository.get_user(user_id=eric_id)
    user2 = user_repository.get_user(username="John")

    assert user1.username == "Eric"
    assert user2.username == "John"


def test_get_user_chats(testdb, testsession):
    user_repository = UserRepository(testsession)
    user_chats = user_repository.get_user_chats(user_id=john_id, status=1)

    assert user_chats[0].name == "EricJohn"
    assert len(user_chats) == 1


def test_get_user_messages(testdb, testsession):
    user_repository = UserRepository(testsession)
    user_messages = user_repository.get_user_messages()

    assert len(user_messages) == 2
    assert user_messages[0].text == "Hello"
    assert user_messages[1].text == "Hi"


def test_get_chats_amount(testdb, testsession):
    chat_repository = ChatRepository(testsession)
    chat_count = chat_repository.get_chats_amount(status=0)

    assert chat_count == 1


def test_get_chat_messages_amount(testdb, testsession):
    chat_repository = ChatRepository(testsession)
    message_count = chat_repository.get_chat_messages_amount(chat_id=1)

    assert message_count == 2
