from chat.models import Chat, User, UserChat, UserMessage


class UserRepository:

    def __init__(self, Session):
        self.Session = Session


    def get_all_users(self):
        with self.Session() as session:
            return session.query(User).all()

    
    def get_user(self, user_id=None, username=None):
        if user_id:
            with self.Session() as session:
                return session.query(User).filter(User.id==user_id).first()

        if username:
            with self.Session() as session:
                return session.query(User).filter(User.username==username).first()

    
    def get_user_chats(self, user_id, status=None):
        with self.Session() as session:
            queryset = session.query(Chat)

            if type(status) is int:
                queryset = queryset.filter(Chat.status==status)
            
            return queryset.join(UserChat).join(User).filter(User.id==user_id).all()

    
    def get_user_messages(self, sender=None, receiver=None, time_delivered=None):
        with self.Session() as session:
            queryset = session.query(UserMessage)

            if sender:
                queryset = queryset.filter(UserMessage.sender==sender)
            
            if receiver:
                queryset = queryset.filter(UserMessage.receiver==receiver)
            
            if time_delivered:
                queryset = queryset.filter(UserMessage.time_delivered==time_delivered)
            
            return queryset.all()


class ChatRepository:

    def __init__(self, Session):
        self.Session = Session


    def get_chats_amount(self, status=None):
        with self.Session() as session:
            queryset = session.query(Chat)
            
            if type(status) is int:
                queryset = queryset.filter(Chat.status==status)

            return queryset.count()


    def get_chat_messages_amount(self, chat_id):
        with self.Session() as session:
            users = session.query(UserChat.user).filter(UserChat.chat == chat_id).all()
            user_ids = [user_id for (user_id,) in users]
            queryset = session.query(UserMessage)
            messages = queryset.filter(UserMessage.sender.in_(user_ids) | UserMessage.receiver.in_(user_ids))
            
            return messages.count()
