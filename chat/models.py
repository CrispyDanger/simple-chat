from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Thread(BaseModel):
    participants = models.ManyToManyField(User, verbose_name=("participants"))

    def add_participant(self, participant):
        if self.participants.count() >= 2:
            raise Exception("Too many participants")
        else:
            self.participants.add(participant)

    def __str__(self) -> str:
        users = list(self.participants.all().values_list("username", flat=True))
        return f"{users[0]} and {users[1]} Chat"


class Message(BaseModel):
    sender = models.OneToOneField(
        User, verbose_name=("sender"), on_delete=models.CASCADE
    )
    text = models.TextField(("text"), null=False, max_length=50)
    thread = models.OneToOneField(
        Thread, verbose_name=("thread"), on_delete=models.CASCADE
    )
    is_read = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.sender} message in "{self.thread}"'


# Create your models here.
