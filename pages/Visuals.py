# This creates the page for displaying data visualizations.

import streamlit as st
import json
import pandas as pd
import plotly.express as px
# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# PAGE TITLE
st.title("Data Visualizations 📈")


# PART 1: GRAPHS FROM data.json
with open("data.json") as f:
    Golf = json.load(f)

st.subheader(Golf["chart_title"])
holes = []
scores = []
pars = []
putts = []

for hole in Golf["data_points"]:
    holes.append(hole["Label"])
    scores.append(hole["Score"])
    pars.append(hole["Par"])
    putts.append(hole["Putts"])


df = pd.DataFrame({"Scores": scores}, index=holes)
st.bar_chart(df, x_label="Hole", y_label="Strokes")

if "stat" not in st.session_state:
    st.session_state.stat = "Score"

choice = st.radio("Show:", ["Score", "Par", "Putts"])
st.session_state.stat = choice
stats = {"Score": scores, "Par": pars, "Putts": putts}
selected = stats[st.session_state.stat]

fig = px.line(x=holes, y=selected, title=st.session_state.stat+ " by Hole",
              labels={"x": "Hole", "y": st.session_state.stat}, markers=True)
st.plotly_chart(fig)



# PART 2: GRAPHS FROM data.csv
# --- YOUR CODE GOES HERE ---
golf_csv = pd.read_csv("data.csv")
st.write(golf_csv)
club_counts = golf_csv["Club"].value_counts()

fig2 = px.pie(names=club_counts.index, values=club_counts.values, title="How Often I used Each Club Off the Tee")

st.plotly_chart(fig2)
if "csv_stat" not in st.session_state:
    st.session_state.csv_stat = "Score"

choice2 = st.radio("Show average:", ["Score", "Putts"])
st.session_state.csv_stat = choice2

avg = golf_csv.groupby("Hole")[st.session_state.csv_stat].mean()

fig3 = px.bar(x=avg.index, y=avg.values, title="Average " + st.session_state.csv_stat + " by Hole", labels={"x":"Hole", "y": st.session_state.csv_stat})
st.plotly_chart(fig3)
