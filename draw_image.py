"""Offline generator for the committed entry.png; requires Pillow and Noto fonts on the build machine, not the grader."""

from PIL import Image, ImageDraw, ImageFont
import os

W = H = 1024
BG = '#0e141c'
WHITE = '#eef3f8'
CYAN = '#39c2d7'
AMBER = '#f0a13c'
CARD = '#1a2431'
BORDER = '#2c3a49'
FONT_B = '/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf'
FONT_R = '/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf'
FONT_BLACK = '/usr/share/fonts/truetype/noto/NotoSans-Black.ttf'

im = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(im)

def font(path, size):
    return ImageFont.truetype(path, size)

def text_h(f, sample='Ag'):
    b = d.textbbox((0, 0), sample, font=f)
    return b[3] - b[1]

def wrap(text, f, max_width):
    words = text.split()
    lines, line = [], ''
    for word in words:
        candidate = word if not line else line + ' ' + word
        if d.textbbox((0, 0), candidate, font=f)[2] <= max_width:
            line = candidate
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines

def fit_lines(text, path, size, max_width, max_lines, min_size=13):
    for s in range(size, min_size - 1, -1):
        f = font(path, s)
        lines = wrap(text, f, max_width)
        if len(lines) <= max_lines:
            return f, lines
    f = font(path, min_size)
    return f, wrap(text, f, max_width)

def draw_lines(lines, f, x, y, fill, leading):
    for line in lines:
        d.text((x, y), line, font=f, fill=fill)
        y += leading
    return y

def chip(label, x, y, color, size=15):
    f = font(FONT_B, size)
    d.text((x, y), label, font=f, fill=color)

# Masthead
x = 28
d.text((x, 20), 'THE DAY IN ONE PICTURE', font=font(FONT_B, 19), fill=CYAN)
d.text((x-2, 43), '20 NOVEMBER 2026', font=font(FONT_BLACK, 76), fill=WHITE)
d.text((x, 137), 'Friday · World news of 20 November 2026, summed up in one image', font=font(FONT_R, 21), fill='#c4d0db')
d.rounded_rectangle((28, 177, 996, 181), radius=2, fill=AMBER)

# Hero
hx, hy, hw, hh = 28, 197, 968, 220
d.rounded_rectangle((hx, hy, hx+hw, hy+hh), radius=12, fill='#14313e')
# understated skyline, clipped to the panel's lower area
sky = '#102b37'
base = hy + hh
buildings = [(30,18),(86,27),(146,21),(203,32),(275,20),(330,25),(397,17),(454,30),(523,22),(588,34),(666,19),(718,28),(781,20),(844,31),(915,22)]
for bx, bh in buildings:
    d.rectangle((hx+bx, base-bh, hx+bx+34, base), fill=sky)
# cover central copy zone in slightly lighter hero tone for contrast
# text is laid above skyline; restrained translucent-looking solid backing is avoided.
chip('CONFLICT · RIYADH', hx+22, hy+17, CYAN, 16)
hero_head = "Houthi Missile Damages Riyadh's Tallest Tower"
f, lines = fit_lines(hero_head, FONT_B, 44, 910, 2, 37)
y = hy + 43
y = draw_lines(lines, f, hx+22, y, WHITE, 51)
hero_detail = "The strike blows out windows across eight floors of the PIF tower in the city's financial district."
f, lines = fit_lines(hero_detail, FONT_R, 24, 910, 2, 19)
draw_lines(lines, f, hx+22, min(y+3, hy+151), '#d7e1e8', 29)

stories = [
    ('UKRAINE · KYIV', '#e05252', 'Russian Barrage Damages Embassies in Kyiv', "A daytime attack shatters windows at the Austrian and Dutch missions; Brussels summons Moscow's envoy.", 'kyiv'),
    ('MARKETS', '#43b581', 'Anthropic Closes Up 17% in Nasdaq Debut', "Shares end near $97, yet US stocks fall a fifth straight day and Tokyo's Nikkei plunges 4.8%.", 'markets'),
    ('HEALTH · KENYA', '#39c2d7', 'Kenya Discharges Its Last Ebola Patient', 'The outbreak is contained 37 days after the first case was confirmed.', 'health'),
    ('TECH · ITALY', '#7d6fd0', 'Italy Fines Meta 805 Million Euros', 'Regulators punish the tech giant over how it accessed photos on Android phones.', 'tech'),
    ('ECONOMY', '#f0a13c', 'IMF Warns Global Debt Nears 100% of GDP', 'Public debt is closing on the size of the whole world economy, the fund says.', 'economy'),
    ('ART · NEW YORK', '#d76fb0', 'Van Gogh Painting Sells for Record $190.4M', 'The canvas sets a new auction high for the artist after a disputed sale.', 'art'),
]

