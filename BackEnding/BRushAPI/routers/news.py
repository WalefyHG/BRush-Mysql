from typing import List, Optional
from ninja import Router, UploadedFile, File
from ..models import Notices
from ..schema import NoticeIn, NoticeOut, UserResponse
from ninja.errors import HttpError

router = Router()

@router.get("/allnotices", response=List[NoticeOut])
def get_notices(request):
    notices = Notices.objects.all()
    return notices

@router.post("/notices", response=NoticeOut)
def create_notices(request, notice: NoticeIn, image: Optional[UploadedFile] = File(None)):
    user = request.auth
    notices = Notices.objects.create(
        notice_title=notice.notice_title,
        notice_content=notice.notice_content,
        notice_date=notice.notice_date,
        notice_image= image,
        notice_writer=user
    )
    notices.save()
    return notices

@router.delete("deletando/{id}", response=UserResponse)
def delete_notice_by_id(request, id: int):
    try:
        user = request.auth
        notice_data = Notices.objects.get(notice_id=id)
        if user.user_name == notice_data.notice_writer.user_name:
            notice_data.delete()
            return {"mensagem": "Noticia deletada com sucesso!"}
        else:
            raise HttpError(401, "Você não tem permissão para isso")
    except Notices.DoesNotExist:
        raise HttpError(404, "Noticia não encontrada")
    

@router.put("update/{id}", response=NoticeOut)
def update_notice_by_id(request, id: int, notice: NoticeIn, image: Optional[UploadedFile] = File(None)):
    user = request.auth
    existing_notice = Notices.objects.get(notice_id=id)
    if user.user_name == existing_notice.notice_writer.user_name:
        existing_notice.notice_title = notice.notice_title
        existing_notice.notice_content = notice.notice_content
        existing_notice.notice_date = notice.notice_date
        if image is not None:
            existing_notice.notice_image = image
        existing_notice.save()
        return existing_notice
    else:
        raise HttpError(404, "Você não tem permissão para isso")