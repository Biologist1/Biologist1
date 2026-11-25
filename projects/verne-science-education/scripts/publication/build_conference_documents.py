from pathlib import Path
from copy import deepcopy
import re
import argparse
from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor
from article_content import title, pages, refs

project=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser(description="Rebuild the extended abstract and author response documents.")
parser.add_argument("--output",type=Path,required=True,help="Directory for Word documents")
output=parser.parse_args().output
output.mkdir(parents=True,exist_ok=True)
abstract_path = output/"EduAI2027_13803_Revised_Extended_Abstract.docx"
letter_path = output/"EduAI2027_13803_Response_to_Reviewers.docx"
dark=RGBColor.from_string("131313")
gray=RGBColor.from_string("374149")

def set_font(style, name, size, bold=False):
    style.font.name=name
    style.font.size=Pt(size)
    style.font.bold=bold
    style.font.color.rgb=dark
    pr=style.element.get_or_add_rPr()
    fonts=pr.find(qn("w:rFonts"))
    if fonts is not None:
        for attr in ("asciiTheme","hAnsiTheme","cstheme","eastAsiaTheme"):
            fonts.attrib.pop(qn("w:"+attr),None)
        for attr in ("ascii","hAnsi","cs","eastAsia"):
            fonts.set(qn("w:"+attr),name)
    for col in pr.findall(qn("w:color")):
        col.attrib.pop(qn("w:themeColor"),None)

def style(doc,name,size,after,before=0,bold=False,font="Times New Roman"):
    if name not in doc.styles: doc.styles.add_style(name,WD_STYLE_TYPE.PARAGRAPH)
    s=doc.styles[name]
    set_font(s,font,size,bold)
    s.paragraph_format.space_before=Pt(before)
    s.paragraph_format.space_after=Pt(after)
    s.paragraph_format.line_spacing=1.10
    s.paragraph_format.widow_control=True
    s.paragraph_format.keep_together=False
    s.paragraph_format.keep_with_next=False
    s.paragraph_format.alignment=WD_ALIGN_PARAGRAPH.LEFT
    ppr=s.element.get_or_add_pPr()
    for name in ("pBdr","ind","pageBreakBefore"):
        for node in list(ppr.findall(qn("w:"+name))): ppr.remove(node)
    return s

def new_doc(title_text):
    d=Document(project/"manuscripts"/"conference"/"EduAI2027_Meco_Extended_Abstract.docx")
    for child in list(d.element.body):
        if child.tag!=qn("w:sectPr"): d.element.body.remove(child)
    sec=d.sections[0]
    sec.page_height=Inches(11);sec.page_width=Inches(8.5)
    sec.left_margin=Inches(.86);sec.right_margin=Inches(.86)
    sec.top_margin=Inches(.72);sec.bottom_margin=Inches(.73)
    sec.header_distance=Inches(.25);sec.footer_distance=Inches(.29)
    for part in [sec.header,sec.footer]:
        for par in part.paragraphs: par.clear()
    d.core_properties.title=title_text
    d.core_properties.author="Gülsüm Meço"
    d.core_properties.last_modified_by="Gülsüm Meço"
    d.core_properties.comments=""
    d.core_properties.subject="EduAI2027 International Conference on Artificial Intelligence and Education"
    style(d,"Normal",11.5,6)
    st=style(d,"Title",16,7,bold=True);st.paragraph_format.keep_with_next=True
    st.paragraph_format.line_spacing=1.04
    st=style(d,"Heading 1",13,4,8,True);st.paragraph_format.keep_with_next=True
    style(d,"Author line",11.5,2,bold=True)
    style(d,"Affiliation line",10.5,5)
    style(d,"Keyword line",9.5,7)
    style(d,"Figure note",9.5,1)
    style(d,"Conference reference",9.5,3)
    style(d,"Response intro",11.5,8)
    n=sec.footer.paragraphs[0]
    n.alignment=WD_ALIGN_PARAGRAPH.RIGHT
    run=n.add_run();run.font.name="Times New Roman";run.font.size=Pt(9)
    field=OxmlElement("w:fldSimple");field.set(qn("w:instr"),"PAGE")
    rr=OxmlElement("w:r");tt=OxmlElement("w:t");tt.text="1";rr.append(tt);field.append(rr)
    n._p.append(field)
    return d

def ptext(d,text,sty="Normal"):
    p=d.add_paragraph(style=sty)
    pat=r"(Twenty Thousand Leagues under the Sea|Nautilus)"
    for part in re.split(pat,text):
        if not part: continue
        run=p.add_run(part)
        if re.fullmatch(pat,part): run.italic=True
    return p

