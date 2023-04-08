from datetime import datetime

from financesvc.domain.models import Expense, Category, User


def create_mock_expense(
    title='test expense',
    amount='20000',
    category_id=1,
    created_by_id=1,
    **kwargs
):
    return Expense(
        title=title,
        amount=amount,
        category_id=category_id,
        spent_date=datetime.now(),
        created_by_id=created_by_id
    )


def create_mock_category(
    name='test category',
    abbr_name='test abbr name'
):
    return Category(
        name=name,
        abbr_name=abbr_name
    )


def create_mock_user(code='abc123', email=None, password=None):
    return User(
        code=code,
        email=email,
        password=password,
    )
