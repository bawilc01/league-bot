DROP TABLE IF EXISTS payments, players, teams CASCADE;

CREATE TABLE teams (
    id         SERIAL PRIMARY KEY,
    name       TEXT NOT NULL,
    age_group  TEXT NOT NULL CHECK (age_group IN ('U8','U10','U12','U14')),
    max_size   INTEGER NOT NULL DEFAULT 12 CHECK (max_size > 0)
);

CREATE TABLE players (
    id           SERIAL PRIMARY KEY,
    name         TEXT NOT NULL,
    birth_year   INTEGER NOT NULL,
    age_group    TEXT NOT NULL CHECK (age_group IN ('U8','U10','U12','U14')),
    parent_name  TEXT NOT NULL,
    parent_email TEXT NOT NULL,
    team_id      INTEGER REFERENCES teams(id) ON DELETE SET NULL
);

CREATE TABLE payments (
    id          SERIAL PRIMARY KEY,
    player_id   INTEGER NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    amount_due  NUMERIC(10,2) NOT NULL CHECK (amount_due >= 0),
    amount_paid NUMERIC(10,2) NOT NULL DEFAULT 0 CHECK (amount_paid >= 0),
    due_date    DATE NOT NULL
);

CREATE INDEX idx_players_team ON players(team_id);
CREATE INDEX idx_players_age_group ON players(age_group);
CREATE INDEX idx_payments_player ON payments(player_id);
