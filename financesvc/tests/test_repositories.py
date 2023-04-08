from unittest import TestCase

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from financesvc.domain.models import Base
from financesvc.domain.repositories import ExpenseRepository, UserRepository
from financesvc.tests.fixtures import create_mock_expense, create_mock_category, create_mock_user


def create_initial_test_data(engine):
    user = create_mock_user()
    category = create_mock_category()
    expense = create_mock_expense()
    with Session(engine) as session:
        session.add(category)
        session.add(user)
        session.commit()
        session.add(expense)
        session.commit()


class BaseTestCase(TestCase):
    TEST_DATABASE_URL = 'sqlite:///:memory:'

    def setUp(self) -> None:
        engine = create_engine(self.TEST_DATABASE_URL)
        Base.metadata.create_all(self.repo._engine)
        create_initial_test_data(self.repo._engine)


class TestExpenseRepository(BaseTestCase):
    def setUp(self) -> None:
        engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)
        create_initial_test_data(engine)
        self.repo = ExpenseRepository(self.TEST_DATABASE_URL)
        # super(TestExpenseRepository, self).setUp()

        self.user_repo = UserRepository(self.TEST_DATABASE_URL)


    def test_all_expense_from_user(self):
        user = self.user_repo.get_user(user_code='abc123')
        expenses = self.repo.get_expenses(user.code)

        self.assertEqual(1, len(expenses))
