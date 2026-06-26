from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.database import get_session
from app.dependencies import get_current_user
from app.models import Tag, TaskTag, User
from app.schemas import TagCreate, TagRead, TagUpdate

router = APIRouter(prefix="/tags", tags=["tags"])


@router.post("", response_model=TagRead, status_code=status.HTTP_201_CREATED)
def create_tag(
    data: TagCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    tag = Tag(**data.model_dump(), owner_id=current_user.id)
    session.add(tag)
    session.commit()
    session.refresh(tag)
    return tag


@router.get("", response_model=list[TagRead])
def get_tags(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return session.exec(select(Tag).where(Tag.owner_id == current_user.id)).all()


@router.get("/{tag_id}", response_model=TagRead)
def get_tag(
    tag_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    tag = session.get(Tag, tag_id)
    if tag is None or tag.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


@router.put("/{tag_id}", response_model=TagRead)
def update_tag(
    tag_id: int,
    data: TagUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    tag = session.get(Tag, tag_id)
    if tag is None or tag.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Tag not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(tag, key, value)

    session.add(tag)
    session.commit()
    session.refresh(tag)
    return tag


@router.delete("/{tag_id}")
def delete_tag(
    tag_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    tag = session.get(Tag, tag_id)
    if tag is None or tag.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Tag not found")

    links = session.exec(select(TaskTag).where(TaskTag.tag_id == tag.id)).all()
    for link in links:
        session.delete(link)

    session.delete(tag)
    session.commit()
    return {"message": "Tag deleted"}
