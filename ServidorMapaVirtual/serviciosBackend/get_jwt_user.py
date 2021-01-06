from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

class Json_web_token():
    def get_token_user(self, user):
        token_refresh = TokenObtainPairSerializer().get_token(user)
        token_access = AccessToken().for_user(user)
        token = {
            "refresh": str(token_refresh),
            'access': str(token_access)
        }
        return token