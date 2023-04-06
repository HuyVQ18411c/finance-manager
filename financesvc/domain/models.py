from datetime import datetime, timezone

import bcrypt
from sqlalchemy import Integer, DateTime, String, ForeignKey, Text, Float, Date
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship

from financesvc.utils.code_generator import hash_password


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    def as_dict(self):
        return {
            c.name: getattr(self, c.name)
            if not isinstance(getattr(self, c.name), datetime)
            else str(getattr(self, c.name))
            for c in self.__table__.columns
        }


class BaseModel(Base):
    __abstract__ = True

    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(tz=timezone.utc))


class User(BaseModel):
    __tablename__ = 'users'

    code: Mapped[str] = mapped_column(String(10), nullable=True)

    email: Mapped[str] = mapped_column(String(100), nullable=True)

    password: Mapped[str] = mapped_column(Text, nullable=True)

    expenses: Mapped[list['Expense']] = relationship(back_populates='created_by')

    def validate_password(self, password: str):
        return bcrypt.checkpw(password.encode('utf-8'), bytes(self.password, 'utf-8'))


class Category(Base):
    __tablename__ = 'categories'

    name: Mapped[str] = mapped_column(String(150), nullable=False)

    abbr_name: Mapped[str] = mapped_column(String(10), nullable=False)

    expenses: Mapped[list['Expense']] = relationship(back_populates='category')


class Expense(BaseModel):
    __tablename__ = 'expenses'

    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)

    amount: Mapped[float] = mapped_column(Float, nullable=False)

    spent_date: Mapped[datetime] = mapped_column(Date)

    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    category: Mapped[Category] = relationship(back_populates='expenses')

    created_by_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=True)
    created_by: Mapped[User] = relationship(back_populates='expenses')

    last_updated_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        onupdate=datetime.now(tz=timezone.utc),
        nullable=True
    )
