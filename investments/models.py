from django.db import models
from users.models import CustomUser
from initiatives.models import Initiative

# Create your models here.

class Investment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    initiative = models.ForeignKey(Initiative, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date_invested = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} invested ${self.amount} in {self.initiative.title}"