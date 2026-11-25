from copy import deepcopy
import argparse
from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E

PROJECT = Path(__file__).resolve().parents[2]
source = PROJECT / "manuscripts" / "drafts" / "Gulsum_Meco_makale_EN (2).docx"
FIGURE_NAMES = {2: 'Figure_1_Workflow.png', 3: 'Figure_2_Keyword_Candidates.png', 4: 'Figure_3_Preliminary_Labels.png'}
parser = argparse.ArgumentParser(description="Rebuild the full revised article from its English Word draft.")
parser.add_argument("--output", type=Path, required=True, help="Output .docx file")
parser.add_argument("--figures", type=Path, default=PROJECT / "figures" / "manuscript-en")
args = parser.parse_args()
out = args.output
out.parent.mkdir(parents=True, exist_ok=True)
zipin = ZipFile(source)
root = E.fromstring(zipin.read("word/document.xml"))
rels = E.fromstring(zipin.read("word/_rels/document.xml.rels"))
W="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PK="http://schemas.openxmlformats.org/package/2006/relationships"
XMLSPACE="{http://www.w3.org/XML/1998/namespace}space"
wp=lambda name: "{"+W+"}"+name
par = root.find(wp("body")).findall(wp("p"))
def nodes(i): return [t for r in par[i].findall(wp("r")) for t in r.findall(wp("t"))]
def sub(i,before,after):
    ts=[t for t in nodes(i) if before in (t.text or "")]
    assert len(ts)==1 and ts[0].text.count(before)==1,(i,before)
    ts[0].text=ts[0].text.replace(before,after)
def add(i,s):
    t=[t for t in nodes(i) if t.text and t.text.strip()][-1]
    t.text=t.text.rstrip()+" "+s
def body(i):
    return "".join(t.text or "" for t in nodes(i))
def hyperlink(i,label,url):
    target = next(t for t in nodes(i) if label in (t.text or ""))
    before,after = target.text.split(label)
    original_run = target.getparent()
    assert original_run.getparent() is par[i]
    target.text=before;target.set(XMLSPACE,"preserve")
    ids={x.get("Id") for x in rels}
    idx=1
    while f"rId{idx}" in ids:idx+=1
    rid=f"rId{idx}"
    E.SubElement(rels,"{"+PK+"}Relationship",Id=rid,Type=R+"/hyperlink",Target=url,TargetMode="External")
    h=E.Element(wp("hyperlink"));h.set("{"+R+"}id",rid)
    def make_run(s):
        run=E.Element(wp("r"))
        props=original_run.find(wp("rPr"))
        if props is not None: run.append(deepcopy(props))
        t=E.SubElement(run,wp("t"));t.text=s;t.set(XMLSPACE,"preserve")
        return run
    link_run=make_run(label)
    props=link_run.find(wp("rPr"))
    if props is None:
        props=E.Element(wp("rPr"));link_run.insert(0,props)
    if props.find(wp("u")) is None:
        E.SubElement(props,wp("u")).set(wp("val"),"single")
    h.append(link_run)
    at=par[i].index(original_run)+1;par[i].insert(at,h)
    if after:par[i].insert(at+1,make_run(after))

sub(6,"Paragraphs were pre-classified by keywords, coded through AI-assisted contextual evaluation under researcher control, and matched with the science curriculum.","Keywords identified candidate paragraphs for contextual review. The researcher reviewed the pilot codes, and selected passages were examined against science curriculum outcomes.")
sub(6,"Of the paragraphs, 9.64% contained direct and 28.21% indirect science content.","In the combined preliminary classification, 9.64% of paragraphs received a direct science content code and 28.21% an indirect code.")
sub(6,"In the 50-paragraph pilot, automatic and contextual codes agreed in 58% of cases.","In the 50-paragraph pilot, the rule-based and final researcher-reviewed codes agreed in 29 cases (58%).")
sub(6,"The results indicate that the approach is useful for preliminary screening but requires contextual verification. Automatic outputs should not be used as final classifications.","The study illustrates how researchers can repeat the screening procedure, trace decisions to the original passages, and use contextual evidence to verify preliminary codes.")

add(12,"A keyword can locate a passage about a scientific concept. Reading the paragraph in context establishes whether the narrator merely names the concept or uses it to explain an observation.")
add(14,"Retaining each paragraph’s identifier across stages allows the reader to trace a coding decision back to the passage that supports it.")
sub(26,"So that researchers with no coding experience can also apply it, the workflow is explained below.","The author’s Colab notebook and companion scripts are available on GitHub. The steps below explain the workflow for researchers with no coding experience.")
hyperlink(26,"available on GitHub","https://github.com/Biologist1/Biologist1/tree/93b3d2c6de9686ed8df498dac79cc99478173f61/projects/verne-science-education")

