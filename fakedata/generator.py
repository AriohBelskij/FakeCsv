from django.conf import settings
from faker import Faker
import csv

from fakedata.models import DataSet, FakeSchema, Column


def generate_fake_data(date_type: int, amount=(0, 100)):
    fake = Faker()
    data = {
        "Full_name": fake.name(),
        "Job": fake.job(),
        "Email": fake.email(),
        "Domain": fake.email().split("@")[-1],
        "Phone": fake.phone_number(),
        "Company": fake.company(),
        "Text": fake.sentences(
            nb=fake.random_int(min=amount[0], max=amount[1])
        ),
        "Integer": fake.random_int(*amount),
        "Address": fake.address(),
        "Date": fake.date(),
    }
    return data[date_type]


def generate_csv(dataset: DataSet):
    schema = FakeSchema.objects.get(id=dataset.schema.id)
    columns = Column.objects.filter(schema=schema).order_by("order").values()

    quote = schema.quote
    separator = schema.separator
    print(quote)

    csv.register_dialect(
        "new_dialect",
        delimiter=separator,
        quotechar=quote[0],
        quoting=csv.QUOTE_ALL,
    )

    fieldnames = [column["column_name"] for column in columns]

    with open(
        settings.MEDIA_ROOT
        + f"/schema_{schema.title}_dataset{dataset.id}.csv",
        "w",
    ) as file:
        writer = csv.DictWriter(
            file, fieldnames=fieldnames, dialect="new_dialect"
        )
        writer.writeheader()
        for i in range(dataset.rows):
            row = {}
            for column in columns:
                value = generate_fake_data(column["data_type"])
                row[column["column_name"]] = value

            writer.writerow(row)
        dataset.status = 1
        dataset.download_link = f"{settings.MEDIA_URL}schema_{schema.title}_dataset{dataset.id}.csv"
        dataset.save()
