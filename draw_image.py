"""Render the news image at 2x resolution, then downsample for clean edges."""
from PIL import Image, ImageDraw, ImageFont
import os

S = 2
W = H = 1024
FONT_B = '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'
FONT_R = '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'
im = Image.new('RGB', (W*S, H*S), '#F4EFE3')
d = ImageDraw.Draw(im)

def yy(v): return v-16 if 176 <= v < 970 else v
def xy(v): return int(round(v*S))
def box(coords):
    return (xy(coords[0]),xy(yy(coords[1])),xy(coords[2]),xy(yy(coords[3])))
def font(path, size): return ImageFont.truetype(path, xy(size))
def text(x, y, value, f, fill, anchor=None):
    d.text((xy(x), xy(yy(y))), value, font=f, fill=fill, anchor=anchor)
def line(points, fill, width): d.line([(xy(x),xy(yy(y))) for x,y in points], fill=fill, width=xy(width))
def assert_lines(lines, f, width, name):
    for i, value in enumerate(lines):
        actual=d.textlength(value,font=f)
        assert actual <= xy(width), f'{name} line {i+1} exceeds {width}px: {actual/S:.2f}px'
def draw_lines(lines, x,y,f,fill,leading):
    for v in lines:
        text(x,y,v,f,fill); y += leading

# Masthead
text(48,10,'THE DAY IN ONE PICTURE',font(FONT_B,26),'#D9A441')
text(46,38,'20 NOVEMBER 2026',font(FONT_B,88),'#FFFFFF')
text(48,126,'Friday · World news of 20 November 2026, summed up in one image',font(FONT_R,25),'#E8EDF4')
d.rectangle(box((0,0,1024,160)),fill='#152A44')
# Repaint masthead over the navy band (the background is cream elsewhere).
text(48,10,'THE DAY IN ONE PICTURE',font(FONT_B,26),'#D9A441')
text(46,38,'20 NOVEMBER 2026',font(FONT_B,88),'#FFFFFF')
text(48,126,'Friday · World news of 20 November 2026, summed up in one image',font(FONT_R,25),'#E8EDF4')
d.rectangle(box((0,176,1024,181)),fill='#C9982F')

# Hero band
d.rectangle(box((0,181,1024,413)),fill='#8E2B27')
hero_chip='CONFLICT · RIYADH'; hfchip=font(FONT_B,23)
def chip(label,x,y,color,size=17):
    f=font(FONT_B,size); tw=d.textlength(label,font=f)/S
    d.rounded_rectangle(box((x,y,x+tw+20,y+23)),radius=xy(5),fill=color)
    text(x+10,y+2,label,f,'#FFFFFF')
    return tw+20
chip(hero_chip,48,199,'#8E2B27',23)
hero_h=['Houthi Missile Damages',"Riyadh's Tallest Tower"]
hero_b=['The strike blows out windows across eight floors','of the PIF tower in the city\'s financial district.']
f=font(FONT_B,46); assert_lines(hero_h,f,640,'hero headline'); draw_lines(hero_h,48,232,f,'#FFFFFF',54)
f=font(FONT_R,22); assert_lines(hero_b,f,640,'hero body'); draw_lines(hero_b,48,348,f,'#F7E8E6',29)

# Right-side city and PIF tower illustration
for x,w,h in [(700,38,78),(741,44,112),(790,30,62),(881,39,96),(925,44,74),(973,30,118),(765,20,84),(854,22,63)]:
    d.rectangle(box((x,397-h,x+w,397)),fill='#7A241F')
for x,y in [(708,333),(720,350),(749,309),(775,359),(892,332),(908,356),(943,318),(982,345),(858,370)]:
    d.ellipse(box((x,y,x+3,y+3)),fill='#D98E4A')
# Tower outline and tapered crown
d.polygon([tuple(map(xy,p)) for p in [(800,397),(800,244),(812,217),(864,217),(876,244),(876,397)]],fill='#5E1B18',outline='#3F1210')
d.rectangle(box((800,244,876,397)),fill='#5E1B18',outline='#3F1210',width=xy(2))
d.polygon([tuple(map(xy,p)) for p in [(800,244),(812,217),(864,217),(876,244)]],fill='#5E1B18',outline='#3F1210')
# Arched crown opening
d.pieslice(box((822,235,854,285)),180,360,fill='#8E2B27')
d.rectangle(box((822,260,854,285)),fill='#8E2B27')
# Five columns of windows, fourteen floors; middle floors show impact damage.
for row in range(14):
    for col in range(5):
        x=807+col*13; y=253+row*10
        if 5 <= row <= 12:
            color='#2A0E0C' if (row*3+col*7)%10 < 4 else '#FFB84D'
        else: color='#C97B3D'
        d.rectangle(box((x,y,x+6,y+4)),fill=color)
