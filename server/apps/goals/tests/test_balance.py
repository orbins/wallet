from decimal import Decimal

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ..constants import DefaultTestData
from ..models import Goal
from ...pockets.models.transaction import Transaction
from ...pockets.models.transaction_category import TransactionCategory
from ...users.models.user import User


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
        for i, start_amount in enumerate(DefaultTestData.GOAL_CREATION_DATA_SET):
            with self.subTest(i=i, start_amount=start_amount):
                balance_before = self.client.get(
                    reverse('transactions-get-balance')
                ).data['balance']
                self.client.post(
                    reverse('goals-list'),
                    data={
                        'user': self.user,
                        'name': f'Тестовая цель {i}',
                        'category': self.category.id,
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
                    Decimal(balance_before),
                    Decimal(balance_after) + start_amount
                )

    def test_balance_on_goal_completion(self):
        """
        Проверяет, что при завершении цели, накопленная
        на неё сумма возвращается на счёт.
        """
        for i, target_amount in enumerate(DefaultTestData.TARGET_AMOUNT_DATA_SET):
            with self.subTest(i=i, refill_amount=target_amount):
                self.client.post(
                    reverse('goals-list'),
                    data={
                        'user': self.user,
                        'name': f'Тестовая цель {i}',
                        'category': self.category.id,
                        'start_amount': 0,
                        'target_amount': target_amount,
                        'term': 3,
                        'percent': 5,
                    }
                )
                goal = Goal.objects.get(
                    user=self.user,
                    name__contains=f'Тестовая цель {i}'
                )
                self.client.post(
                    reverse('goals-refill'),
                    data={
                        'goal': goal.id,
                        'amount': target_amount,
                    }
                )
                balance_before = self.client.get(
                    reverse('transactions-get-balance')
                ).data['balance']
                self.client.patch(
                    reverse('goals-complete', args=[goal.id]),
                )
                balance_after = self.client.get(
                    reverse('transactions-get-balance')
                ).data['balance']

                self.assertEqual(
                    Decimal(balance_after),
                    Decimal(balance_before) + target_amount
                )

    def tearDown(self):
        Transaction.objects.filter(user=self.user).delete()
        Goal.objects.filter(user=self.user).delete()
