from pathlib import Path
import re
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4

BASE = Path(__file__).resolve().parent
OUT = BASE.parent / 'pdf' / 'exposition_attribution_audit.pdf'
OUT.parent.mkdir(parents=True, exist_ok=True)

for name, file in [('Body','georgia.ttf'),('BodyBold','georgiab.ttf'),('BodyItalic','georgiai.ttf'),('Sans','arial.ttf'),('SansBold','arialbd.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(Path('C:/Windows/Fonts') / file)))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='BodyBold',italic='BodyItalic',boldItalic='BodyBold')
pdfmetrics.registerFontFamily('Sans',normal='Sans',bold='SansBold',italic='Sans',boldItalic='SansBold')

NAVY = colors.HexColor('#17354B')
BLUE = colors.HexColor('#176082')
INK = colors.HexColor('#242C32')
GREY = colors.HexColor('#5D6B75')
LIGHT = colors.HexColor('#D4E0E8')
styles = {
    'title': ParagraphStyle('title',fontName='SansBold',fontSize=25,leading=29,textColor=NAVY,spaceAfter=10),
    'subtitle': ParagraphStyle('subtitle',fontName='Sans',fontSize=10,leading=14,textColor=GREY,spaceAfter=21),
    'h1': ParagraphStyle('h1',fontName='SansBold',fontSize=15,leading=19,textColor=NAVY,spaceBefore=17,spaceAfter=9,keepWithNext=True),
    'h2': ParagraphStyle('h2',fontName='SansBold',fontSize=10.3,leading=14,textColor=NAVY,spaceBefore=8,spaceAfter=4,keepWithNext=True),
    'body': ParagraphStyle('body',fontName='Body',fontSize=10.15,leading=13.8,textColor=INK,spaceAfter=6,allowWidows=0,allowOrphans=0),
    'small': ParagraphStyle('small',fontName='Sans',fontSize=8.5,leading=11.5,textColor=GREY,spaceAfter=5,wordWrap='LTR'),
    'url': ParagraphStyle('url',fontName='Sans',fontSize=8.7,leading=12,textColor=BLUE,spaceAfter=4,splitLongWords=True),
    'quote': ParagraphStyle('quote',fontName='BodyItalic',fontSize=10.15,leading=14.5,textColor=NAVY,leftIndent=14,rightIndent=12,spaceBefore=5,spaceAfter=9,borderPadding=9,backColor=colors.HexColor('#F0F5F8')),
}

def clean(s):
    return s.replace('\u2013','-').replace('\u2014','-').replace('\u2011','-').replace('\u2010','-').replace('\u2019',"'").replace('\u2018',"'").replace('\u201c','"').replace('\u201d','"').replace('\u2026','...')

def markup(s):
    parts=re.split(r'(https?://[^\s]+)',clean(s))
    return ''.join(f'<link href="{escape(p)}" color="#176082">{escape(p)}</link>' if p.startswith('http') else escape(p) for p in parts)

def para(s,kind='body'):
    return Paragraph(markup(s),styles[kind])

class AuditDoc(SimpleDocTemplate):
    def afterFlowable(self,flowable):
        if isinstance(flowable,Paragraph) and flowable.style.name=='h1':
            key='section-'+str(self.seq.nextf('section'))
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(flowable.getPlainText(),key,0,False)

class PageCanvas(canvas.Canvas):
    def __init__(self,*args,**kwargs):
        canvas.Canvas.__init__(self,*args,**kwargs)
        self.saved=[]
    def showPage(self):
        self.saved.append(dict(self.__dict__))
        self._startPage()
    def save(self):
        total=len(self.saved)
        for state in self.saved:
            self.__dict__.update(state)
            self.saveState()
            w,h=A4
            self.setStrokeColor(LIGHT)
            self.setLineWidth(.5)
            self.line(49,44,w-49,44)
            self.setFont('Sans',8)
            self.setFillColor(GREY)
            self.drawString(49,30,'EXPOSITION & ATTRIBUTION AUDIT  |  14 NOVEMBER 2026')
            self.drawRightString(w-49,30,f'{self._pageNumber} / {total}')
            if self._pageNumber>1:
                self.setFont('Sans',8)
                self.drawString(49,h-31,'Lai / Fauzan exposition: source and wording review')
                self.line(49,h-39,w-49,h-39)
            self.restoreState()
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

source=clean((BASE/'audit.txt').read_text(encoding='utf-8'))
source=source.replace('Exact audited copies are in snapshots/ beside this report.','Exact audited copies accompany the text audit in output/exposition-audit/snapshots/.')
source=source.replace('Evidence files\n\n','Evidence files\n\nThe following paths are relative to output/exposition-audit/ in the project workspace.\n\n')
blocks=source.strip().split('\n\n')
story=[para('Exposition and<br/>attribution audit'.replace('<br/>','\n'),'title')]
# Use an explicit line break in the title only.
story[0]=Paragraph('Exposition and<br/>attribution audit',styles['title'])
story.append(para('14 November 2026 | Audit of two completed PDFs | Public-source review','subtitle'))

headings={'Conclusion','Scope and versions','Page-by-page attribution map','Most important additional sources','Sources already credited','Hexagon and additional ai.vixra matches','Other arXiv and formalization parallels inspected','Suggested attribution changes (not applied to the PDFs)','Method, negative results and limits','Evidence files'}

for block in blocks[2:]:
    block=block.strip()
    if block in headings:
        if block in {'Page-by-page attribution map','Most important additional sources','Suggested attribution changes (not applied to the PDFs)'}:
            story.append(PageBreak())
        story.append(para(block,'h1'))
        continue
    if re.match(r'^[AB] p\d,',block):
        for item in re.split(r'\n(?=[AB] p\d,)',block):
            lines=item.splitlines()
            story.append(KeepTogether([para(lines[0],'h2'),para(' '.join(x.strip() for x in lines[1:]))]))
        continue
    if re.match(r'^\d+(?:-\d+)?\. ',block):
        lines=block.splitlines()
        entry=[para(lines[0],'h2')]
        prose=[]
        def flush():
            if prose:
                entry.append(para(' '.join(prose)))
                prose.clear()
        for line in lines[1:]:
            line=line.strip()
            if line.startswith('http'):
                flush()
                entry.append(para(line,'url'))
            else:
                prose.append(line)
        flush()
        story.append(KeepTogether(entry))
        continue
    if block.startswith(('A. Parallel','B. Why')):
        lines=block.splitlines()
        story.append(KeepTogether([para(lines[0],'h2'),para(lines[1],'small'),para(lines[2],'small')]))
        continue
    if block.startswith('Chat inspected:'):
        story.append(para(block.replace('\n',' '),'small'))
        continue
    if block.startswith('Priority 2:'):
        lines=block.splitlines()
        story.append(para(lines[0]))
        story.append(para(lines[1].strip(),'quote'))
        if len(lines)>2: story.append(para(' '.join(lines[2:])))
        continue
    if block.startswith('snapshots/manifest.json:'):
        story.append(Paragraph('<br/>'.join(markup(line) for line in block.splitlines()),styles['small']))
        continue
    story.append(para(' '.join(x.strip() for x in block.splitlines())))

doc=AuditDoc(str(OUT),pagesize=A4,rightMargin=49,leftMargin=49,topMargin=54,bottomMargin=59,
    title='Exposition and attribution audit',author='Codex',subject='Public-source attribution audit of Lai/Fauzan exposition PDFs')
doc.build(story,canvasmaker=PageCanvas)
print(OUT)
