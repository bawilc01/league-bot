from logic import assign_players, balance_owed


def test_team_cap_never_exceeded():
    teams = [(1, 2), (2, 2)]
    players = [(i, f"P{i}") for i in range(1, 7)]
    counts = {1: 0, 2: 0}
    assignments, waitlist = assign_players(players, teams, counts)
    assert counts[1] <= 2 and counts[2] <= 2
    assert len(assignments) == 4
    assert len(waitlist) == 2


def test_balance_owed():
    assert balance_owed(150, 75) == 75
    assert balance_owed(150, 150) == 0
    assert balance_owed(150, 0) == 150


def test_empty_data():
    assignments, waitlist = assign_players([], [(1, 12)], {1: 0})
    assert assignments == [] and waitlist == []
    assignments, waitlist = assign_players([(1, "A")], [], {})
    assert assignments == [] and waitlist == [(1, "A")]