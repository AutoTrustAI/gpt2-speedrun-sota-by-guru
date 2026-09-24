"""Regenerate the public training-time comparison with matplotlib."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
root=Path(__file__).resolve().parents[1]
current=json.loads((root/'results/nc033/metrics.json').read_text())
labels=['AutoTrust · ScienceGuru','Giovanni Zinzi · mixed data','Giovanni Zinzi · ClimbMix','Oriole Networks · n-grams','Official leaderboard · Run 6']
values=[current['training_minutes'],73.917,81.835,91.74,99.0]
core=['0.259212','0.267123','0.261814','0.2578','0.262634']
plt.rcParams.update({'font.family':'DejaVu Sans','svg.fonttype':'none','font.size':11})
fig,ax=plt.subplots(figsize=(13.2,5.4),facecolor='white')
fig.subplots_adjust(left=.27,right=.91,top=.74,bottom=.23)
colors=['#2363e8','#b8c5dd','#b8c5dd','#b8c5dd','#6f85a7']
bars=ax.barh(range(len(values)),values,height=.55,color=colors,zorder=3)
ax.set_yticks(range(len(values)),labels);ax.invert_yaxis();ax.set_xlim(0,110)
ax.set_xticks([0,20,40,60,80,100]);ax.set_xlabel('Native training time (minutes) · lower is faster',color='#4b5870',labelpad=12)
ax.tick_params(axis='both',length=0,pad=8,colors='#26344d');ax.xaxis.grid(True,color='#e7edf5',linewidth=.8,zorder=0)
for s in ax.spines.values():s.set_visible(False)
for i,(bar,value) in enumerate(zip(bars,values)):
 label=f'{value:.2f}' if i==0 else ('≈99.00' if i==4 else f'{value:.3f}')
 ax.text(value+1.25,bar.get_y()+bar.get_height()/2,label,va='center',weight='bold' if i==0 else 'normal',color='#163462' if i==0 else '#485870',fontsize=11)
fig.text(.045,.935,'GPT-2 Speedrun',fontsize=24,weight='bold',color='#13284a')
fig.text(.045,.868,'ScienceGuru + Guru Turbo 1.2   /   AutoTrust',fontsize=13,color='#526784')
fig.text(.95,.932,'72.24 min',ha='right',fontsize=24,weight='bold',color='#2363e8')
fig.text(.95,.866,'CORE 0.259212  ·  8×H100',ha='right',fontsize=12,color='#526784')
fig.text(.045,.035,'CORE target > 0.256525  ·  Reported run counts and source links accompany the comparison table.',fontsize=10,color='#61718b')
for suffix in ['svg','png']:
 fig.savefig(root/'assets'/f'gpt2-comparison.{suffix}',dpi=180,facecolor='white',metadata={'Title':'GPT-2 Speedrun training-time comparison'})
plt.close(fig)
