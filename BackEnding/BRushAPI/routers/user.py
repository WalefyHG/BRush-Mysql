
from datetime import datetime, timedelta, timezone
from ninja import Router, UploadedFile, File
from typing import List, Optional
from ..schema import UserChangePassword, UserIn, UserLogin, UserOut, UserPut, UserResponse, UserSocialMedias
from ..models import User, UserCode
from django.contrib.auth.hashers import check_password, make_password
from rest_framework_simplejwt.tokens import AccessToken
from ninja.errors import HttpError
from django.core.mail import send_mail
import random, threading, string


router = Router()

def sending_code(user):
    try:
        # Verifica se já existe um código para o usuário
        existing_code = UserCode.objects.filter(user_id=user).first()

        if existing_code:
            # Se existir, atualiza o código e a validade
            code = generate_verification_code()
            existing_code.verification_code = code["code"]
            existing_code.verification_code_expires = code["verification_code_expires"]
            existing_code.save()
            user_code = existing_code
        else:
            # Se não existir, cria um novo código
            code = generate_verification_code()
            user_code = UserCode.objects.create(
                user_id=user,
                verification_code=code["code"],
                verification_code_expires=code["verification_code_expires"]
            )
            user_code.save()
            user_code_id = user_code.id

        timer = threading.Timer(600, delete_verification_code, args=[user_code.id])  # 600 segundos = 10 minutos
        timer.start()
        
        subject = '🌟 Bem-vindo ao Nosso Site 🌟'
        mensagem = f'''
             <html>

  <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f2f2f2;">
    <div style="background-color: #222; border-radius: 10px; padding: 20px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); color: white;">
      <h2>Olá {user.user_firstName}! 😊</h2>
      <p style="font-size: 16px; line-height: 24px; color: #dfd7d7; text-align: justify;">
        Esperamos que você esteja bem. Para garantir a segurança da sua conta na
        Plataforma B-Rush 🚀, estamos implementando um processo de verificação
        adicional. Por favor, siga as instruções abaixo para concluir a
        verificação:
      </p>
      <p style="font-size: 16px; line-height: 24px; color: #dfd7d7; text-align: justify;">Nome de Usuário: <strong style="font-size: 16px;line-height: 24px; color: #d407e7;">{user.user_name}</strong></p>
      <p style="font-size: 16px; line-height: 24px; color: #dfd7d7; text-align: justify;">
        Código de Verificação: <strong style="font-size: 16px;line-height: 24px; color: #d407e7;">{code["code"]}</strong>
      </p>
      <p style="font-size: 16px; line-height: 24px; color: #dfd7d7; text-align: justify;">
        Este código é válido por 10 minutos. Certifique-se de inseri-lo assim que possível para evitar
        quaisquer inconvenientes no acesso à sua conta.
      </p>
      <p style="font-size: 16px; line-height: 24px; color: #dfd7d7; text-align: justify;">
        Se você não solicitou este código ou tem alguma dúvida, por favor, entre
        em contato conosco imediatamente respondendo a este e-mail. Estamos aqui
        para ajudar.
      </p>
      <p style="font-size: 16px; line-height: 24px; color: #dfd7d7; text-align: justify;">Agradecemos pela sua cooperação.</p>
      <pre style=" font-size: 16px; line-height: 24px; color: #dfd7d7;">
    Atenciosamente,

    Suporte
    B-Rush Suporte
    brushsuporte@gmail.com
      </pre>
    </div>
  </body>
</html>
        '''
        from_email = 'BRushSuporte@gmail.com'
        recipient_list = [user.user_email]
        send_mail(subject, 
                  '', 
                  from_email, 
                  recipient_list, 
                  fail_silently=False, 
                  auth_user='brushsuporte@gmail.com', 
                  auth_password='bgqs qwmw iimh jxzj',
                  html_message=mensagem
                  )
        return {"mensagem": "Enviado com sucesso", "code": code["code"]}
    except User.DoesNotExist:
        return {"mensagem": "Usuário não encontrado"}


def generate_verification_code():
    code = ''.join(random.choice(string.digits) for _ in range(6))
    verification_code_expires = datetime.now(timezone.utc) + timedelta(minutes=10)
    return {"code": code, "verification_code_expires": verification_code_expires}

def delete_verification_code(user_code_id):
    try:
        user_code = UserCode.objects.get(id=user_code_id)
        user_code.delete()
    except UserCode.DoesNotExist:
        pass
    except Exception as e:
        print(f"Erro ao excluir código: {e}")

@router.get('/perfil', response=UserOut)
def get_user_by_token(request):
    return request.auth

