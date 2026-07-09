
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import matplotlib.patches as mpatches
from math import pi

st.set_page_config(page_title="Gala Scout 25/26", layout="wide", page_icon="⚽")

@st.cache_data
def load_data():
    return pd.read_csv("data/scouting_report_with_mv.csv")

df = load_data()

# --- Sidebar ---
st.sidebar.title("🔍 Filters")
roles = ["All"] + sorted(df["Role"].unique().tolist())
selected_role = st.sidebar.selectbox("Position", roles)
max_mv = st.sidebar.slider("Max Market Value (€M)", 1, 50, 50)
min_score = st.sidebar.slider("Min ScoutScore", 0.0, 1.0, 0.0, step=0.01)

filtered = df.copy()
if selected_role != "All":
    filtered = filtered[filtered["Role"] == selected_role]
filtered = filtered[filtered["MarketValue_EUR"] <= max_mv * 1_000_000]
filtered = filtered[filtered["ScoutScore"] >= min_score]
filtered = filtered.sort_values("Efficiency", ascending=False).reset_index(drop=True)

# --- Header ---
st.title("⚽ Galatasaray Scout Report — 2025/26")
st.markdown(f"**{len(filtered)} players** match your filters.")

# --- Table ---
display_df = filtered[["Player","Role","Squad","ScoutScore","MarketValue_EUR","Efficiency"]].copy()
display_df["MarketValue_EUR"] = display_df["MarketValue_EUR"].apply(lambda x: f"€{x/1_000_000:.1f}M")
display_df["ScoutScore"] = display_df["ScoutScore"].apply(lambda x: f"{x:.3f}")
display_df["Efficiency"] = display_df["Efficiency"].apply(lambda x: f"{x:.3f}")
display_df.index = display_df.index + 1

st.dataframe(display_df, use_container_width=True)

# --- Radar Chart ---
st.markdown("---")
st.subheader("📡 Player Radar")

role_metrics = {
    "Forward":     ["Gls", "Ast", "xG", "xAG", "Sh", "SoT"],
    "Midfielder":  ["Ast", "xAG", "KP", "TklW", "Int", "PrgP"],
    "Defender":    ["TklW", "Int", "Clr", "AerWon", "Fld", "Crs"],
    "AttMid_Wing": ["Gls", "Ast", "xG", "xAG", "KP", "Crs"],
}

full_data = pd.read_csv("data/players_data-2025_2026.csv")

player_names = filtered["Player"].tolist()
selected_player = st.selectbox("Select player to view radar", player_names)

if selected_player:
    role = filtered[filtered["Player"] == selected_player]["Role"].values[0]
    metrics = role_metrics.get(role, role_metrics["Forward"])

    available = [m for m in metrics if m in full_data.columns]
    if not available:
        st.warning("Metrics not found in dataset.")
    else:
        player_row = full_data[full_data["Player"] == selected_player]
        if player_row.empty:
            st.warning(f"Player not found in full dataset: {selected_player}")
        else:
            vals = player_row[available].fillna(0).values[0].tolist()
            role_players = full_data[full_data["Pos"].str.contains(
                "FW" if role == "Forward" else
                "MF" if role == "Midfielder" else
                "DF", na=False
            )]
            mins = role_players[available].min()
            maxs = role_players[available].max()
            norm = [(v - mins[m]) / (maxs[m] - mins[m] + 1e-9) for v, m in zip(vals, available)]

            N = len(available)
            angles = [n / float(N) * 2 * pi for n in range(N)]
            angles += angles[:1]
            norm += norm[:1]

            fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
            fig.patch.set_facecolor("#1a1a2e")
            ax.set_facecolor("#1a1a2e")
            ax.plot(angles, norm, color="#e8b400", linewidth=2)
            ax.fill(angles, norm, color="#e8b400", alpha=0.3)
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(available, color="white", size=10)
            ax.set_yticklabels([])
            ax.spines["polar"].set_color("#444")
            ax.tick_params(colors="white")
            ax.set_title(selected_player, color="white", size=13, pad=15)
            st.pyplot(fig)

# --- Similarity ---
st.markdown("---")
st.subheader("🔁 Find Similar Players")

sim_player = st.selectbox("Find players similar to", player_names, key="sim")

if sim_player:
    role = filtered[filtered["Player"] == sim_player]["Role"].values[0]
    metrics = role_metrics.get(role, role_metrics["Forward"])
    available = [m for m in metrics if m in full_data.columns]

    if available:
        role_df = full_data[full_data["Pos"].str.contains(
            "FW" if role == "Forward" else
            "MF" if role == "Midfielder" else
            "DF", na=False
        )].copy()

        role_df = role_df.dropna(subset=available)
        if sim_player in role_df["Player"].values:
            target = role_df[role_df["Player"] == sim_player][available].values[0]
            others = role_df[role_df["Player"] != sim_player].copy()
            others["Distance"] = others[available].apply(
                lambda row: np.sqrt(np.sum((row.values - target) ** 2)), axis=1
            )
            top5 = others.nsmallest(5, "Distance")[["Player", "Squad"] + available + ["Distance"]]
            st.dataframe(top5.reset_index(drop=True), use_container_width=True)
        else:
            st.warning("Player not found in full dataset for similarity.")
