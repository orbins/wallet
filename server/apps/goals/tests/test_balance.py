from decimal import Decimal

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ..constants import DefaultTestData
from ..models import Goal
from ...pockets.models.transaction import Transaction
from ...pockets.models.transaction_category import TransactionCategory
from ...users.models.user import User


start_amount = 10000


class TestBalanceChange(APITestCase):

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

    def test_balance_on_goal_creation(self):
        """
        Проверяет, что при создании цели со счета списывается сумма,
        указанная в запросе при создании цели.
        """
        initial_balance = self.client.get(
            reverse('transactions-get-balance')
        ).data['balance']
        response = self.client.post(
            reverse('goals-list'),
            data={
                'user': self.user,
                'name': 'Тестовая цель',
                'category': 1,
                'start_amount': start_amount,
                'target_amount': 50000,
                'term': 3,
                'percent': 5,
            }
        )
        balance_after = self.client.get(
            reverse('transactions-get-balance')
        ).data['balance']
        self.assertEqual(
            Decimal(balance_after),
            Decimal(initial_balance) - start_amount
        )

    def tearDown(self):
        Transaction.objects.filter(user=self.user).delete()
        Goal.objects.filter(user=self.user).delete()
