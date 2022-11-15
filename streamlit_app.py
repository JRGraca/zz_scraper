import streamlit as st
import numpy as np
import pickle
from statsmodels.sandbox.regression.predstd import wls_prediction_std

with open('model.pkl', 'rb') as f:
	model = pickle.load(f)

st.set_page_config(page_title="League table prediction")

st.title("Are you ready for some football?")
st.image("Images/ball.png", width=100)


st.write("Is your favorite team about to be champion?\nWould they like to avoid relegation? Find out how many points do they need and if they are on the right track with this powerful AI model trained in over 300 league tables from 20 competitions")



# Inputs:
# Desired classification
# Current number of points
# Number of games played

# Outputs
# Total number of points predicted
# 95% range
# Total number of points needed (min, exp, max)
# Average number of points needed (min, exp, max)
# 
desired_rank = st.number_input(label="What place would your team like to achieve in the table?", value = 1, step=1)
teams_n = st.slider(label="How Many Teeams are in your League?", min_value=16, max_value=24, step=1)
current_points = st.number_input(label="How many points does your team currently have?", value = 0, step=1)
games_played = st.number_input(label="How many games have been played already?", value = 0, step=1)
if(st.button("Calculate!")):
	total_games_in_league = teams_n * 2 - 2
	result = model.predict([desired_rank, teams_n])[0]
	lower_bound = result - wls_prediction_std(model)[0].mean()
	upper_bound = result + wls_prediction_std(model)[0].mean()
	points_to_goal = result - current_points
	up_points_to_goal = upper_bound - current_points
	lo_points_to_goal = lower_bound - current_points
	games_left = total_games_in_league - games_played
	if games_left <= 0:
		eval_string = "Isn't the league finished already?"
	elif (current_points/games_played > 3):
		eval_string = "Please check your inputs (it seems you can score more than 3 points per game)"
	else:
		if (points_to_goal / games_left) > 3:
			eval_string = f"We estimate it's highly unlikely or impossible you'll achieve your goal. Sorry"
		else:
			eval_string = f"According to the model, you're going to need another {round(points_to_goal, 2)} points to reach your desired position  \nThe model is highly confident you'll reach your goal \
				if you collect between {round(lo_points_to_goal, 2)} and {round(up_points_to_goal, 2)} points.  \nThat's between {round(lo_points_to_goal / games_left, 2)} and\
					{round(up_points_to_goal / games_left, 2)} points per game with an average of {round(points_to_goal / games_left, 2)} points per game  "
			if (games_played == 0):
				eval_string = f"It's the beggining of the league.  \n" + eval_string
			elif (current_points / games_played) >= (points_to_goal / games_left):
				eval_string += f"\nThe good news is if you keep up your pace ({round(current_points / games_played, 2)} points per game), you have a great chance of achieving it!"
			else:
				eval_string += f"\nYou currently have an average of {round(current_points / games_played, 2)} points per game."
	st.success(eval_string)
