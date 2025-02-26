from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import get_user_model

token_generator = PasswordResetTokenGenerator()
APP_NAME = "myapp"

def generate_password_reset_token(user):
    # Ensure user is a Django user model instance
    UserModel = get_user_model()
    if not isinstance(user, UserModel):
        raise ValueError("The user must be a Django user model instance.")

    # Generate a unique token
    token = token_generator.make_token(user)

    # Use the user's primary key (integer ID) as the UID
    uid = str(user.pk)

    return uid, token

def create_deep_link(user):
    """Create a deep link for password reset"""
    uid, token = generate_password_reset_token(user)
    deep_link = f"{APP_NAME}://reset-password?uid={uid}&token={token}"
    return deep_link