from io import BytesIO

from openpyxl import Workbook


class TransactionFileHandler:
    def __init__(self, transactions=None):
        """
        :param transactions: queryset модели Transaction
        """
        self.transactions = transactions
        self.wb = Workbook()
        self.ws = self.wb.active

    def save_data_to_worksheet(self):
        self.ws.append(
            ['Дата операции', 'Тип операции', 'Категория', 'Сумма']
        )
        for transaction in self.transactions:
            self.ws.append([
                transaction.transaction_date,
                'Доход' if transaction.transaction_type == 'income' else 'Расход',
                transaction.category.name if transaction.category else None,
                transaction.amount
            ])

    def save_file(self):
        file = BytesIO()
        self.wb.save(file)
        file.seek(0)

        return file

    def export_transactions_to_excel(self):
        self.save_data_to_worksheet()
        file = self.save_file()

        return file
