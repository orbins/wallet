from typing import Final


class TransactionErrors:
    NOT_USERS_CATEGORY: Final[str] = 'У пользователя нет такой категории'
    DOES_NOT_SET_CATEGORY: Final[str] = 'Нельзя задать категорию для транзакций доходного типа'
    CATEGORY_NOT_SPECIFIED: Final[str] = 'Укажите категорию расходов'
    INCORRECT_TRANSACTION_TYPE: Final[str] = 'Некорректный тип транзакции'
    NOT_ENOUGH_BALANCE: Final[str] = 'Недостаточно средств для выполнения операции'


class TransactionCategoryErrors:
    ALREADY_EXISTS: Final[str] = 'У пользователя уже существует категория с таким названием и типом'
