import streamlit as st
import psycopg2
from datetime import date

import psycopg2

import psycopg2

def get_connection():
    return psycopg2.connect(
        host="aws-0-us-east-2.pooler.supabase.com",
        port="6543",
        dbname="postgres",
        user="postgres.yguikznmzbkidxouchyf",
        password="#Nevertoolate24",
        sslmode="require"
    )






# --- Insert New Game ---
def insert_game(user, stadium, team1, team2, winner, game_date):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO games (user_name, stadium, team_1, team_2, winner, game_date)
        VALUES (%s, %s, %s, %s, %s, %s);
    """, (user, stadium, team1, team2, winner, game_date))
    conn.commit()
    cur.close()
    conn.close()

# --- Fetch Games ---
def fetch_games(user):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT stadium, team_1, team_2, winner, game_date FROM games WHERE user_name = %s ORDER BY game_date DESC;", (user,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

# --- Streamlit App ---
st.title("🏟️ My Personal Stadium Tracker")

st.header("➕ Add a Game You Attended")

with st.form("add_game_form"):
    user_name = st.text_input("Your Name", value="Dillon Singh")
    stadium_name = st.text_input("Stadium Name")
    team_1 = st.text_input("Team 1 (e.g. Yankees)")
    team_2 = st.text_input("Team 2 (e.g. Red Sox)")
    game_date = st.date_input("Date of Game", value=date.today())

    winner = st.selectbox(
        "Who won?",
        options=[f"{team_1}", f"{team_2}", "Draw"] if team_1 and team_2 else ["Enter both teams to select winner"],
        disabled=not (team_1 and team_2)
    )

    submitted = st.form_submit_button("Add Game")
    if submitted:
        if not (stadium_name and team_1 and team_2 and winner and game_date):
            st.error("Please complete all fields.")
        else:
            insert_game(user_name, stadium_name, team_1, team_2, winner, game_date)
            st.success("Game successfully added!")

# --- Display Logged Games ---
st.markdown("## 📋 Your Logged Games")
games = fetch_games("Dillon Singh")  # hardcoded for MVP
if games:
    st.dataframe(games, use_container_width=True)
else:
    st.info("No games logged yet.")










