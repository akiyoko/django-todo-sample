from django.db import models


class Todo(models.Model):
    """TODOモデル"""

    class Meta:
        db_table = 'todo'
        verbose_name = verbose_name_plural = 'TODO'

    title = models.CharField(verbose_name='タイトル', max_length=255)
    expiration_date = models.DateField(verbose_name='期限日', null=True, blank=True)

    def __str__(self):
        return self.title
