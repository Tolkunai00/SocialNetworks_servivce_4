from datetime import datetime
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from stories_site.database.db import Base

class Stories(Base):
    __tablename__ = "stories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user: Mapped[str] = mapped_column(String, nullable=False, index=True)
    file: Mapped[str] = mapped_column(String, nullable=False)
    created_date: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    likes: Mapped[list["StoriesLike"]] = relationship(back_populates="story_ref", cascade="all, delete-orphan")
    comments: Mapped[list["StoriesComment"]] = relationship(back_populates="story_ref", cascade="all, delete-orphan")

class StoriesLike(Base):
    __tablename__ = "stories_like"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user: Mapped[str] = mapped_column(String, nullable=False, index=True)
    story: Mapped[int] = mapped_column(ForeignKey("stories.id"), nullable=False)
    like: Mapped[bool] = mapped_column(default=True)

    story_ref: Mapped["Stories"] = relationship(back_populates="likes")

class StoriesComment(Base):
    __tablename__ = "stories_comment"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user: Mapped[str] = mapped_column(String, nullable=False, index=True)
    story: Mapped[int] = mapped_column(ForeignKey("stories.id"), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)

    story_ref: Mapped["Stories"] = relationship(back_populates="comments")