from sqlalchemy.orm import Session

from app.models import Link
from app.utils import generate_short_code


def create_short_link(db: Session, original_url: str) -> Link:
    short_code = generate_short_code()
    while db.query(Link).filter(Link.short_code == short_code).first():
        short_code = generate_short_code()

    link = Link(original_url=original_url, short_code=short_code)
    db.add(link)
    db.commit()
    db.refresh(link)
    return link


def get_link_by_code(db: Session, short_code: str) -> Link | None:
    return db.query(Link).filter(Link.short_code == short_code).first()


def increment_click_count(db: Session, link: Link) -> Link:
    link.click_count += 1
    db.commit()
    db.refresh(link)
    return link
