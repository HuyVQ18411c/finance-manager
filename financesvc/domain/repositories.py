from datetime import datetime

from sqlalchemy import create_engine, select, update
from sqlalchemy.orm import Session, joinedload

from financesvc.domain.models import Expense, Category, User
from financesvc.utils.code_generator import generate_user_code, hash_password


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
            return instance

    def create_many(self, instances: list):
        with self._session as session:
            session.add_all(instances)
            session.commit()

    def get_many(self, stmt=None, *args, **kwargs):
        if stmt is None:
            stmt = select(self.MODEL).where(*args, **kwargs)

        rows = self._session.scalars(stmt).all()

        return rows

    def get_one(self, *args, **kwargs):
        stmt = select(self.MODEL).where(*args, **kwargs)
        return self._session.scalars(stmt).first()

    def update(self, get_instance_query, *args, **kwargs):
        stmt = update(self.MODEL).where(get_instance_query).values(*args, **kwargs)
        with self._session as session:
            session.execute(stmt)


class ExpenseRepository(BaseRepository):
    MODEL = Expense

    def get_expenses(self, user_code: str) -> list[Expense]:
        stmt = select(Expense).join(
            Expense.category
        ).join(
            Expense.created_by
        ).where(
            User.code == user_code
        ).options(joinedload(Expense.category)).order_by(Expense.spent_date)

        expenses = self.get_many(stmt)

        return expenses

    def get_expense_by_id(self, expense_id: int, user_code: str):
        pass

    def create_expense(
        self,
        title: str,
        amount: float,
        category_id: int,
        description: str = '',
        spent_date: datetime = datetime.now().strftime('%Y-%m-%d'),
        created_by_id: int = None,
    ) -> dict:
        spent_date = spent_date.strftime('%Y-%m-%d')
        new_expense = Expense(
            title=title,
            amount=amount,
            description=description,
            spent_date=spent_date,
            category_id=category_id,
            created_by_id=created_by_id,
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

    def delete_expense(self, expense_id):
        pass


class CategoryRepository(BaseRepository):
    MODEL = Category

    def get_categories(self):
        return self.get_many()


class UserRepository(BaseRepository):
    MODEL = User

    def get_user(self, user_code: str = '', email: str = '') -> User:
        if user_code:
            return self.get_one(User.code == user_code)

        if email:
            return self.get_one(User.email == email)

    def create_user(self, email: str = '', password: str = '') -> User:
        while True:
            code = generate_user_code()
            if not self.get_user(code):
                break

        new_user = User(
            code=code,
            email=email,
            password=hash_password(password).decode('utf-8')
        )

        return self.create(new_user)
