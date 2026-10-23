"""Editable book-cover composition using the supplied exact logo and portrait assets.
PDF clipping frames the supplied art; it does not redraw or retouch the brand marks.
"""
from pathlib import Path
import json,html,argparse
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output-dir',required=True,type=Path)
parser.add_argument('--asset-dir',required=True,type=Path,help='Directory of exact assets restored from the saved v0.4 package')
parser.add_argument('--art-dir',type=Path,help='Directory with the six approved artwork PNGs restored from the saved v0.4 package')
args=parser.parse_args()
OUTPUT=args.output_dir.resolve();OUTPUT.mkdir(parents=True,exist_ok=True)
ASSETS=args.asset_dir.resolve()
ART=args.art_dir.resolve() if args.art_dir else ASSETS
manifest=json.loads((ROOT/'references/approved-assets.json').read_text())
import hashlib
for row in manifest['assets']:
    source=ASSETS/Path(row['path']).name
    if not source.is_file() or hashlib.sha256(source.read_bytes()).hexdigest()!=row['sha256']:
        raise SystemExit('Approved bundled asset missing or changed: '+row['path'])
for row in manifest.get('archived_cover_art',[]):
    source=ART/Path(row['path']).name
    if not source.is_file() or hashlib.sha256(source.read_bytes()).hexdigest()!=row['sha256']:
        raise SystemExit('Approved cover art missing or changed: '+str(source)+'; restore the saved v0.4 package using references/approved-assets.json')
for name,file in [('Sans','DejaVuSans.ttf'),('SansBold','DejaVuSans-Bold.ttf'),('Serif','DejaVuSerif.ttf'),('SerifBold','DejaVuSerif-Bold.ttf')]:
    pdfmetrics.registerFont(TTFont(name,'/usr/share/fonts/truetype/dejavu/'+file))
INK=HexColor('#060708');WHITE=HexColor('#F7F4EA');GOLD=HexColor('#D8AF55');MUTED=HexColor('#C4C3BC')
W,H=432,648
COPY={
 'ADULT':dict(title='The Architecture of Integrity',age='ADULT EDITION | 18+',accent='#D8AF55',hook='What does it cost to keep a lie alive?',
  blurb="A lie can begin in embarrassment, instinct, fear, or the wish to belong. The cost can keep growing long after the moment has passed. Drawing on Major Dream Williams's lived reflections, this collection explores the space between a mistake and its cover-up, between helping someone and carrying their consequences, and between forgiveness and restored trust.",
  promise='Ten lessons in truth, accountability, boundaries and personal governance. Stories, difficult questions and practical challenges invite you to examine your own choices without pretending every situation has a simple answer.',
  details='The Lie Tax | Own Your Actions | Repairing Trust',close='Honesty with discernment. Accountability with a future.'),
 'TEEN':dict(title='The Integrity Code',age='TEEN EDITION | AGES 13-17',accent='#58B5F4',hook='Who are you when fitting in has a price?',
  blurb="A borrowed jacket. A group-chat rumor. A promise that becomes difficult to keep. Some choices happen fast. What you do afterward can change the story. The Integrity Code explores belonging, peer pressure, friendship, digital identity and the courage to correct what you got wrong.",
  promise='Ten lessons pair original stories with reflection, practical challenges and scenario questions. Learn to notice who carries the cost, respect other people\'s choices, and keep your own privacy and boundaries.',
  details='Think independently | Speak clearly | Respond with effort',close='You do not have to perform a perfect life to practice integrity.'),
 'CHILD':dict(title='The Truth Compass',age='YOUNGER LEARNERS | AGES 7-12',accent='#8AD6A0',hook='A small mistake. A brave next step.',
  blurb="When a cardboard bus gets a bent wheel, a made-up story gives two friends another problem to solve. What happens when they find safe help and work on a repair? The Truth Compass invites young readers into adventures about honesty, courage, kindness and responsibility.",
  promise='Ten adventures include talk-and-draw activities, thoughtful questions and practical challenges. Children can explore the stories without sharing private experiences. Read together or use the age-appropriate prompts for supported learning.',
  details='Pause | Tell someone safe | Help make things better',close='You can tell the truth and keep private information safe.')}

def para(c,text,x,top,width,size=11.2,leading=16,font='Sans',color=WHITE):
    p=Paragraph(html.escape(text),ParagraphStyle('p',fontName=font,fontSize=size,leading=leading,textColor=color))
    _,h=p.wrap(width,1000);p.drawOn(c,x,top-h);return top-h

def framed_asset(c,path,bbox,x,y,w,h):
    """Frame exact source pixels through a PDF clip; preserve the source file."""
    iw,ih=Image.open(path).size;left,top,right,bottom=bbox;bw,bh=right-left,bottom-top
    sx,sy=w/bw,h/bh
    c.saveState();clip=c.beginPath();clip.rect(x,y,w,h);c.clipPath(clip,stroke=0,fill=0)
    c.drawImage(str(path),x-left*sx,y-(ih-bottom)*sy,width=iw*sx,height=ih*sy,mask='auto');c.restoreState()