line([(808,304),(821,311),(816,319),(831,326),(824,334),(841,342)],'#FFE1A0',2)
line([(843,303),(837,313),(849,319),(840,328),(854,337)],'#FFE1A0',2)
for pts in [[(813,350),(818,355),(811,358)],[(831,343),(836,349),(829,351)],[(851,355),(856,361),(849,362)],[(866,342),(870,347),(864,349)],[(839,367),(844,372),(837,373)]]:
    d.polygon([tuple(map(xy,p)) for p in pts],fill='#FFC46B')
# Missile, dotted parallel trails, and impact burst
line([(968,205),(876,300)],'#F5D98B',6)
d.polygon([tuple(map(xy,p)) for p in [(876,300),(879,288),(887,296)]],fill='#FFE9B8')
for off in [-10,10]:
    pts=[]
    for t in range(0,10):
        x=968-(92*t/10); y=205+(95*t/10)+off
        if t%2==0: pts.append((x,y))
        elif pts: line([pts[-1],(x,y)],'#F5D98B',2); pts=[]
burst=[]
for i in range(24):
    import math
    r=13 if i%2==0 else 6
    a=math.pi*2*i/24
    burst.append((876+math.cos(a)*r,300+math.sin(a)*r))
d.polygon([tuple(map(xy,p)) for p in burst],fill='#FFC46B')
d.ellipse(box((870,294,882,306)),fill='#FFE9B8')

stories=[
 ('UKRAINE · KYIV','#C4502B',['Russian Barrage Damages','Embassies in Kyiv'],['A daytime attack shatters windows at the','Austrian and Dutch missions; Brussels',"summons Moscow's envoy."],'ukraine',19),
 ('MARKETS','#2E7D4F',['Anthropic Closes Up 17%','in Nasdaq Debut'],['Shares end near $97, yet US stocks fall','a fifth straight day and Tokyo\'s Nikkei','plunges 4.8%.'],'markets',19),
 ('HEALTH · KENYA','#B23A48',['Kenya Discharges Its','Last Ebola Patient'],['The outbreak is contained 37 days after','the first case was confirmed.'],'health',20),
 ('TECH · ITALY','#7A4FA3',['Italy Fines Meta 805','Million Euros'],['Regulators punish the tech giant over','how it accessed photos on Android phones.'],'tech',20),
 ('ECONOMY','#A87B12',['IMF Warns Global Debt','Nears 100% of GDP'],['Public debt is closing on the size of','the whole world economy, the fund says.'],'economy',20),
 ('ART · NEW YORK','#5B6FA6',['Van Gogh Painting Sells','for Record $190.4M'],['The canvas sets a new auction high for','the artist after a disputed sale.'],'art',20),
]
headline_accents = {
    'MARKETS': {0: [('Anthropic Closes Up ', '#1B2A3B'), ('17%', '#2E7D4F')]},
    'TECH · ITALY': {0: [('Italy Fines Meta ', '#1B2A3B'), ('805', '#7A4FA3')]},
    'ECONOMY': {1: [('Nears ', '#1B2A3B'), ('100%', '#A87B12'), (' of GDP', '#1B2A3B')]},
    'ART · NEW YORK': {1: [('for Record ', '#1B2A3B'), ('$190.4M', '#5B6FA6')]},
}
def draw_icon(kind,x,y,c):
    # Icon coordinate space is exactly 72x72; all marks use Pillow primitives.
    if kind=='ukraine':
        line([(x+6,y+26),(x+36,y+8),(x+66,y+26)],c,5); d.rectangle(box((x+8,y+26,x+64,y+32)),fill=c)
        for xx in [14,33,52]: d.rectangle(box((x+xx,y+36,x+xx+6,y+58)),fill=c)
        d.rectangle(box((x+6,y+58,x+66,y+64)),fill=c); line([(x+36,y+8),(x+36,y+1)],'#C9982F',2)
        d.polygon([tuple(map(xy,p)) for p in [(x+36,y+2),(x+49,y+6),(x+36,y+10)]],fill='#C9982F')
        line([(x+55,y+39),(x+51,y+45),(x+57,y+49),(x+53,y+56)],'#FFFFFF',2)
    elif kind=='markets':
        line([(x+10,y+8),(x+10,y+62),(x+64,y+62)],c,5); line([(x+14,y+50),(x+28,y+42),(x+40,y+46),(x+62,y+20)],c,5)
        d.polygon([tuple(map(xy,p)) for p in [(x+62,y+20),(x+51,y+22),(x+59,y+30)]],fill=c)
    elif kind=='health':
        d.ellipse(box((x+10,y+10,x+62,y+62)),outline=c,width=xy(5)); d.rectangle(box((x+31,y+20,x+41,y+52)),fill=c); d.rectangle(box((x+20,y+31,x+52,y+41)),fill=c)
        line([(x+48,y+54),(x+56,y+62),(x+68,y+46)],c,5)
    elif kind=='tech':
        d.rounded_rectangle(box((x+22,y+6,x+50,y+66)),radius=xy(6),outline=c,width=xy(5)); d.ellipse(box((x+28,y+20,x+36,y+28)),fill=c)
        line([(x+26,y+52),(x+36,y+38),(x+42,y+46),(x+46,y+52)],c,4)
        d.ellipse(box((x+41,y+41,x+67,y+67)),fill=c); f=font(FONT_B,20); text(x+54,y+44,'€',f,'#FFFFFF',anchor='mm')
    elif kind=='economy':
        d.arc(box((x+8,y+20,x+64,y+76)),180,360,fill=c,width=xy(5))
        for a in [180,216,252,288,324,360]:
            import math
            rad=math.radians(a); line([(x+36+math.cos(rad)*23,y+48+math.sin(rad)*23),(x+36+math.cos(rad)*28,y+48+math.sin(rad)*28)],c,3)
        line([(x+36,y+48),(x+56,y+30)],c,5); d.ellipse(box((x+32,y+44,x+40,y+52)),fill=c)
    else:
        d.rectangle(box((x+8,y+10,x+64,y+62)),outline=c,width=xy(5)); d.rectangle(box((x+14,y+16,x+58,y+56)),fill='#22355E')
        d.arc(box((x+20,y+25,x+48,y+53)),200,500,fill='#D9A441',width=xy(3)); d.arc(box((x+31,y+20,x+55,y+44)),30,310,fill='#D9A441',width=xy(3))
        for xx,yy in [(23,22),(50,25),(44,48)]: d.ellipse(box((x+xx-2,y+yy-2,x+xx+2,y+yy+2)),fill='#D9A441')
        d.ellipse(box((x+30,y+30,x+44,y+44)),fill='#D9A441'); d.ellipse(box((x+35,y+27,x+49,y+41)),fill='#22355E')

