from django.contrib.auth import get_user_model
from django.db import models
from tizer.utils import get_cost
from django.db import IntegrityError, transaction

User = get_user_model()


class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cost = models.IntegerField(default=0)

    @classmethod
    def get_user(cls, user: User) -> "Wallet":
        wal, _ = Wallet.objects.get_or_create(user=user)
        return wal

    def refill(self, cost=get_cost()):
        self.cost += cost


class Tizer(models.Model):
    class Status(models.IntegerChoices):
        WAIT = 0
        PAY = 1
        FAlL = 2

    title = models.CharField(max_length=64)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    status = models.IntegerField(choices=Status.choices, default=Status.WAIT)
    created = models.DateTimeField(auto_now=True)


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    tizer: Tizer = models.ForeignKey(Tizer, on_delete=models.PROTECT)
    cost = models.SmallIntegerField(default=get_cost())
    created = models.DateTimeField(auto_now=True)
