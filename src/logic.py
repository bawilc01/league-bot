def balance_owed(amount_due, amount_paid):
    return max(amount_due - amount_paid, 0)


def assign_players(players, teams, counts):
    """players: [(id, name)], teams: [(team_id, max_size)],
    counts: {team_id: current_count}. Returns (assignments, waitlist)."""
    assignments = []
    waitlist = []
    for player_id, name in players:
        for team_id, max_size in teams:
            if counts[team_id] < max_size:
                assignments.append((player_id, team_id))
                counts[team_id] += 1
                break
        else:
            waitlist.append((player_id, name))
    return assignments, waitlist