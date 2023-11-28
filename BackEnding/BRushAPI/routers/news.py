from typing import List
from ninja import Router
from ..models import Notices
from ..schema import NoticeIn, NoticeOut, UserResponse

router = Router()

@router.get("/allnotices", response=List[NoticeOut])
def get_notices(request):
    notices = Notices.objects.all()
    return notices

@router.post("/notices", response=NoticeOut)
def create_notices(request, notice: NoticeIn):
    user = request.auth
    notices = Notices.objects.create(
        notice_title=notice.notice_title,
        notice_content=notice.notice_content,
        notice_date=notice.notice_date,
        notice_writer=user
    )
    notices.save()
    return notices

@router.delete("deletando/{id}", response=UserResponse)
def delete_notice_by_id(request, id: int):
    notice = Notices.objects.get(notice_id=id)
    notice.delete()
    return {"mensagem": "Noticia deletada com sucesso!"}

@router.put("update/{id}", response=NoticeOut)
def update_notice_by_id(request, id: int, notice: NoticeIn):
    existing_notice = Notices.objects.get(notice_id=id)
    existing_notice.notice_title = notice.notice_title
    existing_notice.notice_content = notice.notice_content
    existing_notice.notice_date = notice.notice_date
    existing_notice.save()
    return existing_notice