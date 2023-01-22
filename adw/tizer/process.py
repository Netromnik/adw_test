from tizer.models import Wallet, Tizer, Transaction
from django.db import transaction as m_transaction


class Process(object):
    def failt(self):
        transaction = Transaction(
            user=self.admin,
            tizer=self.tizer,
        )
        self.tizer.status = self.status
        try:
            with m_transaction.atomic():
                transaction.save()
                self.tizer.save()
        except:
            return False
        return True

    def pay(self):
        walet = Wallet.get_user(self.tizer.author)
        transaction = Transaction(
            user=self.admin,
            tizer=self.tizer,
        )
        self.tizer.status = self.status
        walet.refill()
        try:
            with m_transaction.atomic():
                transaction.save()
                walet.save()
                self.tizer.save()
        except:
            return False
        return True

    def wait(self):
        return True

    def __init__(self, tizer: Tizer, status: Tizer.Status, admin) -> None:
        self.tizer = tizer
        self.status = status
        self.admin = admin

        self.call = {
            Tizer.Status.WAIT: self.wait,
            Tizer.Status.PAY: self.pay,
            Tizer.Status.FAlL: self.failt,
        }

    def run(self) -> bool:
        if self.tizer.status != Tizer.Status.WAIT:
            return False

        try:
            return self.call[self.status]()
        except KeyError:
            return False
