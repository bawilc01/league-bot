import os
import psycopg2
from dotenv import load_dotenv
import random
from faker import Faker
from pathlib import Path
from datetime import date

amount_due = 150
due_date = date(2026, 12, 1)

#load psql environment
load_dotenv()
conn = psycopg2.connect(os.environ["DATABASE_URL"])
cur = conn.cursor()

schema_path = Path(__file__).resolve().parent.parent / "sql" / "schema.sql"
with open(schema_path) as f:
    cur.execute(f.read())

# create Faker object
fake = Faker()

age_groups = ["U8", "U10", "U12", "U14"]

for age_group in age_groups:
    for letter in ["A", "B", "C"]:
        name = f"{age_group} Team {letter}"
        cur.execute(
            "INSERT INTO teams (name, age_group, max_size) VALUES (%s, %s, %s)",
            (name, age_group, 12),
        )

conn.commit()

birth_years = {
    "U8": (2019, 2020),
    "U10": (2017, 2018),
    "U12": (2015, 2016),
    "U14": (2013, 2014),
}

for i in range(150):
    age_group = random.choice(age_groups)
    low, high = birth_years[age_group]
    birth_year = random.randint(low, high)
    name = fake.name()
    parent_name = fake.name()
    parent_email = fake.email()
    amount_paid = random.choice([150, 150, 150, 150, 150, 75, 0])

    cur.execute(
        "INSERT INTO players (name, birth_year, age_group, parent_name, parent_email) VALUES (%s, %s, %s, %s, %s) RETURNING id",
        (name, birth_year, age_group, parent_name, parent_email),
    )
    player_id = cur.fetchone()[0]

    cur.execute(
        "INSERT INTO payments (player_id, amount_due, amount_paid, due_date) VALUES (%s, %s, %s, %s)",
        (player_id, amount_due, amount_paid, due_date),
    )

conn.commit()
conn.commit()

cur.execute("SELECT COUNT(*) FROM players;")
print(cur.fetchone())

cur.close()
conn.close()