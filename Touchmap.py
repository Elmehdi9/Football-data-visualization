# -*- coding: utf-8 -*-


import pandas as pd
import json 
import matplotlib.pyplot as plt
from PIL import Image
from mplsoccer.pitch import Pitch



with open(r'3845507.json', 'r') as f:
    data = json.load(f)
df = pd.json_normalize(data)

# Identify midfield positions
midfield_positions=['Left Center Midfield', 'Center Midfield', 'Right Center Midfield',
                  'Center Defensive Midfield', 'Left Defensive Midfield', 'Right Defensive Midfield']

# Identify actions that can be considered as touches
touches= ['Pass', 'Ball Receipt*', 'Carry','Ball Recovery', 'Miscontrol','Block', 'Dribble',
       'Shot','Own Goal Against', 'Own Goal For']

# Filter data based on midfield position and touch name
midfield_df= df.loc[df['position.name'].isin(midfield_positions) & df['type.name'].isin(touches)]
players= midfield_df['player.name'].unique()

# Set-up pitch subplots
pitch= Pitch(pitch_type='statsbomb',pitch_color='#E8DED1', line_color='#43464B', linewidth= .7, stripe= False)
fig, ax= pitch.grid(nrows= 2, ncols= 4, grid_height= .75, space= .05, axis= False)
fig.set_size_inches(15,8)
fig.set_facecolor('#E8DED1')
ax['pitch']= ax['pitch'].reshape(-1)
index=0

# Plot the data 
for player in players:
    player_df= midfield_df.loc[midfield_df['player.name']== player]
    touches_num= len(player_df)
    ax['pitch'][index].set_title(label=f"{player}", loc='left', x=.04, y=1.1, fontweight='bold')
    ax['pitch'][index].text(0,-8,f'Touches: {touches_num}',alpha=.7)
    x= list()
    y= list()
    for touch_event in player_df.itertuples():
        x.append(touch_event.location[0])
        y.append(touch_event.location[1])
    ax['pitch'][index].scatter(x=x, y=y, marker='p', color='#00613E', edgecolor='white', alpha=.5)
    pitch.kdeplot(x=x, y=y, ax=ax['pitch'][index], shade= True, levels=80, cmap="Greens", alpha=.2)
    index+=1
    
# Add title, subtitle to the figure 
title_text= "Touchmap For France Women's Midfielders vs Germany Women's"
subtitle= "UEFA Women's EURO 22 | Touches per player | Viz by: @dahbi_elmehdi"
fig.text(0.1, 0.955, title_text, fontweight="bold", fontsize=16, color='black')
fig.text(0.102, 0.925, subtitle, fontsize=14, color='black', alpha=.7)

# Add the UEFA EURO Women's logo
img_dir= "pictures/UEFA women's Euro.png"    
ax= fig.add_axes([.017, .9, 0.1, 0.1])
ax.axis("off")
img = Image.open(img_dir)
ax.imshow(img)
    

    


