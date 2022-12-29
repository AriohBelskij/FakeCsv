from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class FakeSchema(models.Model):
    SEPARATORS = [
        (",", "Comma(,)"),
        (";", "Semilicon(;)"),
        ("\t", "Tab(\t)"),
        (" ", "Space( )"),
        ("|", "Pipe(|)"),
    ]
    QUOTES = [
        ("'", "Single-quote('')"),
        ('"', 'Double-quote("")'),
    ]
    title = models.CharField(
        max_length=60, blank=True, null=True, default="Untitled"
    )
    separator = models.TextField(choices=SEPARATORS, max_length=1, default=",")
    quote = models.TextField(choices=QUOTES, default='""', max_length=1)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="schemas"
    )

    def __str__(self):
        return f"{self.title} was created!"

    def get_absolute_url(self):
        return reverse("fakedata:schema-detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["-created"]


class Column(models.Model):
    TYPES = [
        ("Full_name", "Full name (a combination of first name and last name)"),
        ("Job", "Job"),
        ("Email", "Email"),
        ("Domain", "Domain name"),
        ("Phone", "Phone number"),
        ("Company", "Company name"),
        ("Text", "Text (with a specified range for a number of sentences)"),
        ("Integer", "Integer (with specified range)"),
        ("Address", "Address"),
        ("Date", "Date"),
    ]

    column_name = models.CharField(max_length=25)
    data_type = models.CharField(max_length=25, choices=TYPES)
    order = models.PositiveIntegerField(default=0)
    schema = models.ForeignKey(
        FakeSchema, on_delete=models.CASCADE, related_name="column"
    )

    class Meta:
        ordering = ["order"]

    def clean(self):
        super(Column, self).clean()
        if not self.order:
            self.order = Column.objects.filter(schema=self.schema).count() + 1


class DataSet(models.Model):
    STATUSES = [(0, "Processing.."), (1, "Ready!")]
    schema = models.ForeignKey(
        FakeSchema, on_delete=models.CASCADE, related_name="schema_ds"
    )
    created = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUSES, default=0)
    rows = models.PositiveIntegerField(null=True)
    download_link = models.URLField()

    class Meta:
        ordering = [
            "-created",
        ]
