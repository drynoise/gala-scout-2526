# Gala Scout 25/26

A data-driven football scouting pipeline built to identify realistic transfer targets for Galatasaray's 2025/26 squad.

## What This Is

A full end-to-end scouting system: from raw player stats to an interactive recruitment dashboard. Built with Python, deployed on Streamlit.

## Pipeline

### 1. Data Collection
Player statistics sourced from FBref (2025/26 season), covering the top 5 European leagues. Filtered for players aged 18-27 with sufficient minutes played.

### 2. Role-Based Scouting
Players ranked by a composite ScoutScore across four position groups:
- Forward: goals, xG, shots on target
- Midfielder: key passes, progressive passes, tackles, interceptions
- Defender: tackles won, interceptions, aerials, clearances
- AttMid/Wing: goals, assists, xG, key passes, crosses

### 3. Player Similarity Model
Euclidean distance across normalised per-90 metrics within each position group. Surfaces statistically similar players, useful for finding cheaper alternatives to primary targets.

### 4. Market Valuation & Cost Efficiency
Market values sourced from Transfermarkt (2025/26). Efficiency score: ScoutScore divided by (MarketValue_EUR / 10,000,000). Highlights high-output players at low transfer cost.

### 5. Interactive Dashboard
Live Streamlit app with filters, radar charts, and similarity search.

## Repo Structure

data/players_data-2025_2026.csv — full player stats
data/scouting_report.csv — 40 scouted targets with ScoutScores
data/scouting_report_with_mv.csv — enriched with market values and efficiency
outputs/ — radar chart PNGs
scouting_pipeline.ipynb — full analysis notebook
app.py — Streamlit dashboard
requirements.txt

## Stack

Python: pandas, numpy, matplotlib
Streamlit: interactive dashboard
Data: FBref, Transfermarkt

## Author

Built by @drynoise as a football analytics portfolio project.
