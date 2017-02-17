from time import time
from uuid import uuid4


def user_hash_middleware(get_response):
    """
    Middleware добавляет уникальный идентификатор для
    пользователя. В реальной жизни это может быть IP
    или просто можно использовать user.id, если сервис
    предполагает авторизацию.

    Чтобы было интереснее, каждые 5 минут сбрасываем
    идентификатор и просмотр будет засчитан заново
    """
    def middleware(request):
        session_user_hash = request.session.get('user_hash')
        timestamp = int(time())
        if session_user_hash is None or timestamp - session_user_hash[1] > 60 * 5:
            session_user_hash = [str(uuid4()), timestamp]
            request.session['user_hash'] = session_user_hash
        request.user_hash = session_user_hash[0]
        response = get_response(request)
        return response
    return middleware
