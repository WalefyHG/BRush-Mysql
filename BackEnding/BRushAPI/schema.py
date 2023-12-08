from typing import List, Optional
from datetime import date
from ninja import Schema

class UserIn(Schema):
    user_name: str
    user_email: str
    user_password: str
    user_birthday: date = None
    user_lastName: str = None
    user_firstName: str = None
    user_idioma: str = None
    user_games: str = None
    user_pais: str = None
class UserOut(Schema):
    user_id: int
    user_name: str
    user_email: str
    user_password: str
    user_birthday: date = None
    user_firstName: str = None
    user_lastName: str = None
    user_image: str = None
    user_idioma: str = None
    user_games: str = None
    user_pais: str = None
    user_banner: str = None
    user_youtube : str = None
    user_twitch : str = None
    user_instagram : str = None
    user_twitter : str = None
    is_confirmed: bool = None

class UserResponse(Schema):
    mensagem: str
    

class UserSocialMedias(Schema):
    user_twitter: str = None
    user_youtube : str = None
    user_twitch : str = None
    user_instagram : str = None
class UserLogin(Schema):
    user_email: str
    user_password: str
    
class UserPut(Schema):
    user_name: Optional[str] = ''
    user_email: Optional[str] = ''
    user_birthday: date = None
    user_idioma: Optional[str] = ''
    user_games: Optional[str] = ''
    user_pais: Optional[str] = ''


class UserChangePassword(Schema):
    senha_atual: str
    senha_nova: str
    confirmar_senha: str

class TeamIn(Schema):
    team_name: str
    
class TeamOut(Schema):
    team_name: str
    team_member: List[UserOut] = None

class TeamResponse(Schema):
    mensagem: str
    

class TeamAssing(Schema):
    user_id: List[int]
    team_id: int


class NoticeIn(Schema):
    notice_title: str
    notice_content: str
    notice_date: date = None

class NoticeOut(Schema):
    notice_id: int
    notice_title: str
    notice_content: str
    notice_date: date = None
    notice_writer: UserOut = None