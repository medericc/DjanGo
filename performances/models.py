from django.db import models

class Match(models.Model):
    date = models.DateField()
    opponent = models.CharField(max_length=100)
    points = models.PositiveIntegerField()
    assists = models.PositiveIntegerField()
    rebounds = models.PositiveIntegerField()
    steals = models.PositiveIntegerField()
    blocks = models.PositiveIntegerField()
    turnovers = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.date} vs {self.opponent}"

class Season(models.Model):
    year = models.CharField(max_length=9)  # ex : "2023-2024"
    matches = models.ManyToManyField(Match)

    def __str__(self):
        return self.year

class Highlight(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    media = models.FileField(upload_to='highlights/')
    match = models.ForeignKey(Match, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title
