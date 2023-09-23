from decimal import Decimal

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ..constants import DefaultTestData
from ..models import Goal
from ...pockets.models.transaction import Transaction
from ...pockets.models.transaction_category import TransactionCategory
from ..tasks import calculate_daily_percent
from ...users.models.user import User


class TestPercents(APITestCase):

    @staticmethod
    def create_user(
        email: str = DefaultTestData.USER_DATA['email'],
        username: str = DefaultTestData.USER_DATA['username'],
        password: str = DefaultTestData.USER_DATA['password']
    ) -> User:
        user = User.objects.create(
            email=email,
            username=username,
        )
        user.set_password(password)
        return user

    @classmethod
    def setUpTestData(cls):
        cls.user = cls.create_user()
        cls.category = TransactionCategory.objects.create(
            user=cls.user,
            name='Тестовая категория'
        )

    def setUp(self):
        Transaction.objects.create(
            user=self.user,
            amount=DefaultTestData.INITIAL_BALANCE,
            transaction_type='income',
            transaction_date='2023-08-08'
        )
        self.client.force_authenticate(user=self.user)

    def test_calculate_percents(self):
        """
        Проверяет, что на баланс целей
        начислено корректное количество процентов
        """
        for i, (start_amount, target_amount, percent, expected) in enumerate(DefaultTestData.GOAL_CREATION_DATA_SET):
            with self.subTest(
                    i=i,
                    start_amount=start_amount,
                    target_amount=target_amount,
                    percent=percent,
                    expected=expected
            ):
                self.client.post(
                    reverse('goals-list'),
                    data={
                        'user': self.user,
                        'name': f'Тестовая цель {i}',
                        'category': self.category.id,
                        'start_amount': start_amount,
                        'target_amount': target_amount,
                        'term': 3,
                        'percent': percent,
                    }
                )
                calculate_daily_percent()
                goal = Goal.objects.filter(
                    user=self.user,
                    name__exact=f'Тестовая цель {i}',
                ).annotate_with_accumulated_amount().first()
                self.assertEqual(
                    goal.accumulated_amount,
                    expected
                )

    def tearDown(self):
        Transaction.objects.filter(user=self.user).delete()
        Goal.objects.filter(user=self.user).delete()