@router.get('/perfil/{user_name}', response=UserOut)
def get_user_perfil_by_userName(request, user_name: str):
    user_data = User.objects.get(
        user_name=user_name
    )
    return user_data

@router.post("/criando", response=UserResponse, auth=None)
def create_user(request, user: UserIn, image: Optional[UploadedFile] = File(None)):
    password_hash = make_password(user.user_password)
    user_data = User.objects.create(
        user_name=user.user_name,
        user_email=user.user_email,
        user_password=password_hash,
        user_birthday=user.user_birthday,
        user_firstName=user.user_firstName,
        user_lastName=user.user_lastName,
        user_image= image,
        user_idioma= user.user_idioma,
        user_games= user.user_games,
        user_pais= user.user_pais
    )
    
    user_data.save()
    return {"mensagem": "Usuário criado com sucesso!"}

@router.post("/login", auth=None)
def login(request, user: UserLogin):
    try:
        user_data = User.objects.get(user_email=user.user_email)

        # Adicione a verificação de código aqui
        if check_password(user.user_password, user_data.user_password):
            if user_data.is_confirmed:
                response = {"mensagem": "Usuário logado com sucesso!"}
                token = AccessToken.for_user(user_data)
                return {"response": response, "token": str(token)}
            else:
                verification_code = sending_code(user_data)
                response = {"mensagem": "Código de verificação enviado", "code": verification_code["code"]}
                token = AccessToken.for_user(user_data)
                return {"response": response, "token": str(token)}
        else:
            return 400, {"message":"Credenciais inválidas"}
    except User.DoesNotExist:
        raise HttpError(404, detail="Usuário não encontrado")


@router.get("/pesquisar/{user_firstName}", response=List[UserOut])
def get_user_by_id(request, user_firstName: str):
    user_data =  User.objects.filter(
        user_firstName__icontains=user_firstName
    )
    return user_data

@router.put("/atualizar/{id}", response=UserOut)
def update_by_id(request, id: int, user: UserPut, image: Optional[UploadedFile] = File(None), banner: Optional[UploadedFile] = File(None)):
    user_data = User.objects.get(user_id=id)
    if user.user_name:
        user_data.user_name = user.user_name
    if user.user_email:
        user_data.user_email = user.user_email
    if user.user_birthday:
        user_data.user_birthday = user.user_birthday
    if image:
        user_data.user_image = image
    if user.user_idioma:
        user_data.user_idioma = user.user_idioma
    if user.user_games:
        user_data.user_games = user.user_games
    if user.user_pais:
        user_data.user_pais = user.user_pais
    if banner:
        user_data.user_banner = banner
    user_data.save()
    
    return user_data

@router.delete("/deletar", response=UserResponse)
def delete_user_by_id(request):
    user_data = request.auth
    user_data.delete()
    return {"mensagem": "Usuário deletado com sucesso!"}
  
@router.post('/enviar_codigo', response=UserResponse)
def send_code(request):
    user = request.auth
    return sending_code(user)

@router.post('/verificar_codigo/{code}', response=UserResponse)
def verify_code(request, code: str):
    try:
        user = request.auth
        user_code = UserCode.objects.get(verification_code=code, user_id=user.user_id)
        if user_code.verification_code_expires > datetime.now(timezone.utc):
            user.is_confirmed = True
            user.save()
            user_code.delete()
            return {"mensagem": "Código verificado com sucesso"}
        else:
            user_code.delete()
            return {"mensagem": "Código expirado"}
    except UserCode.DoesNotExist:
        return {"mensagem": "Código não encontrado"}
    
@router.put('/atualizar_senha', response=UserResponse)
def update_password(request, change_password: UserChangePassword):
    user = request.auth
    if change_password.senha_nova == change_password.confirmar_senha:
        if check_password(change_password.senha_atual, user.user_password):
            user.user_password = make_password(change_password.senha_nova)
            user.save()
            return {"mensagem": "Senha atualizada com sucesso"}
        else:
            return HttpError(400, "Senha atual incorreta")
    else:
        return HttpError(402, "As senhas não coincidem")
    

@router.put('/atualizar_redes_sociais', response=UserOut)
def update_social_medias(request, user: UserSocialMedias):
    user_data = request.auth
    if user.user_youtube:
        user_data.user_youtube = user.user_youtube
    if user.user_twitch:
        user_data.user_twitch = user.user_twitch
    if user.user_instagram:
        user_data.user_instagram = user.user_instagram
    if user.user_twitter:
        user_data.user_twitter = user.user_twitter
    user_data.save()
    return user_data