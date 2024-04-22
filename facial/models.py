from itsdangerous import URLSafeTimedSerializer as  Serializer
from facial import db
from facial import db,login_manager, app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.Text,unique=True,nullable=False)
    email = db.Column(db.Text,unique=True,nullable=False)
    password = db.Column(db.Text,nullable=False)

    # Generate a unique password reset token
    def get_reset_token(self,expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')
    
    # Validate the token is not invalid or expired
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
    
    def __repr__(self) -> str:
        return f"User('{self.username}','{self.email}')"
