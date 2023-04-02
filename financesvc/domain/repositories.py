from datetime import datetime

from sqlalchemy import create_engine, select, update
from sqlalchemy.orm import Session

from financesvc.domain.models import Expense


class BaseRepository:
    MODEL = None

    def __init__(self, database_url: str):
        self._engine = create_engine(database_url)
        self._session = Session(self._engine)

        if not self.MODEL:
            raise AttributeError('No model is set for repository {}'.format(self.__class__.__name__))

    def create(self, instance):
        with self._session as session:
            session.add(instance)
            session.commit()
            session.refresh(instance)
            return instance.as_dict()

    def create_many(self, instances: list):
        with self._session as session:
            session.add_all(instances)
            session.commit()

    def get_many(self, *args, **kwargs):
        stmt = select(self.MODEL).where(*args, **kwargs)
        return self._session.execute(stmt).all()

    def get_one(self, *args, **kwargs):
        stmt = select(self.MODEL).where(*args, **kwargs)
        return self._session.scalars(stmt).first()

    def update(self, get_instance_query, *args, **kwargs):
        stmt = update(self.MODEL).where(get_instance_query).values(*args, **kwargs)
        with self._session as session:
            session.execute(stmt)


class ExpenseRepository(BaseRepository):
    MODEL = Expense

    def create_expense(
        self,
        title: str,
        amount: float,
        category_id: int,
        description: str = '',
        spent_date: datetime = datetime.now(),
        created_by_id: int = None,
        is_archived: bool = False
    ) -> dict:
        new_expense = Expense(
            title=title,
            amount=amount,
            description=description,
            spent_date=spent_date,
            category_id=category_id,
            created_by_id=created_by_id,
            is_archived=is_archived
        )
        return self.create(new_expense)

    def update_expense(
        self,
        expense_id,
        title: str,
        amount: float,
        spent_date: datetime,
        category_id: int,
        created_by_id: int,
        is_archived: bool = False
    ):
        expense = self.get_one(Expense.id == expense_id)
        if not expense:
            return

        return
