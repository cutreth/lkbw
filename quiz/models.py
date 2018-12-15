from django.db import models


class Category(models.Model):
    category_text = models.CharField(max_length=200)

    def __str__(self):
        return self.category_text

    class Meta:
        verbose_name_plural = 'categories'


class Question(models.Model):
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
    )
    question_text = models.CharField(max_length=200)
    ask_date = models.DateField(blank=True, null=True)
    remove = models.BooleanField()

    def __str__(self):
        return self.question_text
