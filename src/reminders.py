import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv

load_dotenv()
conn = psycopg2.connect(os.environ["DATABASE_URL"])
cur = conn.cursor()

# Unpaid balances (your query 1, plus due_date and player id)
cur.execute("""
    SELECT
        p.id,
        p.name,
        p.parent_name,
        p.parent_email,
        pay.amount_due - pay.amount_paid AS balance_owed,
        pay.due_date
    FROM players p
    JOIN payments pay ON p.id = pay.player_id
    WHERE pay.amount_paid < pay.amount_due
    ORDER BY balance_owed DESC;
""")
rows = cur.fetchall()
print(f"Unpaid balances found: {len(rows)}")

# Make sure the outbox folder exists (path is relative to the project root)
outbox = Path(__file__).resolve().parent.parent / "outbox"
outbox.mkdir(exist_ok=True)

for player_id, player_name, parent_name, parent_email, balance, due_date in rows:
    message = (
        f"To: {parent_email}\n"
        f"Subject: Registration payment reminder for {player_name}\n"
        f"\n"
        f"Hi {parent_name},\n"
        f"\n"
        f"Our records show a remaining balance of ${balance:.2f} for "
        f"{player_name}'s registration. Payment is due by "
        f"{due_date.strftime('%B %d, %Y')}.\n"
        f"\n"
        f"If you've already paid, please disregard this message.\n"
        f"\n"
        f"Thank you,\n"
        f"League Registration Team\n"
    )
    (outbox / f"player_{player_id}.txt").write_text(message)

print(f"Wrote {len(rows)} reminder files to {outbox}")

cur.close()
conn.close()