for i,(label,color,heads,bodies,kind,body_size) in enumerate(stories):
    cx=28+(i%2)*496; cy=423+(i//2)*182
    d.rounded_rectangle(box((cx,cy,cx+472,cy+182)),radius=xy(10),fill='#FFFFFF',outline='#D9D2C2',width=xy(1))
    d.rectangle(box((cx,cy,cx+8,cy+182)),fill=color)
    chip(label,cx+26,cy+9,color,17)
    icx,icy=cx+384,cy+12
    draw_icon(kind,icx,icy,color)
    # The text lane runs from x+26 to the icon frame at x+384 (358 px).
    fh=font(FONT_B,28); assert_lines(heads,fh,358,label+' headline')
    hy=cy+37
    for hi,headline in enumerate(heads):
        segments=headline_accents.get(label,{}).get(hi,[(headline,'#1B2A3B')])
        hx=cx+26
        assert ''.join(part for part,_ in segments)==headline
        for part,ink in segments:
            text(hx,hy,part,fh,ink)
            hx += d.textlength(part,font=fh)/S
        hy += 32
    actual_body_size=body_size+2
    fb=font(FONT_R,actual_body_size); assert_lines(bodies,fb,432,label+' body'); draw_lines(bodies,cx+26,cy+100,fb,'#33475B',25 if body_size==19 else 27)

# Footer
d.rectangle(box((0,970,1024,1024)),fill='#152A44')
text(28,985,'20 NOVEMBER 2026 — ONE DAY OF WORLD NEWS',font(FONT_B,20),'#FFFFFF')
text(976,985,"Compiled from the day's reporting",font(FONT_R,20),'#C9D4E2',anchor='ra')

out_dir=os.environ.get('MAKEFUN_OUTPUT_DIR',os.path.dirname(os.path.abspath(__file__)))
os.makedirs(out_dir,exist_ok=True)
final=im.resize((1024,1024),Image.Resampling.LANCZOS)
entry_path=os.path.join(out_dir,'entry.png')
final.save(entry_path,format='PNG',optimize=True)
final.resize((300,300),Image.Resampling.LANCZOS).save(os.path.join(out_dir,'preview300.png'),format='PNG',optimize=True)
print(f'All text width assertions passed; wrote {entry_path}')
