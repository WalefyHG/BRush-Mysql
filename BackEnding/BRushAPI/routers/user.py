from ninja import Router, UploadedFile, File
from typing import List, Optional
from ..schema import UserIn, UserLogin, UserOut, UserPut, UserResponse
from ..models import User
from django.contrib.auth.hashers import check_password, make_password
from django.core.files.base import ContentFile
from rest_framework_simplejwt.tokens import AccessToken

router = Router()


@router.get("/todos", response=List[UserOut])
def list_users(request):
    return User.objects.all()

@router.post("/criando", response=UserResponse, auth=None)
def create_user(request, user: UserIn, image: UploadedFile = File(...)):
    image_data = image.read()
    password_hash = make_password(user.user_password)
    user_data = User.objects.create(
        user_name=user.user_name,
        user_email=user.user_email,
        user_password=password_hash,
        user_image= ContentFile(image_data, name=image.name)
    )
    user_data.save()
    return {"mensagem": "Usuário criado com sucesso!"}

@router.post("/login", auth=None)
def login(request, user: UserLogin):
    try:
        user_data = User.objects.get(user_name=user.user_name)
        if check_password(user.user_password, user_data.user_password):
            response = {"mensagem": "Usuário logado com sucesso!"}
            token = AccessToken.for_user(user_data)
            return {"response": response, "token": str(token)}
    except User.DoesNotExist:
        pass
    return {"mensagem": "Usuário ou senha inválidos!"}

@router.get("/pesquisar/{user_id}", response=UserOut)
def get_user_by_id(request, user_id: int):
    user_data = User.objects.get(user_id=user_id)
    return user_data

@router.put("/atualizar/{user_id}", response=UserResponse)
def update_by_id(request, user_id: int, user: UserPut, image: Optional[UploadedFile] = File(None)):
    user_data = User.objects.get(user_id=user_id)
    if image is not None:
        image_data = image.read()
    else:
        image_data = None
    if user.user_name:
        user_data.user_name = user.user_name
    if user.user_email:
        user_data.user_email = user.user_email
    if user.user_password:
        user_data.user_password = make_password(user.user_password)
    if image_data:
        user_data.user_image = ContentFile(image_data, name=image.name)
    user_data.save()
    return {"mensagem": "Usuário atualizado com sucesso!"}

@router.delete("/deletar/{user_id}", response=UserResponse)
def delete_user_by_id(request, user_id: int):
    user_data = User.objects.get(user_id=user_id)
    user_data.delete()
    return {"mensagem": "Usuário deletado com sucesso!"}