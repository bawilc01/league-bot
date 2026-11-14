-- 1. Unpaid balances
SELECT
    p.name,
    p.parent_name,
    p.parent_email,
    pay.amount_due - pay.amount_paid AS balance_owed
FROM players p
JOIN payments pay ON p.id = pay.player_id
WHERE pay.amount_paid < pay.amount_due
ORDER BY balance_owed DESC;

-- 2. Roster count by age group
SELECT age_group, COUNT(*) AS players
FROM players
GROUP BY age_group
ORDER BY age_group asc;

-- 3. Open spots per team
SELECT
    t.name,
    t.age_group,
    t.max_size,
    t.max_size - COUNT(p.id) AS open_spots
FROM teams t
LEFT JOIN players p ON p.team_id = t.id
GROUP BY t.id, t.name, t.age_group, t.max_size
ORDER BY t.age_group, t.name;