def logo(c,variant,x,y,size):
    if variant=='A':
        # Transparent supplied MD + woven hat; remove only empty margins by framing.
        framed_asset(c,ASSETS/'MD-Hat-Original.png',(180,45,420,348),x,y,size*240/303,size)
    else:
        framed_asset(c,ASSETS/'MD-Circle-Original.png',(60,15,650,605),x,y,size,size)

def front(c,ed,opt):
    c.drawImage(str(ART/f'{ed}-{opt}-Art.png'),0,0,W,H)
    band=46 if ed=='CHILD' else 32
    c.setFillColor(INK);c.rect(0,H-band,W,band,fill=1,stroke=0)
    size=36 if ed=='CHILD' else 27;y=H-band+(band-size)/2
    logo(c,opt,153,y,size)
    c.setFillColor(GOLD);c.setFont('SansBold',14);c.drawString(193,H-band+band/2+1,'MAIM')
    c.setFillColor(WHITE);c.setFont('Sans',6.7);c.drawString(193,H-band+band/2-9,'MAJOR DREAM')

def back(c,ed,opt):
    d=COPY[ed];accent=HexColor(d['accent']);c.setFillColor(INK);c.rect(0,0,W,H,fill=1,stroke=0)
    # Subtle color bar and rules are layout elements, never additional logos.
    c.setFillColor(accent);c.rect(0,H-5,W,5,fill=1,stroke=0)
    logo(c,opt,35,563,53)
    c.setFillColor(WHITE);c.setFont('SansBold',11.5);c.drawString(108,599,'MAIM INTEGRITY COLLECTION')
    c.setFillColor(accent);c.setFont('Sans',8.8);c.drawString(108,580,d['age'])
    c.setStrokeColor(HexColor('#4C4637'));c.line(35,547,W-35,547)
    top=para(c,d['hook'],35,524,362,22,28,'SerifBold',WHITE)-17
    top=para(c,d['blurb'],35,top,362,11.3,16.8)-14
    top=para(c,d['promise'],35,top,362,11.1,16.5)-13
    top=para(c,d['close'],35,top,362,11.1,16,'Serif',WHITE)
    assert top>231,(ed,opt,top)
    c.setStrokeColor(HexColor('#4C4637'));c.line(35,220,W-35,220)
    # A and B retain the same real portrait, with alternate positions.
    px=35 if opt=='A' else 317;tx=132 if opt=='A' else 35;tw=265 if opt=='A' else 267
    framed_asset(c,ASSETS/'Major-Author-Photo.JPG',(260,100,1120,1230),px,104,80,105)
    top=para(c,'MAJOR DREAM WILLIAMS',tx,207,tw,11,15,'SansBold',accent)-7
    top=para(c,'Entrepreneur, former college basketball athlete and MAIM founder. Major draws on his South Bronx upbringing, Jamaican family roots and lived experience to invite honest conversation about choices, character and responsibility.',tx,top,tw,9.7,14,'Sans',WHITE)
    assert top>104
    logo(c,'B' if opt=='A' else 'A',35,30,36)
    c.setFillColor(MUTED);c.setFont('Sans',8.6);c.drawString(85,55,'MAJOR DREAM / MAIM');c.drawString(85,41,'Integrity Collection')
    c.setStrokeColor(HexColor('#77746C'));c.rect(296,30,101,49,fill=0,stroke=1)
    c.setFont('Sans',8);c.drawCentredString(346.5,58,'ISBN / BARCODE');c.drawCentredString(346.5,44,'SPACE RESERVED')

def pairs():
    for ed in COPY:
        for opt in ['A','B']:
            out=OUTPUT/f'{ed}-{opt}-Front-and-Back.pdf';c=canvas.Canvas(str(out),pagesize=(W,H));c.setTitle(COPY[ed]['title']+f' - Option {opt}, front and back');c.setAuthor('Major Dream Williams');front(c,ed,opt);c.showPage();back(c,ed,opt);c.showPage();c.save();print(out)

def review():
    out=OUTPUT/'MAIM-Integrity-Six-Cover-Pairs-v0.4.pdf';c=canvas.Canvas(str(out),pagesize=(1008,760));c.setTitle('MAIM Integrity - six front and back cover pairs');c.setAuthor('Major Dream Williams')
    for ed in COPY:
        for opt in ['A','B']:
            d=COPY[ed];c.setFillColor(HexColor('#EEEAE0'));c.rect(0,0,1008,760,fill=1,stroke=0);c.setFillColor(INK);c.setFont('SansBold',18);c.drawString(38,722,d['title']+f' | Option {opt}')
            c.setFont('Sans',10.5);c.drawString(38,701,'Existing visual direction retained. Exact supplied Major Dream mark and author photograph.')
            for x,label,fn in [(38,'FRONT',front),(538,'BACK',back)]:
                c.setFont('SansBold',10);c.drawString(x,679,label);c.saveState();c.translate(x,58);c.scale(.92,.92);fn(c,ed,opt);c.restoreState()
            c.setFont('Sans',9.5);c.drawString(38,27,'DRAFT COLLECTION COVERS | Back copy and author bio for review. ISBN, spine, trim and bleed remain pending.')
            c.showPage()
    c.save();print(out)

if __name__=='__main__':pairs();review()
