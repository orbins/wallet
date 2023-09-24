import datetime
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
            transaction_date=datetime.date.today()
        )
        self.client.force_authenticate(user=self.user)
        for i, (start_amount, percent, _) in enumerate(DefaultTestData.GOAL_CREATION_DATA_SET):
            self.client.post(
                reverse('goals-list'),
                data={
                    'user': self.user,
                    'name': f'Тестовая цель {i}',
                    'category': self.category.id,
                    'start_amount': start_amount,
                    'target_amount': DefaultTestData.TARGET_AMOUNT_FOR_PERCENTS,
                    'term': 3,
                    'percent': percent,
                }
            )

    def test_calculate_percents(self):
        """
        Проверяет, что на баланс целей
        начислено корректное количество процентов
        """
        calculate_daily_percent()
        for i, (_, _, expected) in enumerate(DefaultTestData.GOAL_CREATION_DATA_SET):
            with self.subTest(i=i, expected=expected):
                goal = Goal.objects.filter(
                    user=self.user,
                    name__exact=f'Тестовая цель {i}',
                ).annotate_with_accumulated_amount().first()
                self.assertEqual(goal.accumulated_amount, expected)

    def test_not_calculate_to_completed(self):
        """
        Проверяет, что на завершенные цели
        не начисляются проценты
        """
        count_before = Transaction.objects.filter(user=self.user).count()
        Goal.objects.update(is_completed=True)
        calculate_daily_percent()
        count_after = Transaction.objects.filter(user=self.user).count()
        self.assertEqual(count_before, count_after)

    def tearDown(self):
        Transaction.objects.filter(user=self.user).delete()
        Goal.objects.filter(user=self.user).delete()