from pathlib import Path
import json
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

root=Path(__file__).resolve().parents[1]
import argparse
parser = argparse.ArgumentParser(description="Redraw the three supplement figures from the archived result counts.")
parser.add_argument("--output", type=Path, required=True, help="Output folder for PNGs")
out=parser.parse_args().output
out.mkdir(parents=True,exist_ok=True)
data=json.loads((root/"results"/"result_counts.json").read_text())
mpl.rcParams.update({"font.family":"DejaVu Sans","font.size":10,"savefig.facecolor":"white"})
ink, gray, teal, light = "#162e37","#425963","#235a67","#e9f1f2"

rows=[
    ("Retrieve the edition", "Project Gutenberg eBook 164 in English"),
    ("Identify paragraphs", "1,680 content paragraphs with persistent IDs"),
    ("Normalize a text copy", "Tokens and stems alongside the original wording"),
    ("Search for keywords", "659 candidates and 1,021 nonmatches retained"),
    ("Code the pilot blind", "30 candidates and 20 nonmatches, then reviewed codes"),
    ("Review priority passages with AI", "60 proposed codes, themes, and rationales"),
    ("Examine curriculum links", "976 unit candidates and 62 scored outcome pairs"),
    ("Summarize each stage", "Counts and decision sources linked to paragraph IDs"),
]
fig, ax=plt.subplots(figsize=(8.55,2.76))
ax.set_xlim(0,1); ax.set_ylim(-.2,9.0);ax.axis("off")
ax.add_patch(plt.Rectangle((.005,8.10),.99,.84,color=teal,lw=0))
ax.text(.021,8.52,"Stage",ha="left",va="center",weight="bold",color="white",fontsize=11)
ax.text(.426,8.52,"Record retained",ha="left",va="center",weight="bold",color="white",fontsize=11)
for i,(operation,evidence) in enumerate(rows):
    y=7.62-i
    if i%2==0:
        ax.add_patch(plt.Rectangle((.005,y-.5),.99,1,color=light,lw=0))
    ax.text(.021,y,f"{i+1}.  {operation}",ha="left",va="center",color=ink,fontsize=10.2)
    ax.text(.426,y,evidence,ha="left",va="center",color=ink,fontsize=10.2)
fig.subplots_adjust(.005,.01,.995,.99)
fig.savefig(out/"Figure_1_Workflow.png",dpi=300,pad_inches=0)
plt.close(fig)

fig,ax=plt.subplots(figsize=(8.2,3.7))
items=list(data["overlapping_candidate_groups"].items())
ax.barh(range(len(items)),[v for _,v in items],color=teal,height=.51)
ax.set_yticks(range(len(items)),[k for k,_ in items]);ax.invert_yaxis()
n=data["expanded_keyword_candidates"]
for i,(_,v) in enumerate(items):
    ax.text(v+6,i,f"{v}  ({v/n:.2%})",va="center",fontsize=10,color=ink)
ax.set_xlim(0,545);ax.set_xticks([0,100,200,300,400,500])
ax.grid(axis="x",color="#dce4e6",lw=.8);ax.set_axisbelow(True)
ax.set_xlabel("Candidate paragraphs",labelpad=7)
ax.tick_params(axis="both",length=0,labelcolor=ink)
for s in ax.spines.values():s.set_visible(False)
fig.subplots_adjust(left=.365,right=.975,top=.83,bottom=.23)
fig.text(.025,.93,"Keyword matches by thematic group",size=15,weight="bold",color=ink)
fig.text(.025,.045,"Percentages use 659 candidate paragraphs as the denominator. A paragraph can match more than one group.",size=8.6,color=gray)
fig.savefig(out/"Figure_2_Keyword_Candidates.png",dpi=300)
plt.close(fig)

fig,ax=plt.subplots(figsize=(8.2,3.35))
codes=["2","1","0"]; names=["Direct science content","Indirect science connection","No science content"]
levels=data["combined_preliminary_codes"]
ax.barh(range(3),[levels[c]["percent"] for c in codes],height=.5,color=[teal,"#59868a","#75848b"])
ax.set_yticks(range(3),names);ax.invert_yaxis();ax.set_xlim(0,78);ax.set_xticks([0,20,40,60],["0%","20%","40%","60%"])
for i,c in enumerate(codes):
    v=levels[c]
    ax.text(v["percent"]+.9,i,f'{v["n"]:,}  ({v["percent"]:.2f}%)',va="center",color=ink)
ax.grid(axis="x",color="#dce4e6",lw=.8);ax.set_axisbelow(True);ax.tick_params(axis="both",length=0,labelcolor=ink)
for s in ax.spines.values():s.set_visible(False)
fig.subplots_adjust(left=.29,right=.975,top=.77,bottom=.24)
fig.text(.025,.91,"Preliminary science-content labels",size=15,weight="bold",color=ink)
fig.text(.025,.805,"Combined classification of 1,680 numbered paragraphs",size=10,color=gray)
fig.text(.025,.074,"Label sources: 1,570 by rules, 60 by AI contextual review, and 50 by researcher-reviewed pilot decisions.",size=8.7,color=gray)
fig.text(.025,.019,"The percentages shown are rounded.",size=8.7,color=gray)
fig.savefig(out/"Figure_3_Preliminary_Labels.png",dpi=300)
plt.close(fig)