def reference(d,text):
    p=d.add_paragraph(style="Conference reference")
    mark={
       "Bowen":"Qualitative Research Journal, 9",
       "Ministry":"Türkiye Yüzyılı Maarif Modeli Fen Bilimleri Dersi Öğretim Programı",
       "Nelson":"Sociological Methods & Research, 49",
       "Verne":"Twenty thousand leagues under the sea",
    }[text.split()[0].strip(",")]
    before,after=text.split(mark,1)
    p.add_run(before);p.add_run(mark).italic=True;p.add_run(after)
    p.paragraph_format.left_indent=Inches(.20)
    p.paragraph_format.first_line_indent=Inches(-.20)
    p.paragraph_format.keep_together=True

def make_article():
    d=new_doc(title)
    p=ptext(d,title,"Title")
    p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    for txt,st in [("Gülsüm Meço","Author line"),("Sakarya University, Türkiye  ·  ORCID 0000-0003-4069-5970","Affiliation line")]:
        par=d.add_paragraph(txt,style=st);par.alignment=WD_ALIGN_PARAGRAPH.CENTER
    keywords=d.add_paragraph(style="Keyword line")
    keywords.add_run("Keywords  ").bold=True
    keywords.add_run("Qualitative document analysis, natural language processing, artificial intelligence, science education, curriculum alignment")
    for idx,group in enumerate(pages):
        for index,(kind,txt) in enumerate(group):
            if kind=="p": ptext(d,txt)
            else:
                par=d.add_paragraph(txt,style="Heading 1")
                if idx and index==0:
                    par.paragraph_format.page_break_before=True
                    par.paragraph_format.space_before=Pt(0)
        if idx==1:
            # The eight-row graphic is also available in full resolution in the supplement.
            p=d.add_paragraph()
            p.paragraph_format.space_before=Pt(3);p.paragraph_format.space_after=Pt(4)
            p.paragraph_format.keep_with_next=True
            p.alignment=WD_ALIGN_PARAGRAPH.CENTER
            pic=p.add_run().add_picture(str(project/"figures/supplement/Figure_1_Workflow.png"),width=Inches(6.52))
            pic._inline.docPr.set("descr","Eight stages linking source acquisition, paragraph preparation, lexical processing, screening, pilot coding, AI review, curriculum review and reporting to the retained records.")
            c=d.add_paragraph(style="Figure note")
            c.add_run("Figure 1. ").bold=True
            c.add_run("From the source text to an auditable coding decision.")
            c.alignment=WD_ALIGN_PARAGRAPH.CENTER
    d.add_paragraph("References",style="Heading 1")
    for ref in refs:reference(d,ref)
    d.save(abstract_path)

def make_letter():
    d=new_doc("Response to reviewers")
    d.add_paragraph("Response to reviewers",style="Title")
    p=d.add_paragraph(style="Affiliation line")
    p.add_run("EduAI2027  ·  Submission 13803  ·  Gülsüm Meço")
    ptext(d,title,"Response intro")
    ptext(d,"Dear Editors and Reviewers,")
    ptext(d,"Thank you for the comments on this extended abstract. I have revised the opening and conclusion to state the contribution more precisely. I propose a procedure that science educators can apply to another document and illustrate how to trace a decision from a keyword hit to its interpretation and possible curricular use.")
    d.add_paragraph("Reviewer 1",style="Heading 1")
    ptext(d,"The supplement contains my original preprocessing notebook, the four instructions reported in Turkish with English translations, the coding criteria, paragraph-level results, and Python code that recalculates the reported figures. An additional script and example dictionary allow a reader to try the search and sampling steps on another corpus. I distinguish this reference implementation from the historical analysis. The records contain observed term hits but do not establish the complete original search dictionary, downstream search script, or verbatim contextual prompt log.")
    ptext(d,"I label the whole-corpus distribution as preliminary and identify the source of each code. The curriculum analysis distinguishes the unit-level search from contextual ratings for four selected outcomes. The methodology figure and both supplementary results figures now have English labels. The paragraph sample and limits of single-researcher review are explicit.")
    d.add_paragraph("Reviewer 2",style="Heading 1")
    ptext(d,"I connect qualitative document analysis with computational retrieval and explain why a word match, the scientific function of a passage, and the action required by a learning outcome require separate judgments. The method section identifies the software, sampling rule, and evidence required for each code. Examples illustrate the boundary between a narrative mention and a scientific explanation.")
    ptext(d,"The 58% figure is the proportion of rule-based pre-codes retained in the final contextual decisions for 50 pilot paragraphs. A disagreement identifies a passage worth rereading. It cannot establish independent human agreement or the accuracy of labels for the full novel. The revision reports how the pilot was used, and identifies independent coding of a larger sample as a test for future applications.")
    d.add_paragraph("Reviewer 3",style="Heading 1")
    ptext(d,"Thank you for recognizing the value of a workflow accessible to educators. I retained the practical sequence and clarified which tasks Python performed and where the researcher made an interpretive decision. The study illustrates the automation of preliminary screening. It did not record analysis time, so I have limited the workload claim to the specific tasks automated.")
    ptext(d,"Gülsüm Meço")
    d.save(letter_path)

make_article()
make_letter()
