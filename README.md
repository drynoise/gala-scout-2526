# Gala Scout 25/26

A data-driven scouting pipeline built to identify transfer targets for Galatasaray using FBref player statistics from the 2025/26 season.

## What It Does

- Filters 2,800+ outfield players across the top 5 European leagues
- Removes goalkeepers and players with under 500 minutes played
- Excludes elite clubs unreachable for Galatasaray
- Scores players by position using weighted per-90 metrics
- Generates radar charts for shortlisted targets
- Finds statistically similar players using Euclidean distance

## Project Structure

    gala-scout-2526/
    data/
        players_data-2025_2026.csv   Raw FBref data (2,839 players)
        scouting_report.csv          Top 40 targets by position
        *_radar.png                  Radar charts per player
    scouting_pipeline.ipynb          Full pipeline notebook
    README.md

## Positions and Metrics

| Position | Key Metrics |
|---|---|
| Forward | Gls/90, Ast/90, SoT/90, G/Sh, G/SoT |
| Midfielder | G+A/90, TklW/90, Int/90, Ast/90 |
| Defender | TklW/90, Int/90, Fld/90, Crs/90, Discipline |
| Att Mid / Wing | Gls/90, Ast/90, G+A/90, SoT/90 |

## Scouting Filters

- Max age: 28
- Min minutes: 900
- Excluded clubs: Real Madrid, Barcelona, Manchester City, Bayern Munich, PSG, Liverpool, Arsenal, Chelsea, Manchester Utd, Inter, Juventus, Atletico Madrid

## Top Targets 25/26

**Forwards:** Donyell Malen, Jonathan Burkardt, Nikola Krstovic

**Midfielders:** Lamine Camara, Sergi Altimira, Mamadou Sangare

**Defenders:** Kassoum Ouattara, Alidu Seidu, Nnamdi Collins

**Att Mid / Wings:** Endrick, Karim Adeyemi, Ansu Fati

## Similarity Model

Given a target player, the model finds the most statistically similar players in the filtered pool using Euclidean distance on StandardScaler-normalized per-90 metrics. Useful for finding cheaper alternatives with the same playing profile.

## Data Source

FBref — 2025/26 season stats across Premier League, La Liga, Bundesliga, Serie A, Ligue 1.

## Stack

Python, pandas, scikit-learn, matplotlib
