from django.db import models
import uuid
# Create your models here.


class Todo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=70)
    description = models.TextField(max_length=250)
    done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        'user.User', on_delete=models.CASCADE, related_name='todos')

    def __str__(self):
        return self.title
