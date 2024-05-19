-- Cockroach SQL dialect
-- Create Schema for the application then create the tables

CREATE SCHEMA IF NOT EXISTS mlb;
CREATE SCHEMA IF NOT EXISTS nfl;
CREATE SCHEMA IF NOT EXISTS nba;
CREATE SCHEMA IF NOT EXISTS nhl;
CREATE SCHEMA IF NOT EXISTS ncaaf;
CREATE SCHEMA IF NOT EXISTS ncaab;
CREATE SCHEMA IF NOT EXISTS soccer;
CREATE SCHEMA IF NOT EXISTS tennis;
CREATE SCHEMA IF NOT EXISTS golf;
CREATE SCHEMA IF NOT EXISTS mma;
CREATE SCHEMA IF NOT EXISTS boxing;
CREATE SCHEMA IF NOT EXISTS nascar;
CREATE SCHEMA IF NOT EXISTS esports;
CREATE SCHEMA IF NOT EXISTS olympics;
CREATE SCHEMA IF NOT EXISTS rugby;
CREATE SCHEMA IF NOT EXISTS cricket;
CREATE SCHEMA IF NOT EXISTS wnba;
CREATE SCHEMA IF NOT EXISTS cfl;
CREATE SCHEMA IF NOT EXISTS aaf;
CREATE SCHEMA IF NOT EXISTS xfl;
CREATE SCHEMA IF NOT EXISTS afl;




CREATE TABLE IF NOT EXISTS mlb.teams (
    team_id SERIAL PRIMARY KEY,
    team_name VARCHAR(50) NOT NULL,
    team_city VARCHAR(50) NOT NULL,
    team_state VARCHAR(50) NOT NULL,
    team_stadium VARCHAR(50) NOT NULL,
    team_manager VARCHAR(50) NOT NULL,
    team_owner VARCHAR(50) NOT NULL,
    team_championships INT NOT NULL,
    team_logo VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS mlb.players (
    player_id SERIAL PRIMARY KEY,
    player_name VARCHAR(50) NOT NULL,
    player_position VARCHAR(50) NOT NULL,
    player_team VARCHAR(50) NOT NULL,
    player_number INT NOT NULL,
    player_batting_avg DECIMAL(3, 3) NOT NULL,
    player_home_runs INT NOT NULL,
    player_rbi INT NOT NULL,
    player_era DECIMAL(3, 3) NOT NULL,
    player_strikeouts INT NOT NULL,
    player_wins INT NOT NULL,
    player_saves INT NOT NULL,
    player_logo VARCHAR(50) NOT NULL
);



CREATE TABLE IF NOT EXISTS mlb.player_base_stats (COMMENT = 'Base Stats for MLB Players',
    player_id INT PRIMARY KEY,
    player_name VARCHAR(50) NOT NULL,
    player_position VARCHAR(50) NOT NULL,
    player_team VARCHAR(50) NOT NULL,
    player_number INT NOT NULL,
    player_batting_avg DECIMAL(3, 3) NOT NULL,
    player_home_runs INT NOT NULL,
    player_rbi INT NOT NULL,
    player_era DECIMAL(3, 3) NOT NULL,
    player_strikeouts INT NOT NULL,
    player_wins INT NOT NULL,
    player_saves INT NOT NULL,
    player_logo VARCHAR(50) NOT NULL
);