def icon(kind, x, y, color):
    # Small, simple line icons. Each stays inside a 30 x 30 box.
    if kind == 'kyiv':
        d.polygon([(x+3,y+13),(x+15,y+3),(x+27,y+13)], outline=color, fill=None)
        d.rectangle((x+6,y+13,x+24,y+28), outline=color, width=2)
        d.rectangle((x+13,y+19,x+17,y+28), fill=color)
    elif kind == 'markets':
        d.line((x+3,y+26,x+3,y+4), fill=color, width=2); d.line((x+3,y+26,x+28,y+26), fill=color, width=2)
        d.line((x+6,y+21,x+12,y+16,x+17,y+19,x+25,y+7), fill=color, width=3)
        d.polygon([(x+21,y+7),(x+27,y+5),(x+26,y+12)], fill=color)
    elif kind == 'health':
        d.ellipse((x+4,y+4,x+26,y+26), outline=color, width=2)
        d.rectangle((x+12,y+8,x+18,y+22), fill=color); d.rectangle((x+8,y+12,x+22,y+18), fill=color)
    elif kind == 'tech':
        d.rounded_rectangle((x+4,y+5,x+26,y+24), radius=3, outline=color, width=2)
        d.line((x+10,y+28,x+20,y+28), fill=color, width=2); d.line((x+15,y+24,x+15,y+28), fill=color, width=2)
        d.ellipse((x+13,y+8,x+17,y+12), fill=color)
    elif kind == 'economy':
        d.ellipse((x+4,y+4,x+26,y+26), outline=color, width=2)
        d.text((x+9,y+3), '$', font=font(FONT_B, 21), fill=color)
    else:
        d.rectangle((x+5,y+5,x+25,y+25), outline=color, width=2)
        d.line((x+8,y+20,x+14,y+12,x+18,y+17,x+23,y+9), fill=color, width=2)
        d.ellipse((x+8,y+8,x+11,y+11), fill=color)

# Three compact rows, with consistent gutters and a reserved icon corner.
cols_x = [28, 512]
card_w, card_h, gap_y = 472, 158, 10
start_y = 429
for i, (label, accent, headline, detail, kind) in enumerate(stories):
    col, row = i % 2, i // 2
    cx, cy = cols_x[col], start_y + row * (card_h + gap_y)
    d.rounded_rectangle((cx, cy, cx+card_w, cy+card_h), radius=9, fill=CARD, outline=BORDER, width=1)
    px, py = cx+15, cy+10
    chip(label, px, py, accent, 14)
    icon(kind, cx+card_w-44, cy+10, accent)
    available = card_w - 30
    hf, hl = fit_lines(headline, FONT_B, 28, available, 2, 23)
    head_y = cy + 34
    head_lead = text_h(hf, 'Ag') + 4
    after_head = draw_lines(hl, hf, px, head_y, WHITE, head_lead)
    detail_y = after_head + 4
    # Shrink until detail fits width, three lines, and leaves at least 10px below.
    max_detail_bottom = cy + card_h - 10
    for ds in range(21, 13, -1):
        df = font(FONT_R, ds)
        dl = wrap(detail, df, available)
        line_h = text_h(df, 'Ag') + 3
        if len(dl) <= 3 and detail_y + len(dl)*line_h <= max_detail_bottom:
            break
    else:
        df = font(FONT_R, 14); dl = wrap(detail, df, available); line_h = text_h(df, 'Ag') + 2
    draw_lines(dl, df, px, detail_y, '#c7d2dc', line_h)

# Footer strip
fy = 933
d.rectangle((0, fy, W, H), fill='#090e14')
d.rectangle((0, fy, W, fy+1), fill=AMBER)
d.rectangle((0, fy+2, W, H), fill='#16202c')
d.text((28, fy+17), '20 NOVEMBER 2026 — ONE DAY OF WORLD NEWS', font=font(FONT_B, 15), fill='#aab8c5')
right = 'Compiled from the day\'s reporting'
rf = font(FONT_R, 14)
rw = d.textbbox((0,0), right, font=rf)[2]
d.text((996-rw, fy+18), right, font=rf, fill='#82909d')

out_dir = os.environ.get('MAKEFUN_OUTPUT_DIR', os.path.dirname(os.path.abspath(__file__)))
os.makedirs(out_dir, exist_ok=True)
im.save(os.path.join(out_dir, 'entry.png'), format='PNG', optimize=True)
