import os
import psycopg2
from dotenv import load_dotenv
from logic import assign_players


load_dotenv()
conn = psycopg2.connect(os.environ["DATABASE_URL"])
cur = conn.cursor()

age_groups = ["U8", "U10", "U12", "U14"]
waitlist = []

for age_group in age_groups:
    cur.execute(
        "SELECT id, max_size FROM teams WHERE age_group = %s ORDER BY id",
        (age_group,),
    )
    teams = cur.fetchall()   # list of (id, max_size) tuples

    cur.execute(
        "SELECT id, name FROM players WHERE age_group = %s AND team_id IS NULL ORDER BY id",
        (age_group,),
    )
    players = cur.fetchall()   # list of (id, name) tuples

    # Track how many players each team has, e.g. a dict
    counts = {}
    for team_id, max_size in teams:
        cur.execute("SELECT COUNT(*) FROM players WHERE team_id = %s", (team_id,))
        counts[team_id] = cur.fetchone()[0]

    for player_id, player_name in players:
        placed = False
        for team_id, max_size in teams:
            if counts[team_id] < max_size:
                cur.execute(
                    "UPDATE players SET team_id = %s WHERE id = %s",
                    (team_id, player_id),
                )
                counts[team_id] += 1
                placed = True
                break
        if not placed:
            waitlist.append((player_name, age_group))

assignments, overflow = assign_players(players, teams, counts)
for player_id, team_id in assignments:
    cur.execute("UPDATE players SET team_id = %s WHERE id = %s", (team_id, player_id))
for player_id, name in overflow:
    waitlist.append((name, age_group))
conn.commit()

print(f"Waitlist: {len(waitlist)} players")
for name, age_group in waitlist:
    print(age_group, name)

cur.close()
conn.close()