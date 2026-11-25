from pathlib import Path
from io import BytesIO
import argparse
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont

PROJECT = Path(__file__).resolve().parents[2]
SOURCE = PROJECT / "figures" / "manuscript-tr"
FIGURE_NAMES = {2: 'Figure_1_Workflow.png', 3: 'Figure_2_Keyword_Candidates.png', 4: 'Figure_3_Preliminary_Labels.png'}
parser = argparse.ArgumentParser(description="Render the English labels on the full manuscript's three original figure layouts.")
parser.add_argument("--output", type=Path, required=True, help="Folder for the English PNG files")
OUTPUT = parser.parse_args().output
OUTPUT.mkdir(parents=True, exist_ok=True)
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans"
@lru_cache(maxsize=None)
def font(family, bold, pixels):
    if family == "serif": name = SERIF + ("Bold" if bold else "Regular") + ".ttf"
    else: name = SANS + ("-Bold" if bold else "") + ".ttf"
    return ImageFont.truetype(name, pixels)

class Overlay:
    def __init__(self, number, virtual_width):
        self.number = number
        self.image = Image.open(SOURCE / FIGURE_NAMES[number]).convert("RGBA")
        self.d = ImageDraw.Draw(self.image)
        self.s = self.image.width / virtual_width
    def point(self, coords):
        return tuple(round(x*self.s) for x in coords)
    def box(self, region, color="white"):
        self.d.rectangle(self.point(region), fill=color)
    def rounded(self, region, color, r):
        self.d.rounded_rectangle(self.point(region), radius=round(self.s*r), fill=color)
    def text(self, pos, line, size, *, color="black", bold=False, family="sans", anchor="lm", max_width=None):
        pixels = round(size*self.s)
        while max_width and font(family,bold,pixels).getlength(line) > max_width*self.s:
            pixels -= 1
        self.d.text(self.point(pos), line, fill=color, font=font(family,bold,pixels), anchor=anchor, stroke_width=0)
    def lines(self, x, center, lines, step, size, **kw):
        for k,line in enumerate(lines):
            self.text((x,center+(k-(len(lines)-1)/2)*step),line,size,**kw)
    def blank_bar_annotation(self, x, y, w):
        x1,y1,x2,y2=self.point((x, y-11, x+w, y+11))
        sy=round((y-21)*self.s)
        clean=self.image.crop((x1,sy,x2,sy+1)).resize((x2-x1,y2-y1))
        self.image.paste(clean,(x1,y1))
    def save(self):
        # Keep the source resolution and color information. Word uses physical
        # resolution when it calculates the tight text wrap around these charts.
        def chunks(payload):
            i=8
            while i < len(payload):
                size=int.from_bytes(payload[i:i+4], "big")
                yield payload[i+4:i+8],payload[i:i+12+size]
                i+=12+size
        source=(SOURCE / FIGURE_NAMES[self.number]).read_bytes()
        metadata=b"".join(c for name,c in chunks(source) if name in (b"pHYs",b"gAMA",b"sRGB",b"tEXt"))
        buffer=BytesIO();self.image.save(buffer,format="PNG",optimize=True)
        edited=bytearray(source[:8])
        for name,chunk in chunks(buffer.getvalue()):
            edited.extend(chunk)
            if name==b"IHDR":edited.extend(metadata)
        (OUTPUT / FIGURE_NAMES[self.number]).write_bytes(edited)

