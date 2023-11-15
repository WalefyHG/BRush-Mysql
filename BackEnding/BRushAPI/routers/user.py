from ninja import Router, UploadedFile, File
from typing import List, Optional
from ..schema import UserIn, UserLogin, UserOut, UserPut, UserResponse
from ..models import User
from django.contrib.auth.hashers import check_password, make_password
from rest_framework_simplejwt.tokens import AccessToken
from ninja.errors import HttpError

router = Router()


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
        user_image= image
    )
    user_data.save()
    return {"mensagem": "Usuário criado com sucesso!"}

@router.post("/login", auth=None)
def login(request, user: UserLogin):
    try:
        user_data = User.objects.get(user_email=user.user_email)
        if check_password(user.user_password, user_data.user_password):
            response = {"mensagem": "Usuário logado com sucesso!"}
            token = AccessToken.for_user(user_data)
            return {"response": response, "token": str(token)}
        else:
            raise HttpError(400, detail="Credenciais inválidas")
    except User.DoesNotExist:
        raise HttpError(404, detail="Usuário não encontrado")

@router.get("/pesquisar/{user_firstName}", response=List[UserOut])
def get_user_by_id(request, user_firstName: str):
    user_data =  User.objects.filter(
        user_firstName__icontains=user_firstName
    )
    return user_data

@router.put("/atualizar/{user_id}", response=UserResponse)
def update_by_id(request, user_id: int, user: UserPut, image: Optional[UploadedFile] = File(None)):
    user_data = User.objects.get(user_id=user_id)
    if user.user_name:
        user_data.user_name = user.user_name
    if user.user_email:
        user_data.user_email = user.user_email
    if user.user_password:
        user_data.user_password = make_password(user.user_password)
    if user.user_birthday:
        user_data.user_birthday = user.user_birthday
    if image:
        user_data.user_image = image
    user_data.save()
    return {"mensagem": "Usuário atualizado com sucesso!"}

@router.delete("/deletar/{user_id}", response=UserResponse)
def delete_user_by_id(request, user_id: int):
    user_data = User.objects.get(user_id=user_id)
    user_data.delete()
    return {"mensagem": "Usuário deletado com sucesso!"}

