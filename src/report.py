import os
from datetime import datetime
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()
engine = create_engine(os.environ["DATABASE_URL"])

summary = pd.read_sql("""
    SELECT
        COUNT(*)                            AS registrations,
        SUM(pay.amount_due)::float          AS total_due,
        SUM(pay.amount_paid)::float         AS total_collected,
        (SUM(pay.amount_due) - SUM(pay.amount_paid))::float AS total_outstanding,
        COUNT(*) FILTER (WHERE pay.amount_paid < pay.amount_due) AS unpaid_players
    FROM players p
    JOIN payments pay ON p.id = pay.player_id;
""", engine)

by_age_group = pd.read_sql("""
    SELECT age_group,
           COUNT(*) AS players,
           COUNT(team_id) AS placed,
           COUNT(*) - COUNT(team_id) AS waitlisted
    FROM players
    GROUP BY age_group
    ORDER BY age_group;
""", engine)

open_spots = pd.read_sql("""
    SELECT t.name AS team, t.age_group, t.max_size,
           t.max_size - COUNT(p.id) AS open_spots
    FROM teams t
    LEFT JOIN players p ON p.team_id = t.id
    GROUP BY t.id, t.name, t.age_group, t.max_size
    ORDER BY t.age_group, t.name;
""", engine)

html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>League Weekly Report</title>
<style>
  body {{ font-family: sans-serif; max-width: 800px; margin: 2rem auto; }}
  table {{ border-collapse: collapse; margin-bottom: 2rem; }}
  th, td {{ border: 1px solid #ccc; padding: 6px 12px; text-align: right; }}
  th {{ background: #f0f0f0; }}
</style></head><body>
<h1>League Weekly Report</h1>
<p>Generated {datetime.now():%B %d, %Y %I:%M %p}</p>
<h2>Registration and payments</h2>
{summary.to_html(index=False)}
<h2>Players by age group</h2>
{by_age_group.to_html(index=False)}
<h2>Open spots by team</h2>
{open_spots.to_html(index=False)}
</body></html>"""

out = Path(__file__).resolve().parent.parent / "report.html"
out.write_text(html)
print(f"Wrote {out}")