def workflow():
    a=Overlay(2,805)
    sh=dict(family="serif")
    a.box((265,10,353,40));a.box((656,10,726,40))
    a.text((308,25),"Stage",16,bold=True,anchor="mm",**sh)
    a.text((691,25),"Output",16,bold=True,anchor="mm",**sh)
    data=[
        ("Acquire the source text",["Download the English text (.txt) of the novel from Project Gutenberg", "(eBook 164) and upload it to Google Colab."],["Plain-text file (.txt)"],["Researcher"]),
        ("Prepare the corpus",["Remove the front matter and contents. Divide the text into paragraphs", "and assign each paragraph an identifier."],["1,680 content paragraphs", "(unit of analysis)"],["Python / NLP"]),
        ("Preprocess a text copy",["Lowercase and tokenize a copy, remove short and frequent words,", "and apply Porter stemming. Retain the original paragraphs."],["Preprocessed text copy"],["Python / NLP"]),
        ("Search for concepts by keyword",["Search the original paragraphs using five thematic concept lists", "and regular expressions."],["659 candidate paragraphs (39.23%)", "1,021 with no match"],["Python / NLP"]),
        ("Select and code the pilot sample",["Select 30 candidates and 20 nonmatches (random seed 20261015).", "Code each paragraph 0, 1 or 2 before viewing the automated labels."],["50 pilot paragraphs", "with researcher codes"],["Researcher"]),
        ("Review paragraphs in context",["Request a code, theme and rationale for 60 priority paragraphs.", "A later automated pass reclassifies all 1,680 paragraphs."],["Provisional AI codes"],["ChatGPT (AI)"]),
        ("Match passages to the curriculum",["Screen the 44 units and 182 outcomes using concept lists.", "Review 62 proposed outcome links with AI assistance."],["437 paragraphs", "976 candidate unit links"],["Python / NLP","ChatGPT (AI)"]),
        ("Analyze the data",["Calculate counts, percentages and pilot agreement. Report automated", "results and researcher decisions separately."],["Findings for five", "research questions"],["Python / NLP","Researcher"])
    ]
    colors={"Researcher":(62,142,90),"Python / NLP":(47,111,168),"ChatGPT (AI)":(217,130,43)}
    tops=[53.5,160.8,268.1,375.5,482.8,590.2,697.5,804.9]
    for top,(title,body,output,agents) in zip(tops,data):
        a.box((71,top+2,557,top+81),"white")
        a.text((75,top+14),title,15,bold=True,max_width=(284 if len(agents)==2 else 380),**sh)
        for j,line in enumerate(body):
            a.text((75,top+41+15*j),line,13.4,max_width=475,**sh)
        if len(agents)==1:
            starts=[469 if agents[0]=="Researcher" else 463]; ends=[552]
        elif agents[1]=="Researcher":
            starts,ends=[373,469],[462,552]
        else:
            starts,ends=[367,463],[456,552]
        for who,lo,hi in zip(agents,starts,ends):
            a.rounded((lo,top+6,hi,top+23),colors[who],6)
            a.text(((lo+hi)/2,top+14.5),who,11.4,bold=True,color="white",anchor="mm",max_width=hi-lo-6,**sh)
        a.box((591,top+16,791,top+68),(241,241,241))
        a.lines(691,top+42,output,15,13.2,anchor="mm",max_width=194,**sh)
    a.box((48,912,606,944))
    a.text((54,928),"Performed by",13.2,bold=True,**sh)
    for x,who,label in [(139,"Python / NLP","Python / NLP (automated)"),(328,"ChatGPT (AI)","ChatGPT (AI-assisted)"),(500,"Researcher","Researcher")]:
        a.box((x,921,x+14,935),colors[who]);a.text((x+20,928),label,13.1,**sh)
    a.save()

def themes():
    a=Overlay(3,860)
    a.box((25,6,802,69))
    a.text((34,24),"Thematic distribution of candidate paragraphs",19.8,bold=True)
    a.text((34,55),"Corpus: 1,680 paragraphs  |  Keyword candidates: 659 paragraphs",12.6,color=(77,77,77))
    a.box((10,78,252,345))
    labels=["Natural environment and interaction","Living things and biodiversity","Science and technology","Supplementary science search","Earth and geosciences"]
    for y,end,label,number in zip([105,160,215,269,323],[715,500,433,298,286],labels,["419  (63.58%)","222  (33.69%)","160  (24.28%)","37  (5.61%)","26  (3.95%)"]):
        a.text((244,y),label,13.7,anchor="rm",max_width=238)
        a.blank_bar_annotation(end+2,y,min(125,854-end-2))
        a.text((end+9,y),number,13.7)
    a.box((360,375,734,406))
    a.text((542,390),"Number of candidate paragraphs (f)",13.5,anchor="mm")
    a.box((25,420,827,493))
    for i,line in enumerate(["Percentages use the 659 candidate paragraphs as the denominator. A paragraph may appear in several groups.", "The supplementary search extends the four thematic lists.", "Bars show keyword matches before contextual review."]):
        a.text((34,442+i*15),line,11.2,color=(69,69,69))
    a.save()

def levels():
    a=Overlay(4,860)
    a.box((45,12,808,84))
    a.text((52,31),"Distribution of paragraphs by science content level",20.6,bold=True)
    a.text((52,67),"Entire novel  •  1,680 paragraphs  •  Combined preliminary codes",14.3,color=(75,87,106))
    palette=[(40,101,121),(128,179,186),(212,217,223)]
    for left,right,x,lines,shade,col in [(54,122,88,["162","9.64%"],palette[0],"white"),(128,335,231,["474","28.21%"],palette[1],(19,43,54)),(341,805,573,["1,044","62.14%"],palette[2],(19,43,54))]:
        a.box((left,188,right,233),shade)
        a.lines(x,211,lines,17.2,15.3,bold=True,anchor="mm",color=col)
    a.box((27,294,835,337))
    for x,label in zip([52,203,354,505,657,807],["0%","20%","40%","60%","80%","100%"]):
        a.text((x,306),label,14.5,anchor="mm")
    for x,name,shade in [(145,"Direct science content",palette[0]),(338,"Indirect science relation",palette[1]),(541,"No science content",palette[2])]:
        a.box((x,321.5,x+27,330.5),shade);a.text((x+35,326),name,13.1)
    a.box((46,378,840,456))
    a.text((52,394),"Direct or indirect science relation: 636 paragraphs (37.86%)",15,bold=True,color=(32,104,126))
    a.text((52,430),"Rule-based codes, reviewed pilot decisions and AI assessments of selected paragraphs were combined.",11,color=(72,72,72))
    a.text((52,444),"Researcher review covered the pilot. Rounding brings the total to 99.99%.",11,color=(72,72,72))
    a.save()
workflow();themes();levels()
