import jwt
from django.conf import settings
from api.models import User
from rest_framework.exceptions import AuthenticationFailed

class CheckJWT :

    def get_user (token) :
        payload = jwt.decode(token, settings.SECRET_KEY)

        try :
            user = User.objects.get(pk=payload['user_id'], email=payload['email'])
        except User.DoesNotExist :
            raise AuthenticationFailed('해당 서버에서 발급 된 JWT가 아닙니다.')

        return user