sub(34,"In the initial scan conducted with five thematic concept lists in this study, 659 paragraphs were identified as science content candidates.","Four concept lists initially identified 622 distinct paragraphs. The supplementary science search added 37, yielding 659 candidates across five groups.")
sub(36,"The three coding levels are given in Table 1.","For example, a question about fearing sharks received code 0 (P932), whereas an explanation of how a pearl forms received code 2 (P921). Table 1 defines the three coding levels.")
sub(39,"A total of 30 paragraphs were selected from the five candidate groups identified in the initial scan, and 20 paragraphs were selected from those with no keyword match.","Six paragraphs were selected from each of the five candidate groups and 20 from those with no keyword match.")
sub(40,"These codes were then compared with the automated preliminary codes, and the paragraphs for which different decisions were made were identified.","The initial decisions were retained. The researcher then considered ChatGPT’s separate contextual suggestions and recorded a final code for each paragraph. Table 6 compares these final codes with the rule-based pre-codes.")
sub(42,"All 1,680 paragraphs of the novel were put through a second automated classification, and the changes were recorded by comparing the previous and current codes.","After the combined preliminary codes reported in Figure 3 had been recorded, all 1,680 paragraphs underwent a second automated classification. Changes from the earlier codes were recorded separately.")
sub(53,"the automated preliminary codes were compared with the researcher’s codes.","the rule-based preliminary codes were compared with the researcher’s final contextual codes.")
sub(66,"The distribution of the novel’s 1,680 paragraphs by science content level is presented in the figure below.","Figure 3 shows the combined preliminary codes for the novel’s 1,680 paragraphs by science content level.")
sub(67,"Distribution of paragraphs by science content level","Preliminary distribution of paragraphs by science content level")
sub(68,"As seen in Figure 3, 162 of the paragraphs","In this preliminary classification, 162 of the paragraphs")
sub(68,"The 636 paragraphs identified as having a direct or indirect science relation","The 636 paragraphs assigned a direct or indirect science code")
sub(68,"Among the science-related paragraphs, indirect content was found to outnumber direct content.","Among these paragraphs, indirect codes outnumbered direct codes.")
add(68,"This distribution combines 1,570 rule-based codes, 60 AI-assisted contextual codes for priority passages and 50 researcher-reviewed pilot codes.")
sub(77,"In the full-text scan, 86 match candidates related to four learning outcomes were identified in 84 different paragraphs.","In the full-text scan, 86 candidate links to four selected learning outcomes in Grades 5, 6, and 8 were identified in 84 different paragraphs.")
sub(77,"The results are presented in Table 4.","The remaining 24 links were unscored. The results are presented in Table 4.")
sub(81,"Of the 62 matches examined contextually, a direct relationship was identified in 7 (11.29%) and a partial relationship in 27 (43.55%); in 28 (45.16%), the proposed relationship was not supported.","The AI-assisted contextual review rated 7 of the 62 matches (11.29%) as direct and 27 (43.55%) as partial. It found insufficient support for the proposed relationship in 28 (45.16%).")
sub(89,"the codes produced after contextual review.","the researcher’s final codes after AI-assisted contextual review.")
sub(99,"This rate shows the need for contextual review of automated preliminary codes.","The disagreements identify passages in which reading the surrounding explanation changed how a keyword was interpreted.")
sub(102,"it can be said that this approach could reduce a preliminary scanning process that takes days to a matter of hours.","automating the initial search and preparation of coding tables may reduce the researcher’s workload. Analysis time was not measured in this study.")
sub(103,"The findings for the second question show that, of the 1,680 paragraphs,","In the combined preliminary coding for the second question, of the 1,680 paragraphs,")
sub(103,"and that the 636 science-related paragraphs make up 37.86% of the text.", "and the 636 paragraphs assigned a direct or indirect code make up 37.86% of the text.")
sub(103,"That indirectly related paragraphs outnumber direct content ones shows that,","The larger number of indirect codes suggests that,")
sub(103,"the finding that about 38% of the text is directly or indirectly science-related","the finding that about 38% of the text received a direct or indirect code")
sub(103,"the 162 paragraphs with direct science content offer","the 162 paragraphs provisionally coded as direct content offer")
sub(105,"of the 62 matches examined contextually, only 7 (11.29%) showed a direct relationship and 27 (43.55%) a partial relationship, and in 28 (45.16%) the proposed relationship was not supported.","the AI-assisted review rated 7 of the 62 examined matches (11.29%) as direct, 27 (43.55%) as partial and 28 (45.16%) as unsupported.")
sub(109,"That six of the 18 paragraphs that the pilot dataset automatically indicated as having no science content were found science-related in the contextual review shows that it is useful to take a control sample from paragraphs with no matches as well.","In the pilot, six of the 18 paragraphs assigned rule-based code 0 received a science-related code on review. Among the 20 paragraphs sampled specifically because they had no keyword match, the researcher assigned six direct codes and one indirect code. Sampling paragraphs missed by the keyword search can therefore reveal scientific passages that warrant closer reading.")
add(110,"The original Colab notebook documents lexical preprocessing. The new verification script recalculates the reported counts from the archived records, and the example dictionary illustrates how to adapt the screening procedure. The supplement gives four Turkish instructions and their English translations. The complete historical search dictionary, thematic screening script, contextual exchange logs and exact ChatGPT model settings were unavailable.")
sub(114,"the agreement between automated and contextual codes should be supported by reliability coefficients with a second human coder; larger pilot datasets should be used, and different artificial intelligence models should be compared.","two human coders should independently code a larger pilot and their agreement should be examined before reconciliation. The same design could then be used to compare different artificial intelligence models.")

def xml(t):
    return E.tostring(t,encoding="UTF-8",xml_declaration=True,standalone=True)
changed={"word/document.xml":xml(root),"word/_rels/document.xml.rels":xml(rels)}
for n in [2,3,4]:changed[f"word/media/image{n}.png"]=(args.figures / FIGURE_NAMES[n]).read_bytes()
with ZipFile(out,"w") as z:
    for entry in zipin.infolist():
        z.writestr(entry,changed.get(entry.filename,zipin.read(entry.filename)))
print(out)
