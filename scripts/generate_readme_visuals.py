"""Generate the SVG assets used by README.md. Run with --check to verify generated files."""

import argparse
import math
import sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets' / 'chrome-ruby'
THEMES = {
    'dark': dict(bg='#090b10', panel='#12151c', line='#343b47', ink='#f0f3f8', muted='#a6afbd', ruby='#ff4664', silver='#c7d1df', soft='#202733', navink='#151922'),
    'light': dict(bg='#edf0f4', panel='#fbfcfe', line='#b6bfcb', ink='#1c2432', muted='#515e70', ruby='#b51536', silver='#4d607a', soft='#dbe2eb', navink='#151922'),
}

def t(x, y, s, size=18, c='ink', weight=400, extra=''):
    fill = 'url(#cr-type)' if c == 'ink' and size >= 32 and weight >= 600 else f'var(--{c})'
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" {extra}>{escape(s)}</text>'

def lines(x, y, ss, size=18, c='muted', step=26, weight=400):
    return ''.join((t(x, y + i * step, s, size, c, weight) for i, s in enumerate(ss)))

def label(x, y, s, c='muted', size=12):
    return t(x, y, s, size, c, 500, 'class="mono" letter-spacing="1.1"')

def panel(w, h, c='bg'):
    outline = f'M18 1H{w-35}L{w-1} 35V{h-18}Q{w-1} {h-1} {w-18} {h-1}H35L1 {h-35}V18Q1 1 18 1Z'
    s = f'<path d="{outline}" fill="url(#cr-panel)" stroke="url(#cr-edge)" stroke-opacity=".55" stroke-width="1.3"/><path d="{outline}" fill="url(#cr-grain)"/>'
    s += f'<path d="M22 3H{w-39}M3 26V{h-42}" fill="none" stroke="var(--silver)" stroke-opacity=".15"/>'
    s += f'<path d="M{w-32} 8L{w-8} 32M8 {h-32}L32 {h-8}" stroke="var(--ruby)" stroke-opacity=".7" stroke-width="2"/>'
    s += f'<path d="M36 {h-2}H{w-24}" pathLength="100" class="cr-trace" stroke="var(--ruby)" stroke-opacity=".7" stroke-width="1.6"/>'
    return s

def rule(x, y, xx):
    return f'<path d="M{x} {y}H{xx}" stroke="var(--line)"/>'

def arrow(x, y, c='muted'):
    return f'<path d="M{x} {y + 12}L{x + 12} {y}M{x} {y}H{x + 12}V{y + 12}" fill="none" stroke="var(--{c})" stroke-width="1.7"/>'

def star(x, y, r=16, c='ruby', moving=False):
    s = f'<g transform="translate({x} {y})"><g class="{ "star-spin" if moving else ""}">'
    for angle in range(0, 360, 90):
        s += f'<path transform="rotate({angle})" d="M0 {-r}Q{r*.95} {-r*.85} {r*.43} {-r*.15}L{r*.12} {r*.15}Q{r*.45} {-r*.64} 0 {-r}Z" fill="url(#cr-metal)"/>'
    return s + f'</g><circle r="{r*.16}" fill="var(--ruby)"/></g>'
CSS = '''text{font-family:Arial,"Segoe UI",sans-serif}.mono{font-family:Consolas,"Courier New",monospace}
.star-spin{animation:cr-spin 12s linear infinite}
.cr-trace{stroke-dasharray:16 4 3 5 2 70;animation:cr-trace 2.2s linear infinite}
.cr-orbit{animation:cr-spin 14s linear infinite}.cr-reverse{animation:cr-spin 19s linear infinite reverse}
.cr-pulse{opacity:.8;animation:cr-pulse 3.2s ease-in-out infinite}
.cr-node{opacity:.65;animation:cr-node 3.2s ease-in-out infinite}
.cr-rise{animation:cr-rise 6.4s ease-in-out infinite}
.cr-lift{animation:cr-lift 6.4s ease-in-out infinite}
.cr-sheen{opacity:0;animation:cr-sheen 6.4s ease-in-out infinite}
.cr-scan{animation:cr-scan 3.2s ease-in-out infinite alternate}
.cr-phase{opacity:0;animation:cr-phase 6.4s linear infinite}.cr-phase:first-child{opacity:1}
.cr-reveal{transform:scaleX(1);animation:cr-reveal 6.4s steps(23,end) infinite}
.cr-caret{transform:translateX(194px);animation:cr-caret 6.4s steps(23,end) infinite}
.cr-wave{transform-box:fill-box;transform-origin:center;animation:cr-wave .8s ease-in-out infinite alternate}
.cr-ripple{transform-box:fill-box;transform-origin:center;opacity:.08;animation:cr-ripple 3.2s ease-out infinite}
@keyframes cr-spin{to{transform:rotate(360deg)}}
@keyframes cr-trace{from{stroke-dashoffset:100}to{stroke-dashoffset:0}}
@keyframes cr-pulse{0%,100%{opacity:.25}45%,65%{opacity:.85}}
@keyframes cr-node{0%,100%{opacity:.15}35%,58%{opacity:1}}
@keyframes cr-rise{0%,100%{transform:translateY(4px)}50%{transform:translateY(-9px)}}
@keyframes cr-lift{0%,100%{transform:translateY(0)}45%,65%{transform:translateY(-18px)}}
@keyframes cr-sheen{0%,18%{transform:translateX(-250px);opacity:0}30%{opacity:.35}60%{transform:translateX(250px);opacity:.35}70%,100%{transform:translateX(250px);opacity:0}}
@keyframes cr-scan{from{transform:translateY(-55px)}to{transform:translateY(105px)}}
@keyframes cr-phase{0%,28%{opacity:1}33.3%,100%{opacity:0}}
@keyframes cr-reveal{0%,38%{transform:scaleX(0)}80%,97%{transform:scaleX(1)}100%{transform:scaleX(0)}}
@keyframes cr-caret{0%,38%{transform:translateX(0)}80%,97%{transform:translateX(194px)}100%{transform:translateX(0)}}
@keyframes cr-wave{from{transform:scaleY(.2)}to{transform:scaleY(1)}}
@keyframes cr-ripple{0%{transform:scale(.65);opacity:0}25%{opacity:.2}100%{transform:scale(1.6);opacity:0}}
'''

def svg(name, w, h, body, theme, static=False):
    colors = THEMES[theme]
    variables = ';'.join(f'--{k}:{v}' for k,v in colors.items())
    reduce = '@media (prefers-reduced-motion: reduce){*{animation:none!important}}' + ('*{animation:none!important}' if static else '')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc" style="{variables}"><title id="title">{escape(name)}</title><desc id="desc">AI engineering profile. Written content stays visible; motion is decorative.</desc><defs><style>{CSS}</style></defs>{material_defs(theme)}{body}<style>{reduce}</style></svg>'

def brain_art(x, y, scale=1):
    """Chrome accelerator, attention layers, multimodal inputs and token output."""
    s = f'<g transform="translate({x} {y}) scale({scale})">'
    s += '<ellipse class="cr-pulse" cx="15" cy="4" rx="190" ry="181" fill="url(#cr-aura)"/>'
    s += label(-182, -198, 'AI / MULTIMODAL', 'silver', 10)
    for i in range(3):
        s += f'<rect class="cr-node" x="{160+i*7}" y="-205" width="3" height="8" rx="1.5" fill="var(--ruby)" style="animation-delay:-{i*.4}s"/>'
    # Elliptical chrome trajectories turn in a flattened coordinate space.
    for angle, radius, cls in [(-23,187,'cr-orbit'),(22,170,'cr-reverse')]:
        s += f'<g transform="translate(12 10) rotate({angle}) scale(1 .53)"><circle r="{radius}" fill="none" stroke="url(#cr-edge)" stroke-opacity=".2"/><g class="{cls}"><circle r="{radius}" fill="none" stroke="url(#cr-metal)" stroke-width="2" stroke-dasharray="{radius*2} {radius*4.283}"/><circle cx="{radius}" r="4" fill="var(--ruby)" filter="url(#cr-glow)"/></g></g>'
    # Three suspended attention matrices make the model structure visible.
    for layer in range(3):
        yy = -42 + layer * 35
        s += f'<g transform="translate(15 {yy})"><g class="cr-lift" style="animation-delay:-{layer*.32}s"><g transform="matrix(.91 .28 -.65 .43 0 0)">'
        s += '<rect x="-94" y="-90" width="188" height="180" rx="16" fill="url(#cr-glass)" stroke="url(#cr-edge)" stroke-width="1.5"/>'
        for row in range(7):
            for col in range(7):
                s += f'<rect class="cr-node" x="{-75+col*23}" y="{-71+row*22}" width="12" height="11" rx="2" fill="var(--{"ruby" if (row+col+layer)%3==0 else "silver"})" style="animation-delay:-{(row*.17+col*.12+layer*.65):.2f}s"/>'
        s += '</g></g></g>'
    # Floating processor in front of the model layers, with a reflective bevel.
    s += '<g transform="translate(21 -35)"><g class="cr-rise">'
    chip = 'M-66 -67H42L65 -44V53L51 67H-51L-66 52Z'
    inner = 'M-56 -57H38L55 -40V48L47 57H-47L-56 48Z'
    s += f'<path d="{chip}" transform="translate(0 8)" fill="var(--bg)" stroke="var(--ruby)" stroke-opacity=".55" stroke-width="2"/><path d="{chip}" fill="url(#cr-metal)" stroke="url(#cr-edge)" stroke-width="2"/><path d="{inner}" fill="url(#cr-glass)" stroke="var(--silver)" stroke-opacity=".4"/>'
    for yy in range(-42, 48, 15):
        s += f'<path d="M-77 {yy}H-66M65 {yy}H77" stroke="url(#cr-metal)" stroke-width="4"/>'
    # Engraved neural branches remain visible when motion is disabled.
    for sign in (-1,1):
        s += f'<g transform="scale({sign} 1)"><path d="M2 -44C16 -57 35 -42 31 -28C48 -21 41 -3 32 0C40 17 30 32 14 26L7 37" fill="none" stroke="var(--ruby)" stroke-width="1.4" stroke-opacity=".7"/><path class="cr-trace" pathLength="100" d="M2 -44C16 -57 35 -42 31 -28C48 -21 41 -3 32 0C40 17 30 32 14 26L7 37" fill="none" stroke="var(--ruby)" stroke-width="2.5" filter="url(#cr-glow)"/></g>'
    s += '<rect x="-25" y="-24" width="50" height="48" rx="12" fill="var(--bg)" stroke="var(--ruby)" stroke-opacity=".5"/>'
    s += t(0, 10, 'AI', 29, 'ink', 700, 'text-anchor="middle" letter-spacing="-1.8"')
    s += '<defs><clipPath id="cr-chip-clip"><path d="'+chip+'"/></clipPath></defs><g clip-path="url(#cr-chip-clip)"><path class="cr-sheen" d="M-90 -90H-25L85 90H20Z" fill="url(#cr-sheen)"/></g>'
    s += '<path class="cr-trace" pathLength="100" d="M-66 -67H42L65 -44V53L51 67H-51L-66 52Z" fill="none" stroke="var(--ruby)" stroke-width="1.7"/>'
    s += '</g></g>'
    # Input packets arrive from text, image and audio ports.
    for index, yy in enumerate([-120,-40,40]):
        route = f'M-148 {yy}C-104 {yy} -113 {yy+30} -58 {yy+30}'
        s += f'<path d="{route}" fill="none" stroke="var(--silver)" stroke-opacity=".28"/><path d="{route}" pathLength="100" class="cr-trace" fill="none" stroke="var(--ruby)" stroke-width="2.2" filter="url(#cr-glow)" style="animation-delay:-{index*.72}s"/>'
        s += f'<g transform="translate(-168 {yy})"><rect x="-18" y="-19" width="37" height="38" rx="9" fill="url(#cr-metal)"/><rect x="-15" y="-16" width="31" height="32" rx="7" fill="var(--bg)"/>'
        if index == 0:
            s += t(-7, 7, 'T', 19, 'silver', 600)
        elif index == 1:
            s += '<rect x="-10" y="-9" width="21" height="18" rx="2" fill="none" stroke="var(--silver)"/><path d="M-8 6L-2 -1L4 5L8 1" fill="none" stroke="var(--silver)"/><circle cx="5" cy="-4" r="2" fill="var(--ruby)"/>'
        else:
            for col,hh in enumerate([9,20,26,17,11]):
                s += f'<rect class="cr-wave" x="{-11+col*5}" y="{-hh/2}" width="2.4" height="{hh}" rx="1.2" fill="var(--ruby)" style="animation-delay:-{col*.16}s"/>'
        s += '</g>'
    # Right-hand data lattice expands and emits the final generated sequence.
    for col in range(3):
        for row in range(5):
            xx, yy = 132+col*17, -104+row*20
            s += f'<rect class="cr-node" x="{xx}" y="{yy}" width="7" height="7" rx="1.6" fill="var(--{"ruby" if col==1 else "silver"})" style="animation-delay:-{(row*.24+col*.4):.2f}s"/>'
    s += '<path d="M100 -34H125V126H20V147" fill="none" stroke="var(--silver)" stroke-opacity=".28"/><path class="cr-trace" pathLength="100" d="M100 -34H125V126H20V147" fill="none" stroke="var(--ruby)" stroke-width="2.3" filter="url(#cr-glow)"/>'
    s += '<g>'
    for index,caption in enumerate(['01 / PERCEIVE','02 / REASON','03 / GENERATE']):
        s += f'<g class="cr-phase" style="animation-delay:{index*6.4/3:.4f}s">'+t(14,160,caption,10,'ruby',500,'class="mono" text-anchor="middle" letter-spacing="1.6"')+'</g>'
    s += '</g><rect x="-125" y="178" width="277" height="41" rx="9" fill="url(#cr-glass)" stroke="url(#cr-edge)"/>'
    s += star(-105,199,8,moving=True)
    s += '<defs><clipPath id="cr-output"><rect class="cr-reveal" x="0" y="-17" width="194" height="25"/></clipPath></defs><g transform="translate(-83 204)"><g clip-path="url(#cr-output)">'+t(0,0,'see. reason. create.',14,'ink',500,'class="mono" textLength="190" lengthAdjust="spacingAndGlyphs"')+'</g><path class="cr-caret" d="M0 -12V3" stroke="var(--ruby)" stroke-width="1.5"/></g>'
    return s + '</g>'

def signature_motion():
    return '''<defs><style>
      .signature-sweep{opacity:0;animation:signature-sweep var(--period,6.4s) linear infinite}
      .signature-cell{opacity:.3;animation:signature-cell 3.2s ease-in-out infinite}
      .signature-packet{stroke-dasharray:9 3 2 4 1 81;animation:cr-trace 3.2s linear infinite}
      .signature-ring{opacity:.09;transform-box:fill-box;transform-origin:center;animation:signature-ring 4.8s ease-out infinite}
      @keyframes signature-sweep{0%,8%{transform:translateX(-190px);opacity:0}14%{opacity:.82}74%{transform:translateX(var(--travel));opacity:.82}84%,100%{transform:translateX(var(--travel));opacity:0}}
      @keyframes signature-cell{0%,100%{opacity:.16}35%,55%{opacity:.8}}
      @keyframes signature-ring{0%{transform:scale(.8);opacity:0}25%{opacity:.18}100%{transform:scale(1.6);opacity:0}}
    </style>
    <linearGradient id="signature-glint"><stop stop-color="var(--ink)" stop-opacity="0"/><stop offset=".42" stop-color="var(--ink)" stop-opacity=".05"/><stop offset=".68" stop-color="var(--ink)" stop-opacity=".9"/><stop offset=".8" stop-color="var(--silver)" stop-opacity=".8"/><stop offset="1" stop-color="var(--silver)" stop-opacity="0"/></linearGradient>
    <linearGradient id="signature-ruby"><stop stop-color="var(--ruby)" stop-opacity="0"/><stop offset=".72" stop-color="var(--ruby)" stop-opacity=".38"/><stop offset="1" stop-color="var(--ruby)" stop-opacity="0"/></linearGradient>
    </defs>'''

def signature_title(key, specs, bounds, period=6.4):
    """One semantic text copy; clipped light crosses the stationary glyphs."""
    x,y,width,height=bounds
    definitions='<defs><g id="'+key+'-glyphs">'
    for i,(xx,yy,caption,size,weight,spacing) in enumerate(specs):
        definitions+=f'<text id="{key}-line-{i}" x="{xx}" y="{yy}" font-size="{size}" font-weight="{weight}" letter-spacing="{spacing}">{escape(caption)}</text>'
    definitions+='</g><clipPath id="'+key+'-clip">'
    definitions+=''.join(f'<use href="#{key}-line-{i}"/>' for i in range(len(specs)))
    definitions+='</clipPath></defs>'
    s=definitions+'<g class="signature-title" role="presentation">'
    for i in range(len(specs)):
        s+=f'<use href="#{key}-line-{i}" fill="url(#cr-type)"/>'
    s+=f'<g clip-path="url(#{key}-clip)"><g class="signature-sweep" style="--period:{period}s;--travel:{width+220}px"><path d="M{x-95} {y}H{x-5}L{x+95} {y+height}H{x+5}Z" fill="url(#signature-glint)"/><path d="M{x-14} {y}H{x+8}L{x+108} {y+height}H{x+86}Z" fill="url(#signature-ruby)"/></g></g></g>'
    return s

def signature_bus(x,y,width,small=False):
    s=f'<g transform="translate({x} {y})" aria-hidden="true">'
    for row in range(2):
        for col in range(9):
            s+=f'<rect class="signature-cell" x="{col*7}" y="{row*5}" width="3" height="2" rx=".7" fill="var(--{"ruby" if (row+col)%3==0 else "silver"})" style="animation-delay:-{col*.16+row*.3:.2f}s"/>'
    route=f'M70 3H{width-48}L{width-40} -3H{width}'
    s+=f'<path d="{route}" fill="none" stroke="var(--silver)" stroke-opacity=".18"/><path class="signature-packet" pathLength="100" d="{route}" fill="none" stroke="var(--ruby)" stroke-width="1.4"/>'
    for xx in [width-67,width-28,width]:
        s+=f'<circle cx="{xx}" cy="{-3 if xx>width-40 else 3}" r="2.5" fill="var(--bg)" stroke="var(--silver)" stroke-opacity=".5"/>'
    return s+'</g>'

def connection_iris(x,y,r):
    s=f'<g transform="translate({x} {y})" aria-hidden="true"><circle class="signature-ring" r="{r+9}" fill="none" stroke="var(--ruby)" stroke-width=".8"/><circle r="{r+12}" fill="none" stroke="var(--silver)" stroke-opacity=".16"/>'
    s+=f'<g class="cr-reverse"><circle r="{r+12}" fill="none" stroke="var(--ruby)" stroke-width="1.3" stroke-dasharray="{r*.85} {r*9}"/><circle cx="{r+12}" r="1.8" fill="var(--silver)"/></g></g>'
    return s+star(x,y,r,'silver',True)

def hero(m):
    w,h=(400,708) if m else (1000,520)
    s=signature_motion()+panel(w,h)+label(26 if m else 42,36,'NGUYEN XUAN TRUNG',size=11 if m else 12)+star(w-44,33,13,moving=True)
    if m:
        s+=signature_title('hero-name',[(24,105,'xuan trung.',55,750,-3)],(22,57,347,59))
        s+=label(26,140,'AI ENGINEER / HCMC, VIETNAM','ruby',10)+signature_bus(26,154,340,True)
        s+=brain_art(200,342,.87)+t(26,578,'Curiosity, engineered.',25,weight=700,extra='letter-spacing="-1"')
        s+=lines(26,610,['Evidence-grounded AI. Multimodal search.','RAG systems built to be inspected.'],15,step=23)+label(26,676,'BUILD / EVALUATE / ITERATE','silver',10)
    else:
        s+='<path d="M529 50V468" stroke="url(#cr-edge)" stroke-opacity=".2"/>'
        s+=label(42,93,'AI ENGINEER / HCMC, VIETNAM','ruby')
        s+=signature_title('hero-name',[(36,211,'xuan',112,750,-7),(36,315,'trung.',112,750,-7)],(33,123,440,217))
        s+=signature_bus(44,345,425)
        s+=t(43,382,'Curiosity, engineered.',25,weight=600,extra='letter-spacing="-.7"')+lines(44,425,['Evidence-grounded AI. Multimodal search.','RAG systems built to be inspected.'],18,step=27)
        s+=brain_art(755,244,1.04)+label(623,495,'BUILD / EVALUATE / ITERATE','silver')
    return w,h,s

def work(m):
    w, h = (400, 92) if m else (1000, 100)
    return (w, h, label(8, 24, '01 / SELECTED SYSTEMS', 'ruby', 10 if m else 12) + t(6, 68, 'Proof of work.', 32 if m else 44, weight=700, extra='letter-spacing="-1.8"') + label(w - 47, 66, '[04]', size=12))

def project_defs():
    """Local animation vocabulary shared by the four project illustrations."""
    return '''<defs><style>
      .sys-packet{stroke-dasharray:17 3 3 5 2 70;animation:sys-packet 1.2s linear infinite}
      .sys-float{animation:sys-float 2.4s ease-in-out infinite alternate}
      .sys-fire{opacity:.7;animation:sys-fire 2.4s ease-in-out infinite}
      .sys-halo{transform-box:fill-box;transform-origin:center;opacity:.16;animation:sys-halo 2.4s ease-out infinite}
      .sys-scan-x{animation:sys-scan-x 2.4s ease-in-out infinite alternate}
      .sys-track{animation:sys-track 4.8s ease-in-out infinite}
      .sys-wave{transform-box:fill-box;transform-origin:center;animation:sys-wave .75s ease-in-out infinite alternate}
      .sys-playhead{animation:sys-playhead 4.8s linear infinite}
      .sys-paper{animation:sys-paper 2.4s ease-in-out infinite alternate}
      .sys-chunk{opacity:.8;animation:sys-chunk 2.4s ease-in-out infinite}
      .sys-answer{transform:scaleX(1);animation:sys-answer 4.8s ease-in-out infinite}
      .sys-scan-y{animation:sys-scan-y 2.4s ease-in-out infinite alternate}
      .sys-compress{opacity:.7;animation:sys-compress 1.2s ease-in infinite}
      .sys-chip{animation:sys-chip 2.4s ease-in-out infinite}
      .sys-check{stroke-dasharray:100;stroke-dashoffset:0;animation:sys-check 2.4s ease-in-out infinite}
      .sys-runner{transform:translate(192px,39px);animation:sys-runner 4.8s linear infinite}
      .sys-rank{transform:scaleX(1);animation:sys-rank 2.4s ease-in-out infinite}
      @keyframes sys-packet{from{stroke-dashoffset:100}to{stroke-dashoffset:0}}
      @keyframes sys-float{from{transform:translateY(1px) rotate(0deg)}to{transform:translateY(-7px) rotate(-1deg)}}
      @keyframes sys-fire{0%,100%{opacity:.22}35%,65%{opacity:1}}
      @keyframes sys-halo{0%{transform:scale(.5);opacity:0}25%{opacity:.35}100%{transform:scale(2.4);opacity:0}}
      @keyframes sys-scan-x{from{transform:translateX(0)}to{transform:translateX(220px)}}
      @keyframes sys-track{0%,100%{transform:translateX(0)}40%{transform:translateX(66px)}70%{transform:translateX(44px)}}
      @keyframes sys-wave{from{transform:scaleY(.25)}to{transform:scaleY(1)}}
      @keyframes sys-playhead{from{transform:translateX(0)}to{transform:translateX(204px)}}
      @keyframes sys-paper{from{transform:translateY(0)}to{transform:translateY(-9px)}}
      @keyframes sys-chunk{0%{transform:translate(0,0) scale(1);opacity:0}12%{opacity:1}76%{opacity:1}100%{transform:translate(89px,18px) scale(.35);opacity:0}}
      @keyframes sys-answer{0%,28%{transform:scaleX(0)}65%,94%{transform:scaleX(1)}100%{transform:scaleX(0)}}
      @keyframes sys-scan-y{from{transform:translateY(0)}to{transform:translateY(94px)}}
      @keyframes sys-compress{0%{transform:translate(0,0) scale(1);opacity:0}15%,75%{opacity:1}100%{transform:translate(var(--dx),var(--dy)) scale(.25);opacity:0}}
      @keyframes sys-chip{0%,100%{opacity:.6}45%,65%{opacity:1}}
      @keyframes sys-check{0%,20%{stroke-dashoffset:100;opacity:.2}65%,100%{stroke-dashoffset:0;opacity:1}}
      @keyframes sys-runner{0%{transform:translate(29px,163px)}12%{transform:translate(64px,163px)}27%{transform:translate(64px,121px)}43%{transform:translate(112px,121px)}58%{transform:translate(112px,76px)}76%{transform:translate(164px,76px)}89%{transform:translate(164px,39px)}100%{transform:translate(192px,39px)}}
      @keyframes sys-rank{0%,100%{transform:scaleX(.35)}50%{transform:scaleX(1)}}
    </style>
    <filter id="sys-glow" x="-70%" y="-70%" width="240%" height="240%"><feGaussianBlur stdDeviation="1.8" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <linearGradient id="sys-scan-y" x1="0" y1="0" x2="0" y2="1"><stop stop-color="var(--ruby)" stop-opacity="0"/><stop offset="1" stop-color="var(--ruby)" stop-opacity=".3"/></linearGradient>
    </defs>'''

def signal(route, c='ruby', width=2.2, delay=0):
    return f'<path d="{route}" fill="none" stroke="var(--{c})" stroke-opacity=".24"/><path class="sys-packet" d="{route}" pathLength="100" fill="none" stroke="var(--{c})" stroke-width="{width}" stroke-linecap="round" filter="url(#sys-glow)" style="animation-delay:-{delay}s"/>'

def art_footer(captions):
    s = signal('M19 212H261', 'silver', 1.8)
    for i, caption in enumerate(captions):
        cx = [19, 140, 261][i]
        s += f'<circle cx="{cx}" cy="212" r="3" fill="var(--bg)" stroke="var(--ruby)"/><circle class="sys-fire" cx="{cx}" cy="212" r="1.7" fill="var(--ruby)" style="animation-delay:-{i}s"/>'
        s += t(cx, 231, caption, 8.5, 'muted', 500, f'class="mono" text-anchor="{["start", "middle", "end"][i]}" letter-spacing=".5"')
    return s

def video_art(x, y, scale=1):
    s = f'<g transform="translate({x} {y}) scale({scale})"><ellipse cx="141" cy="102" rx="144" ry="115" fill="url(#haze)"/>'
    s += '<g class="sys-float"><rect x="35" y="10" width="227" height="139" rx="12" fill="var(--soft)" stroke="var(--line)"/></g><rect x="25" y="20" width="228" height="140" rx="12" fill="var(--panel)" stroke="var(--silver)" stroke-opacity=".3"/><rect x="14" y="30" width="228" height="141" rx="12" fill="var(--bg)" stroke="var(--silver)" stroke-opacity=".65"/>'
    s += '<defs><clipPath id="video-window"><rect x="15" y="31" width="226" height="139" rx="11"/></clipPath></defs><g clip-path="url(#video-window)">'
    for i, hh in enumerate([43, 72, 53, 89, 67, 42, 75]):
        s += f'<rect x="{24+i*31}" y="{146-hh}" width="24" height="{hh}" rx="2" fill="var(--soft)" opacity=".45"/>'
    for yy in [55, 80, 105, 130, 155]:
        s += f'<path d="M18 {yy}H240" stroke="var(--line)" stroke-width=".55"/>'
    s += '<g transform="translate(46 71)"><g class="sys-track"><circle cx="21" cy="16" r="9" fill="var(--silver)" opacity=".7"/><path d="M7 54Q5 30 21 30Q37 30 35 54M15 54L11 73M27 54L32 73" fill="none" stroke="var(--silver)" stroke-width="7" stroke-linecap="round" opacity=".6"/><rect x="0" y="0" width="43" height="81" rx="4" fill="var(--ruby)" fill-opacity=".035" stroke="var(--ruby)" stroke-width="1.4"/><path d="M-3 11V-3H10M33 -3H46V11M46 70V84H33M10 84H-3V70" fill="none" stroke="var(--ruby)" stroke-width="2.3"/>'
    s += label(2, -7, 'TRACK', 'ruby', 7) + '</g></g>'
    s += '<rect x="181" y="108" width="32" height="36" rx="4" fill="var(--silver)" fill-opacity=".08" stroke="var(--silver)" stroke-dasharray="3 3"/><g class="sys-scan-x"><rect x="-9" y="32" width="28" height="136" fill="url(#scan-grad)"/><path d="M19 32V168" stroke="var(--ruby)" stroke-width="2" filter="url(#sys-glow)"/></g></g>'
    s += '<rect x="30" y="43" width="37" height="12" rx="4" fill="var(--panel)"/>' + label(36, 52, 'VIDEO', 'silver', 6.5)
    for i in range(31):
        hh = 3 + (i * 7 % 11)
        s += f'<rect class="sys-wave" x="{26+i*4}" y="{186-hh/2}" width="2" height="{hh}" rx="1" fill="var(--silver)" style="animation-delay:-{i*.08:.2f}s"/>'
    s += '<path d="M28 164H232" stroke="var(--line)"/><g class="sys-playhead"><path d="M28 159V168" stroke="var(--ruby)" stroke-width="2"/><circle cx="28" cy="159" r="2.4" fill="var(--ruby)"/></g><g class="sys-fire"><rect x="170" y="179" width="74" height="19" rx="6" fill="var(--ruby)" fill-opacity=".09" stroke="var(--ruby)" stroke-opacity=".65"/>' + label(180, 192, 'CITED ↗', 'ruby', 8) + '</g>'
    return s + art_footer(['TRACK', 'RETRIEVE', 'CITE']) + '</g>'

def docs_art(x, y, scale=1):
    s = f'<g transform="translate({x} {y}) scale({scale})"><ellipse cx="138" cy="107" rx="142" ry="112" fill="url(#haze)"/>'
    s += '<g class="sys-paper"><rect x="26" y="20" width="65" height="95" rx="8" fill="var(--soft)" stroke="var(--line)"/></g><g class="sys-paper" style="animation-delay:-1.5s"><rect x="16" y="36" width="67" height="96" rx="8" fill="var(--panel)" stroke="var(--silver)" stroke-opacity=".6"/></g><rect x="7" y="53" width="67" height="101" rx="8" fill="var(--bg)" stroke="var(--silver)"/>'
    s += label(18, 75, 'PDF', 'silver', 10)
    for i, yy in enumerate([89, 102, 115, 128]):
        s += f'<rect x="18" y="{yy}" width="{43 if i%2==0 else 32}" height="3" rx="1" fill="var(--muted)" opacity=".4"/><rect class="sys-fire" x="15" y="{yy-4}" width="49" height="11" rx="3" fill="var(--silver)" fill-opacity=".16" style="animation-delay:-{i*.5}s"/>'
    for i in range(5):
        s += f'<g transform="translate(54 {79+i*12})"><rect class="sys-chunk" width="22" height="5" rx="2" fill="var(--silver)" style="animation-delay:-{i*.6}s"/></g>'
    s += signal('M70 105C101 105 98 128 118 128', 'silver', 2.3)
    s += '<g class="sys-chip"><path d="M113 89V147C113 158 162 158 162 147V89" fill="var(--bg)" stroke="var(--silver)"/><ellipse cx="137.5" cy="89" rx="24.5" ry="10" fill="var(--soft)" stroke="var(--silver)"/><path d="M113 112C113 124 162 124 162 112M113 135C113 147 162 147 162 135" fill="none" stroke="var(--silver)" stroke-opacity=".45"/></g>'
    for row in range(3):
        for col in range(5):
            s += f'<rect class="sys-fire" x="{120+col*7}" y="{101+row*22}" width="3" height="5" rx="1" fill="var(--ruby)" style="animation-delay:-{(row+col)*.24:.2f}s"/>'
    s += signal('M162 113H185V77H197', 'ruby', 2.5, .4)
    s += '<g transform="translate(188 36)"><g class="sys-float"><rect width="81" height="133" rx="10" fill="var(--bg)" stroke="var(--ruby)" stroke-opacity=".7"/>' + label(11, 22, 'ANSWER', 'ruby', 8)
    for i, width in enumerate([58, 47, 54, 34]):
        s += f'<g transform="translate(11 {38+i*13})"><rect class="sys-answer" width="{width}" height="3" rx="1" fill="var(--ink)" opacity=".75" style="animation-delay:{i*.15}s"/></g>'
    s += '<rect x="10" y="99" width="61" height="23" rx="5" fill="var(--ruby)" fill-opacity=".1" stroke="var(--ruby)" stroke-opacity=".4"/>' + label(18, 114, 'CITED ↗', 'ruby', 8) + '</g></g>'
    s += signal('M40 158V183H229V173', 'silver', 1.8, .7) + label(104, 190, 'VERSIONED', 'muted', 7)
    return s + art_footer(['INGEST', 'RETRIEVE', 'GROUND']) + '</g>'

def latent_art(x, y, scale=1):
    s = f'<g transform="translate({x} {y}) scale({scale})"><ellipse cx="145" cy="110" rx="140" ry="111" fill="url(#haze)"/>'
    s += '<rect x="7" y="28" width="95" height="142" rx="13" fill="var(--bg)" stroke="var(--silver)" stroke-opacity=".65"/><defs><clipPath id="face-window"><rect x="8" y="29" width="93" height="140" rx="12"/></clipPath></defs><g clip-path="url(#face-window)">'
    face = [(54,48),(34,58),(73,58),(27,81),(81,81),(34,108),(74,108),(43,129),(65,129),(54,141),(42,81),(66,81),(54,100),(42,116),(66,116)]
    s += '<path d="M54 47C20 47 23 99 32 115Q54 153 76 115C85 99 88 47 54 47Z" fill="var(--silver)" fill-opacity=".055" stroke="var(--silver)" stroke-opacity=".7"/>'
    for a,b in [(0,1),(0,2),(1,3),(2,4),(3,5),(4,6),(5,7),(6,8),(7,9),(8,9),(1,10),(2,11),(10,11),(10,12),(11,12),(12,13),(12,14),(13,14),(13,7),(14,8),(3,10),(4,11),(5,13),(6,14)]:
        s += f'<path d="M{face[a][0]} {face[a][1]}L{face[b][0]} {face[b][1]}" stroke="var(--silver)" stroke-opacity=".45" stroke-width=".8"/>'
    for i,(cx,cy) in enumerate(face):
        s += f'<circle class="sys-fire" cx="{cx}" cy="{cy}" r="2" fill="var(--ruby)" style="animation-delay:-{i*.16:.2f}s"/>'
    s += '<g class="sys-scan-y"><rect x="8" y="24" width="93" height="28" fill="url(#sys-scan-y)"/><path d="M8 52H101" stroke="var(--ruby)" stroke-width="2" filter="url(#sys-glow)"/></g></g>'
    for i in range(11):
        yy=46+i*10
        s += f'<path d="M103 {yy}L152 98" stroke="var(--silver)" stroke-opacity=".12"/><g transform="translate(101 {yy})"><rect class="sys-compress" x="-2" y="-2" width="5" height="5" rx="1" fill="var(--silver)" style="--dx:52px;--dy:{98-yy}px;animation-delay:-{i*.136:.3f}s"/></g>'
    s += '<g class="sys-chip"><rect x="144" y="58" width="72" height="80" rx="12" fill="var(--ruby)" fill-opacity=".035" stroke="var(--ruby)" stroke-opacity=".35"/><rect x="151" y="65" width="58" height="66" rx="9" fill="var(--bg)" stroke="var(--ruby)"/></g>'
    for row in range(8):
        for col in range(8):
            s += f'<rect class="sys-fire" x="{159+col*5.5}" y="{76+row*5.5}" width="3" height="3" rx=".7" fill="var(--ruby)" style="animation-delay:-{(row*8+col)*.046:.3f}s"/>'
    s += t(180, 153, '64 B', 15, 'ruby', 600, 'class="mono" text-anchor="middle"')
    s += signal('M211 98H239', 'ruby', 2.7)
    s += '<path d="M253 79L268 85V100Q267 114 253 123Q239 114 238 100V85Z" fill="var(--ruby)" fill-opacity=".06" stroke="var(--ruby)" stroke-width="1.5"/><path class="sys-check" pathLength="100" d="M245 99L251 105L262 92" fill="none" stroke="var(--ruby)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>'
    s += label(34, 188, 'EDGE', 'silver', 8) + label(223, 188, 'SERVER', 'ruby', 8)
    return s + art_footer(['ENCODE', 'QUANTIZE', 'VERIFY']) + '</g>'

def trajectory_art(x, y, scale=1):
    s = f'<g transform="translate({x} {y}) scale({scale})"><ellipse cx="140" cy="108" rx="145" ry="115" fill="url(#haze)"/><rect x="9" y="17" width="204" height="173" rx="13" fill="var(--bg)" stroke="var(--silver)" stroke-opacity=".6"/>'
    for xx in range(24,207,14):
        for yy in range(31,184,14):
            s += f'<circle cx="{xx}" cy="{yy}" r=".7" fill="var(--silver)" opacity=".2"/>'
    s += '<path d="M47 17V65H91M9 99H45V140M85 190V147H140V110H190M132 17V50H104V86H80M188 58H213" fill="none" stroke="var(--soft)" stroke-width="9" stroke-linejoin="round"/>'
    routes=['M29 163H64V121H112V76H164V39H192','M29 163V117H65V84H110V61H162V39H192','M29 163H64V178H157V141H174V87H193V39']
    for i,route in enumerate(routes):
        s += signal(route, 'ruby' if i==0 else 'silver', 2.5 if i==0 else 1.6, i*.42)
    s += '<circle cx="29" cy="163" r="4" fill="var(--bg)" stroke="var(--silver)"/><circle cx="192" cy="39" r="5" fill="var(--bg)" stroke="var(--ruby)"/><g class="sys-runner"><circle class="sys-halo" r="7" fill="var(--ruby)"/><circle r="3.7" fill="var(--ruby)" filter="url(#sys-glow)"/></g>'
    s += '<circle class="sys-halo" cx="112" cy="121" r="11" fill="var(--silver)"/><circle cx="112" cy="121" r="6" fill="var(--bg)" stroke="var(--silver)"/><path d="M109 121H115M112 118V124" stroke="var(--silver)"/>'
    s += signal('M213 101H228', 'silver', 2.4) + label(225, 37, 'UTILITY', 'silver', 7)
    for i,ww in enumerate([34,25,29,19,13]):
        yy=53+i*23
        s += f'<rect x="228" y="{yy}" width="39" height="14" rx="4" fill="var(--soft)"/><g transform="translate(231 {yy+4})"><rect class="sys-rank" width="{ww}" height="6" rx="2" fill="var(--{"ruby" if i==0 else "silver"})" opacity="{1-i*.14}" style="animation-delay:-{i*.35}s"/></g>'
    s += label(229, 182, 'OFFLINE', 'muted', 7)
    return s + art_footer(['SCORE', 'INTERVENE', 'EVALUATE']) + '</g>'

PROJECTS = {
    'tracevision': dict(name='TraceVision', tag='MULTIMODAL / VIDEO SEARCH', metric='52.3×', ml='cache-reuse speedup', mobile_metric=['cache-reuse', 'speedup'], scope=['Recorded local benchmark.', 'Persisted outputs reused.'], desc=['Find the moment. Show the evidence.', 'Bilingual video search with timestamped citations.'], md=['Bilingual video search with', 'timestamped evidence.'], stack='PYTORCH · MULTIMODAL RETRIEVAL · STAGE CACHES', art=video_art),
    'knowledge': dict(name='Subject Knowledge Hub', tag='RAG / RELIABLE INGESTION', metric='3/3', ml='interrupted jobs recovered', mobile_metric=['interrupted jobs', 'recovered'], scope=['Controlled process-kill tests.', 'Fixture embeddings.'], desc=['PDF answers that know their source.', 'Version-aware citations and resumable ingestion.'], md=['Version-aware PDF citations.', 'Ingestion that can resume.'], stack='FASTAPI · PGVECTOR · CELERY · REDIS', art=docs_art),
    'aqb': dict(name='AQB-FAS', tag='COMPUTER VISION / EDGE AI', metric='64 B', ml='serialized latent payload', mobile_metric=['serialized', 'latent payload'], scope=['97.01% CelebA-Spoof test accuracy.', 'Validation-selected operating threshold.'], desc=['A smaller payload. A testable interface.', 'Split-computing face anti-spoofing for edge devices.'], md=['Split-computing face anti-spoofing.', 'A compact edge-to-server interface.'], stack='PYTORCH · QUANTIZATION · HELD-OUT EVALUATION', art=latent_art),
    'datu': dict(name='DATU / Offline RL', tag='REINFORCEMENT LEARNING / INDEPENDENT STUDY', metric='86', ml='completed training jobs', mobile_metric=['completed', 'training jobs'], scope=['Frozen original experiment matrix.', 'Four offline-RL learners; 17.8M updates.'], desc=['Which trajectories change a policy?', 'Offline ranking, frozen interventions and paired evaluation.'], md=['Which trajectories change a policy?', 'Offline ranking. Paired evaluation.'], stack='PYTORCH · IQL / REBRAC / CQL / BC · REPRODUCIBLE EVAL', art=trajectory_art),
}

def project(key,m):
    p = PROJECTS[key]
    w,h = (400,630) if m else (1000,378)
    s = project_defs()+panel(w,h,'panel')
    if m:
        s += label(24,32,p['tag'],'silver',8 if key=='datu' else 9)+arrow(353,23,'ruby')
        s += lines(23,74,['Subject','Knowledge Hub'],29,'ink',33,700) if key=='knowledge' else t(23,78,p['name'],32,weight=700,extra='letter-spacing="-1.1"')
        s += enhance_art(p['art'](39,128,1.15))+lines(24,435,p['md'],15.5,step=23)
        s += t(22,520,p['metric'],49,'ruby',600,extra='letter-spacing="-2"')+lines(179,499,p['mobile_metric'],14,'ink',21)
        s += rule(24,541,376)+lines(24,565,p['scope'],12.5,step=19)+label(24,610,'VIEW SOURCE ↗','silver',10)
    else:
        s += enhance_art(p['art'](25,72,1.05))+'<path d="M337 36V341" stroke="url(#cr-edge)" stroke-opacity=".3"/>'
        s += label(370,43,p['tag'],'silver',10.5)+arrow(947,29,'ruby')
        s += t(367,97,p['name'],33,weight=700,extra='letter-spacing="-1.1"')+lines(370,140,p['desc'],18,step=27)
        s += '<rect x="364" y="191" width="595" height="111" rx="10" fill="var(--bg)" fill-opacity=".45" stroke="var(--line)" stroke-opacity=".6"/>'
        s += t(378,258,p['metric'],56,'ruby',600,extra='letter-spacing="-2"')
        mx = 562 if key=='tracevision' else 528
        s += t(mx,230,p['ml'],17,'ink',500)+lines(mx,255,p['scope'],12.5,step=19)+rule(370,323,957)+label(370,350,p['stack'],size=10)
    return w,h,s

def profile_defs():
    """Motion for the experience, research and toolkit sections only."""
    return '''<defs><style>
      .prof-packet{stroke-dasharray:17 3 3 5 2 70;animation:prof-packet 1.2s linear infinite}
      .prof-pulse{opacity:.7;animation:prof-pulse 2.4s ease-in-out infinite}
      .prof-cluster{animation:prof-cluster 4.8s ease-in-out infinite}
      .prof-halo{transform-box:fill-box;transform-origin:center;opacity:.15;animation:prof-halo 2.4s ease-out infinite}
      .prof-paper{animation:prof-paper 2.4s ease-in-out infinite alternate}
      .prof-scan{animation:prof-scan 2.4s ease-in-out infinite alternate}
      .prof-draw{stroke-dasharray:100;stroke-dashoffset:0;animation:prof-draw 4.8s ease-in-out infinite}
      .prof-bar{transform-box:fill-box;transform-origin:left center;animation:prof-bar 2.4s ease-in-out infinite alternate}
      .prof-rack{animation:prof-rack 2.4s ease-in-out infinite alternate}
      .prof-sweep{animation:prof-sweep 4.8s linear infinite}
      @keyframes prof-packet{from{stroke-dashoffset:100}to{stroke-dashoffset:0}}
      @keyframes prof-pulse{0%,100%{opacity:.22}35%,65%{opacity:1}}
      @keyframes prof-cluster{0%,12%,100%{transform:translate(var(--sx),var(--sy))}58%,86%{transform:translate(0,0)}}
      @keyframes prof-halo{0%{transform:scale(.55);opacity:0}25%{opacity:.3}100%{transform:scale(2.1);opacity:0}}
      @keyframes prof-paper{from{transform:translateY(0) rotate(0deg)}to{transform:translateY(-8px) rotate(-2deg)}}
      @keyframes prof-scan{from{transform:translateY(0)}to{transform:translateY(92px)}}
      @keyframes prof-draw{0%,12%{stroke-dashoffset:100;opacity:.3}68%,94%{stroke-dashoffset:0;opacity:1}100%{stroke-dashoffset:100;opacity:.3}}
      @keyframes prof-bar{from{transform:scaleX(.25)}to{transform:scaleX(1)}}
      @keyframes prof-rack{from{transform:translateY(2px)}to{transform:translateY(-4px)}}
      @keyframes prof-sweep{from{transform:translateX(0)}to{transform:translateX(var(--travel))}}
    </style>
    <filter id="prof-glow" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="1.6" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <linearGradient id="prof-scan-fill" x1="0" y1="0" x2="0" y2="1"><stop stop-color="var(--ruby)" stop-opacity="0"/><stop offset="1" stop-color="var(--ruby)" stop-opacity=".22"/></linearGradient>
    <linearGradient id="prof-sweep-fill"><stop stop-color="var(--silver)" stop-opacity="0"/><stop offset="1" stop-color="var(--ruby)" stop-opacity=".85"/></linearGradient>
    </defs>'''

def profile_signal(route, c='ruby', delay=0, width=2):
    return f'<path d="{route}" fill="none" stroke="var(--{c})" stroke-opacity=".23"/><path class="prof-packet" pathLength="100" d="{route}" fill="none" stroke="var(--{c})" stroke-width="{width}" stroke-linecap="round" filter="url(#prof-glow)" style="animation-delay:-{delay}s"/>'

def delivery_stage(index, x, y, width):
    captions = [('SEGMENT', 'RFM / K-MEANS'), ('RESEARCH', 'GEMINI / SERPAPI'), ('SERVE', 'FASTAPI / POSTGRES'), ('DEPLOY', 'DOCKER / AWS EC2')]
    caption, tools = captions[index]
    scale = (width - 20) / 180
    s = f'<g transform="translate({x} {y})"><rect width="{width}" height="104" rx="12" fill="var(--panel)" stroke="var(--line)"/>'
    s += label(12, 19, f'0{index+1} / {caption}', 'silver', 9) + label(12, 94, tools, 'muted', 7.5)
    s += f'<g transform="translate(10 25) scale({scale} .85)">'
    if index == 0:
        centers = [(37, 26), (93, 38), (145, 24)]
        colors = ['silver', 'ruby', 'ink']
        for i, ((cx, cy), color) in enumerate(zip(centers, colors)):
            s += f'<circle cx="{cx}" cy="{cy}" r="19" fill="var(--{color})" opacity=".045"/><circle cx="{cx}" cy="{cy}" r="2.4" fill="var(--{color})"/>'
            for j in range(9):
                a=j*2.4+i;rr=8+(j%3)*4
                px=cx+math.cos(a)*rr;py=cy+math.sin(a)*rr
                sx=10+(j*19+i*37)%160;sy=7+(j*13+i*17)%43
                s += f'<circle class="prof-cluster" cx="{px:.2f}" cy="{py:.2f}" r="2" fill="var(--{color})" style="--sx:{sx-px:.2f}px;--sy:{sy-py:.2f}px"/>'
    elif index == 1:
        for i in range(3):
            yy=7+i*18
            s += f'<rect x="6" y="{yy}" width="31" height="12" rx="4" fill="var(--soft)" stroke="var(--silver)" stroke-opacity=".4"/>'
            s += profile_signal(f'M37 {yy+6}Q62 {yy+6} 83 29', 'silver', i*.4)
        s += '<circle class="prof-halo" cx="90" cy="29" r="17" fill="var(--ruby)"/>' + star(90, 29, 11, 'ruby')
        s += profile_signal('M102 29H132', 'ruby', .6)
        for i in range(3):
            s += f'<rect class="prof-bar" x="137" y="{12+i*15}" width="{36-i*7}" height="5" rx="2" fill="var(--ruby)" style="animation-delay:-{i*.5}s"/>'
    elif index == 2:
        s += '<rect x="67" y="3" width="49" height="52" rx="9" fill="var(--bg)" stroke="var(--silver)"/>'
        s += t(91, 37, '{ }', 24, 'ruby', 500, 'text-anchor="middle" class="mono"')
        for i in range(3):
            yy=11+i*18
            s += profile_signal(f'M5 {yy}H65', 'silver', i*.35, 2.5)
            s += profile_signal(f'M118 {yy}H176', 'ruby', i*.35+.6, 2.5)
    else:
        s += '<path d="M37 43C11 43 16 19 37 20C41 -1 70 -3 78 15C97 7 113 17 112 30H149" fill="none" stroke="var(--silver)" stroke-opacity=".6"/>'
        s += profile_signal('M17 52H66V29H103', 'silver', .5)
        for row in range(2):
            for col in range(3):
                xx=103+col*21;yy=14+row*22
                s += f'<g transform="translate({xx} {yy})"><g class="prof-rack" style="animation-delay:-{(row+col)*.45}s"><rect width="17" height="18" rx="3" fill="var(--bg)" stroke="var(--ruby)" stroke-opacity=".65"/><circle class="prof-pulse" cx="5" cy="5" r="1.5" fill="var(--ruby)"/><path d="M4 11H13M4 14H10" stroke="var(--silver)" stroke-opacity=".55"/></g></g>'
    return s + '</g></g>'

def experience(m):
    w, h = (400, 610) if m else (1000, 398)
    p = 24 if m else 36
    s = profile_defs() + panel(w, h) + label(p, 34, '02 / IN THE FIELD', 'ruby', 10 if m else 12)
    s += t(p-1, 79, 'Built beyond the notebook.', 24 if m else 36, weight=700, extra='letter-spacing="-1"')
    if m:
        s += t(p, 123, 'ECE Technology', 23, weight=600) + t(p, 151, 'AI Engineer Intern', 16, 'silver') + label(p, 176, 'JAN–APR 2026 · E-COMMERCE MVP', size=9)
        s += lines(p, 213, ['RFM segmentation · Mini-Batch K-Means.', 'Market research · Gemini + SerpAPI.', 'FastAPI / PostgreSQL microservice.', 'Docker deployment on AWS EC2.'], 14.5, step=23)
        s += '<g transform="translate(24 321)">' + profile_signal('M164 52H188', 'ruby') + profile_signal('M270 104V123H82V142', 'silver', .6) + profile_signal('M164 194H188', 'ruby', 1)
        for i, (xx, yy) in enumerate([(0,0),(188,0),(0,142),(188,142)]):
            s += delivery_stage(i, xx, yy, 164)
        s += '</g>' + label(p, 589, 'PROBLEM → MODEL → SERVICE → DEPLOYMENT', 'silver', 8.5)
    else:
        s += t(p, 130, 'ECE Technology', 23, weight=600) + t(p, 160, 'AI Engineer Intern', 17, 'silver') + label(p, 190, 'JAN–APR 2026 · E-COMMERCE MVP', size=10)
        s += '<path d="M329 107V201" stroke="var(--line)"/>' + lines(361, 130, ['RFM segmentation with Mini-Batch K-Means.', 'Market intelligence with Gemini and SerpAPI.', 'FastAPI / PostgreSQL microservice, deployed on AWS EC2.'], 18, step=29)
        s += '<g transform="translate(36 237)">'
        for i in range(3):
            s += profile_signal(f'M{204+i*242} 52H{242+i*242}', 'ruby' if i%2==0 else 'silver', i*.4)
        for i in range(4):
            s += delivery_stage(i, i*242, 0, 204)
        s += '</g>' + label(p, 375, 'PROBLEM → MODEL → SERVICE → DEPLOYMENT', 'silver', 10)
    return (w, h, s)

PAPERS = [
    dict(key='weather', status='published', short='Weather forecasting & shelter suggestion', mobile=['Weather forecasting', '& shelter suggestion'], venue='AJCAI 2025 / Springer'),
    dict(key='yolo', status='published', short='YOLOv11n model optimization', venue='EIDT 2025 / Springer'),
    dict(key='counterfail', status='accepted', short='CounterFail-Edge', venue='ICARCV 2026'),
    dict(key='wca', status='accepted', short='WCA-GRU / Bearing RUL', venue='SIMC 2026'),
    dict(key='tiny', status='submitted', short='TinyConformalAD', venue='FISAT 2026'),
    dict(key='aqb', status='submitted', short='AQB-FAS / Quantized bottlenecks', venue='RIVF 2026 · First author'),
    dict(key='routing', status='submitted', short='Conditional routing for UAV detection', mobile=['Conditional routing', 'for UAV detection'], venue='RIVF 2026'),
]

def research_art(x,y,scale=1):
    definitions='''<defs><style>
      .lab-layer{animation:lab-layer 6.4s cubic-bezier(.45,0,.25,1) infinite}
      .lab-cell{opacity:.65;animation:lab-cell 6.4s ease-in-out infinite}
      .lab-column{animation:lab-column 6.4s ease-in-out infinite}
      .lab-sweep{opacity:0;animation:lab-sweep 6.4s ease-in-out infinite}
      .lab-stream{stroke-dasharray:12 4 2 82;animation:cr-trace 1.6s linear infinite}
      .lab-port{animation:lab-port 6.4s ease-in-out infinite}
      .lab-trace{stroke-dasharray:100;stroke-dashoffset:0;animation:lab-trace 6.4s ease-in-out infinite}
      .lab-verify{stroke-dasharray:100;stroke-dashoffset:0;animation:lab-verify 6.4s ease-in-out infinite}
      .lab-halo{opacity:.12;transform-box:fill-box;transform-origin:center;animation:lab-halo 6.4s ease-out infinite}
      .lab-glint{opacity:0;animation:lab-glint 6.4s ease-in-out infinite}
      @keyframes lab-layer{0%,100%{transform:translateY(0)}30%,68%{transform:translateY(var(--lift,-9px))}}
      @keyframes lab-cell{0%,100%{opacity:.15}24%,48%{opacity:.95}65%,83%{opacity:.45}}
      @keyframes lab-column{0%,15%,100%{opacity:.2}35%,65%{opacity:1}}
      @keyframes lab-sweep{0%,10%{transform:translateX(-22px);opacity:0}18%{opacity:.8}60%{transform:translateX(126px);opacity:.8}70%,100%{transform:translateX(126px);opacity:0}}
      @keyframes lab-port{0%,100%{opacity:.45}22%,45%{opacity:1}}
      @keyframes lab-trace{0%,28%{stroke-dashoffset:100;opacity:.4}68%,96%{stroke-dashoffset:0;opacity:1}100%{stroke-dashoffset:100;opacity:.4}}
      @keyframes lab-verify{0%,62%{stroke-dashoffset:100;opacity:.15}77%,96%{stroke-dashoffset:0;opacity:1}100%{stroke-dashoffset:100;opacity:.15}}
      @keyframes lab-halo{0%,64%{transform:scale(.85);opacity:0}76%{opacity:.25}100%{transform:scale(1.45);opacity:0}}
      @keyframes lab-glint{0%,58%{transform:translateX(-80px);opacity:0}65%{opacity:.25}86%{transform:translateX(235px);opacity:.25}96%,100%{transform:translateX(235px);opacity:0}}
    </style>
    <clipPath id="lab-tensor"><rect x="-6" y="-6" width="108" height="108" rx="7"/></clipPath>
    <clipPath id="lab-result"><rect x="45" y="216" width="192" height="77" rx="10"/></clipPath>
    <linearGradient id="lab-beam"><stop stop-color="var(--ruby)" stop-opacity="0"/><stop offset=".82" stop-color="var(--ruby)" stop-opacity=".55"/><stop offset="1" stop-color="var(--ink)" stop-opacity=".55"/></linearGradient>
    </defs>'''
    s=definitions+f'<g class="research-instrument" transform="translate({x} {y}) scale({scale})">'
    s+='<ellipse class="cr-pulse" cx="140" cy="167" rx="139" ry="151" fill="url(#cr-aura)"/>'
    s+=label(88,19,'EXPERIMENT','silver',8)
    s+='<path d="M15 43V31H45M235 31H265V43M15 282V302H43M238 302H265V282" fill="none" stroke="url(#cr-edge)" stroke-opacity=".45"/>'
    # Source ports feed the tensor stack along visible, continuous routes.
    for i,(xx,yy,tx,ty) in enumerate([(15,90,68,92),(15,157,79,147),(265,103,213,99),(265,175,205,155)]):
        route=f'M{xx} {yy}H{(xx+tx)/2}L{tx} {ty}'
        s+=f'<path d="{route}" fill="none" stroke="var(--silver)" stroke-opacity=".25"/><path class="lab-stream" pathLength="100" d="{route}" fill="none" stroke="var(--ruby)" stroke-width="1.8" style="animation-delay:-{i*.4}s"/>'
        s+=f'<g class="lab-port" style="animation-delay:-{i*.35}s"><rect x="{xx-7}" y="{yy-9}" width="14" height="18" rx="4" fill="url(#cr-glass)" stroke="url(#cr-edge)"/><path d="M{xx-3} {yy-2}H{xx+3}M{xx-3} {yy+2}H{xx+1}" stroke="var(--ruby)" stroke-width="1.2"/></g>'
    # Draw back to front. Consistent affine projection gives the plates real depth.
    for layer in [2,1,0]:
        yy=62+layer*22
        s+=f'<g transform="translate(140 {yy})"><g class="lab-layer" style="--lift:{-5-layer*5}px;animation-delay:-{layer*.22}s"><g transform="matrix(.98 .55 -.98 .55 0 0)">'
        s+='<rect x="-6" y="-6" width="108" height="108" rx="7" fill="url(#cr-glass)" stroke="url(#cr-edge)" stroke-width="1.3"/>'
        s+='<path d="M-2 -4H96Q100 -4 100 0V95" fill="none" stroke="var(--silver)" stroke-opacity=".45" stroke-width=".65"/>'
        for row in range(7):
            for col in range(7):
                active=(row==col or (row+2*col+layer)%5==0)
                s+=f'<rect class="lab-cell" x="{4+col*13}" y="{4+row*13}" width="8" height="8" rx="1.4" fill="var(--{"ruby" if active else "silver"})" style="animation-delay:-{(col*.23+row*.1+layer*.54):.2f}s"/>'
        s+='<g clip-path="url(#lab-tensor)"><g class="lab-sweep" style="animation-delay:-'+str(layer*.2)+'s"><rect x="-16" y="-7" width="24" height="110" fill="url(#lab-beam)"/><path d="M8 -6V101" stroke="var(--ruby)" stroke-width="1.1"/></g></g>'
        s+='</g></g></g>'
    # Three streams carry activations into the experimental trace below.
    for i,xx in enumerate([99,140,181]):
        route=f'M{xx} {179 if i!=1 else 199}V205Q{xx} 211 {xx+8} 211H{144 if i==0 else 181 if i==1 else 212}V221'
        s+=f'<path d="{route}" fill="none" stroke="var(--silver)" stroke-opacity=".2"/><path class="lab-stream" pathLength="100" d="{route}" fill="none" stroke="var(--ruby)" stroke-width="1.8" style="animation-delay:-{i*.4}s"/>'
    # A fixed reference trace and a drawn experimental trace: no invented metrics.
    s+='<rect x="45" y="216" width="192" height="77" rx="10" fill="url(#cr-glass)" stroke="url(#cr-edge)" stroke-width="1.2"/>'
    for yy in [237,255,274]:
        s+=f'<path d="M58 {yy}H223" stroke="var(--silver)" stroke-opacity=".11"/>'
    reference='M58 270C73 268 78 251 92 257S112 243 127 249S148 238 162 243S186 230 211 232'
    measured='M58 273C75 272 77 264 90 261S105 248 120 252S143 234 158 241S181 229 211 233'
    s+=f'<path d="{reference}" fill="none" stroke="var(--silver)" stroke-width="1.2" stroke-opacity=".42" stroke-dasharray="3 3"/><path d="{measured}" fill="none" stroke="var(--ruby)" stroke-opacity=".14" stroke-width="1.8"/><path class="lab-trace" pathLength="100" d="{measured}" fill="none" stroke="var(--ruby)" stroke-width="2.2" filter="url(#cr-glow)"/>'
    s+='<g clip-path="url(#lab-result)"><rect class="lab-glint" x="0" y="215" width="42" height="80" fill="url(#cr-sheen)"/></g>'
    s+='<g transform="translate(233 271)"><circle class="lab-halo" r="22" fill="var(--ruby)"/><circle r="22" fill="url(#cr-metal)"/><circle r="19" fill="var(--bg)" stroke="var(--ruby)" stroke-opacity=".5"/><path d="M-9 0L-2 7L10 -7" fill="none" stroke="var(--silver)" stroke-opacity=".2" stroke-width="2"/><path class="lab-verify" pathLength="100" d="M-9 0L-2 7L10 -7" fill="none" stroke="var(--ruby)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></g>'
    s+=label(45,327,'QUESTION / TEST / REPRODUCE','muted',8)
    return s+'</g>'

def research(m):
    w,h=(400,1030) if m else (1000,680)
    p=24 if m else 36
    s=profile_defs()+panel(w,h)+label(p,34,'03 / RESEARCH NOTES','ruby',10 if m else 12)
    s+=t(p-1,79,'Ask better questions.',28 if m else 36,weight=700,extra='letter-spacing="-1.2"')+arrow(w-53,29,'silver')
    s+=research_art(57 if m else 25,112 if m else 192,1.02 if m else 1)
    if not m:
        s+=label(36,112,'07 PAPERS & MANUSCRIPTS','muted',10)+'<path d="M330 132V590" stroke="var(--line)"/>'
    mobile_y=569
    for i,paper in enumerate(PAPERS):
        xx=24 if m else 366; yy=mobile_y if m else 153+i*65
        color={'published':'ruby','accepted':'silver','submitted':'muted'}[paper['status']]
        titles=paper.get('mobile',[paper['short']]) if m else [paper['short']]
        for j,title in enumerate(titles):
            s+=t(xx,yy+j*24,title,19 if m else 21,weight=600,extra='letter-spacing="-.35"')
        status_y=yy+(len(titles)-1)*24+23
        s+=t(xx,status_y,f"{paper['status'].upper()} · {paper['venue']}",10.5 if m else 12,color,500,'class="mono"')
        if i<len(PAPERS)-1:
            s+=rule(xx,status_y+14,376 if m else 963)
        mobile_y=status_y+36
    for i,(status,color) in enumerate([('published','ruby'),('accepted','silver'),('submitted','muted')]):
        count=sum(paper['status']==status for paper in PAPERS)
        xx=24+i*121 if m else 36+i*314; yy=474 if m else 619; ww=110 if m else 300
        s+=f'<rect x="{xx}" y="{yy}" width="{ww}" height="{54 if m else 40}" rx="9" fill="var(--panel)" stroke="var(--line)"/>'
        s+=t(xx+12,yy+(26 if m else 27),f'{count:02}',24 if m else 25,color,600)
        s+=label(xx+12 if m else xx+53,yy+43 if m else yy+25,status.upper(),color,8 if m else 9)
    return w,h,s

STACK_GROUPS = [
    dict(name='Programming & ML Tools',
         items=['Python', 'SQL', 'PyTorch', 'TensorFlow', 'scikit-learn', 'OpenCV'],
         mobile=['Python / SQL / PyTorch', 'TensorFlow / scikit-learn', 'OpenCV']),
    dict(name='AI Domains',
         items=['Machine Learning', 'Computer Vision', 'Natural Language Processing', 'Reinforcement Learning', 'Multimodal Learning', 'Time-Series Modeling'],
         desktop=['Machine Learning / Computer Vision / Natural Language Processing', 'Reinforcement Learning / Multimodal Learning / Time-Series Modeling'],
         mobile=['Machine Learning / Computer Vision', 'Natural Language Processing', 'Reinforcement Learning', 'Multimodal Learning', 'Time-Series Modeling']),
    dict(name='LLM & Agentic Systems',
         items=['LangChain', 'LangGraph', 'Retrieval-Augmented Generation (RAG)', 'Tool Calling'],
         mobile=['LangChain / LangGraph', 'Retrieval-Augmented', 'Generation (RAG)', 'Tool Calling']),
    dict(name='Backend & Engineering',
         items=['FastAPI', 'REST APIs', 'PostgreSQL', 'SQL Server', 'ETL Pipelines', 'Git'],
         mobile=['FastAPI / REST APIs', 'PostgreSQL / SQL Server', 'ETL Pipelines / Git']),
    dict(name='Languages & Strengths',
         items=['English (B2)', 'Analytical Thinking', 'Problem Solving'],
         mobile=['English (B2)', 'Analytical Thinking', 'Problem Solving']),
]

def stack_glyph(index, x, y):
    s=f'<g transform="translate({x} {y})">'
    if index==0:
        for yy in [5,18,31]:
            s += profile_signal(f'M3 {yy}L22 18L39 {36-yy}', 'silver', yy/20, 1.4)
        for xx,yy in [(3,5),(3,18),(3,31),(22,18),(39,5),(39,18),(39,31)]:
            s += f'<circle class="prof-pulse" cx="{xx}" cy="{yy}" r="2.5" fill="var(--ruby)" style="animation-delay:-{xx*.05}s"/>'
    elif index==1:
        for row in range(4):
            for col in range(5):
                s += f'<rect class="prof-pulse" x="{col*8}" y="{row*9}" width="4" height="5" rx="1" fill="var(--{"ruby" if col==2 else "silver"})" style="animation-delay:-{(row+col)*.35}s"/>'
    elif index==2:
        s += '<path d="M12 2H6V13L2 18L6 23V34H12M29 2H35V13L39 18L35 23V34H29" fill="none" stroke="var(--silver)" stroke-width="1.4"/>'
        s += profile_signal('M11 18H30', 'ruby', 0, 2.3)
    elif index==3:
        for i in range(3):
            s += f'<g class="prof-rack" style="animation-delay:-{i*.5}s"><rect x="2" y="{i*12}" width="36" height="9" rx="2" fill="none" stroke="var(--silver)"/><circle class="prof-pulse" cx="8" cy="{4.5+i*12}" r="1.5" fill="var(--ruby)"/><path d="M15 {4.5+i*12}H31" stroke="var(--ruby)" stroke-opacity=".4"/></g>'
    else:
        s += '<path d="M7 2H34Q40 2 40 8V23Q40 29 34 29H17L8 36V29H7Q1 29 1 23V8Q1 2 7 2Z" fill="none" stroke="var(--silver)" stroke-width="1.3"/>'
        s += t(21, 19, 'B2', 12, 'ruby', 600, 'class="mono" text-anchor="middle"')
        for i in range(3):
            s += f'<circle class="prof-pulse" cx="{15+i*6}" cy="24" r="1" fill="var(--ruby)" style="animation-delay:-{i*.4}s"/>'
    return s+'</g>'

def toolkit(m):
    rows = []
    yy = 142 if m else 116
    for group in STACK_GROUPS:
        text_lines = group['mobile'] if m else group.get('desktop', [' / '.join(group['items'])])
        hh = (64 if m else 84)+(len(text_lines)-1)*(21 if m else 25)
        rows.append((group, text_lines, yy, hh))
        yy += hh+12
    w, h = (400 if m else 1000), yy+12
    p = 24 if m else 36
    s = profile_defs() + panel(w, h, 'panel') + label(p, 32, 'THE TOOLKIT', 'ruby', 10 if m else 12)
    if m:
        s += lines(p-1, 77, ['A practical stack,', 'tied to real work.'], 28, 'ink', 32, 700)
    else:
        s += t(p-1, 77, 'A practical stack, tied to real work.', 34, weight=700, extra='letter-spacing="-1.2"')
    for i,(group,text_lines,yy,hh) in enumerate(rows):
        ww=352 if m else 928
        s += f'<rect x="{p}" y="{yy}" width="{ww}" height="{hh}" rx="10" fill="var(--bg)" stroke="var(--line)"/>'
        s += stack_glyph(i, p+14, yy+(hh-36)/2)
        s += t(p+71, yy+25, group['name'], 14 if m else 16, 'silver', 600)
        s += lines(p+71, yy+50 if m else yy+55, text_lines, 14 if m else 16.5, 'ink', 21 if m else 25)
        if not m:
            for j in range(7):
                s += f'<rect class="prof-pulse" x="{873+j*9}" y="{yy+16}" width="4" height="12" rx="2" fill="var(--ruby)" style="animation-delay:-{i*.5+j*.2}s"/>'
        s += f'<defs><clipPath id="stack-lane-{i}"><rect x="{p+8}" y="{yy+hh-4}" width="{ww-16}" height="2"/></clipPath></defs><g clip-path="url(#stack-lane-{i})"><g transform="translate({p-92} {yy+hh-4})"><rect class="prof-sweep" width="100" height="2" fill="url(#prof-sweep-fill)" style="--travel:{ww+100}px;animation-delay:-{i*1.5}s"/></g></g>'
    return (w, h, s)

def footer(m):
    w,h=(400,368) if m else (1000,270)
    p=24 if m else 36
    s=signature_motion()+panel(w,h)+label(p,34,'OPEN TO AI ENGINEERING OPPORTUNITIES','ruby',9 if m else 12)
    if m:
        s+=signature_title('footer-title',[(21,106,'let’s build',48,700,-2),(21,158,'what’s next.',48,700,-2)],(20,67,275,98),8)
        s+=connection_iris(349,193,17)+t(p,207,'nxt276651@gmail.com ↗',18,'silver',500)
        s+=lines(p,252,['Part-time through Jun 2027.','Full-time from Jul 2027.'],15,step=23)+rule(24,296,376)+lines(p,324,['B.Sc. AI · FPT University · GPA 3.75/4.0','Expected graduation: Jun 2027'],13,step=21)
        route='M24 219H267'
    else:
        s+=signature_title('footer-title',[(31,112,'let’s build what’s next.',58,700,-3)],(29,65,750,65),8)
        s+=connection_iris(926,97,28)+t(p,157,'nxt276651@gmail.com ↗',22,'silver',500)+t(p,196,'Part-time through Jun 2027 · Full-time from Jul 2027',17,'muted')
        s+=rule(36,217,962)+t(p,248,'B.Sc. AI · FPT University · GPA 3.75/4.0 · Expected graduation: Jun 2027',14,'muted')
        route='M36 171H321'
    s+=f'<path d="{route}" stroke="var(--silver)" stroke-opacity=".14"/><path class="signature-packet" pathLength="100" d="{route}" fill="none" stroke="var(--ruby)" stroke-width="1.4"/>'
    return w,h,s
BUILDERS = {'hero': hero, 'work': work, 'tracevision': lambda m: project('tracevision', m), 'knowledge': lambda m: project('knowledge', m), 'aqb': lambda m: project('aqb', m), 'datu': lambda m: project('datu', m), 'experience': experience, 'research': research, 'toolkit': toolkit, 'footer': footer}
MOVING = {'hero', 'tracevision', 'knowledge', 'aqb', 'datu', 'experience', 'research', 'toolkit', 'footer'}

def generate_outputs():
    outputs={}
    for theme in THEMES:
        for name,builder in BUILDERS.items():
            for mobile in (False,True):
                width,height,body=builder(mobile)
                size='mobile' if mobile else 'desktop'
                for static in (False,True) if name in MOVING else (False,):
                    suffix='-still' if static else ''
                    outputs[f'{name}-{theme}-{size}{suffix}.svg']=svg(name,width,height,body,theme,static)
        for name,caption in [('portfolio','Portfolio'),('resume','Résumé'),('linkedin','LinkedIn'),('email','Email')]:
            primary=name=='portfolio'
            fill='url(#cr-metal)' if primary else 'url(#cr-glass)'
            body=f'<rect x=".75" y=".75" width="158.5" height="44.5" rx="9" fill="{fill}" stroke="url(#cr-edge)" stroke-width="1.5"/>'
            body+=t(14,29,caption,16,'navink' if primary else 'ink',600)+arrow(131,16,'ruby')
            outputs[f'nav-{name}-{theme}.svg']=svg(caption,160,46,body,theme,True)
    return outputs

def material_defs(theme):
    dark = theme == 'dark'
    edge = ['#303c4e', '#dce6f5', '#586579', '#f6faff', '#4c5666'] if dark else ['#8b99ab', '#ffffff', '#abb8c8', '#ffffff', '#8a9bb1']
    metal = ['#f9fcff', '#9fabbc', '#e7eef8', '#6d7b91', '#d7e1ef'] if dark else ['#ffffff', '#b5c1d0', '#f9fcff', '#a2afc0', '#edf2f8']
    typography = ['#ffffff', '#e2e8f0', '#939fb1', '#f6f9ff'] if dark else ['#182332', '#526278', '#253448', '#162134']
    stops = lambda values: ''.join(f'<stop offset="{i/(len(values)-1):.3f}" stop-color="{v}"/>' for i,v in enumerate(values))
    return f'''<defs>
      <linearGradient id="cr-edge" x1="0" y1="0" x2="1" y2="1">{stops(edge)}</linearGradient>
      <linearGradient id="cr-metal" x1="0" y1="0" x2=".3" y2="1">{stops(metal)}</linearGradient>
      <linearGradient id="cr-type" x1="0" y1="0" x2=".1" y2="1">{stops(typography)}</linearGradient>
      <linearGradient id="cr-panel" x1="0" y1="0" x2=".8" y2="1"><stop stop-color="var(--panel)"/><stop offset=".55" stop-color="var(--bg)"/><stop offset="1" stop-color="var(--panel)"/></linearGradient>
      <linearGradient id="cr-glass" x1="0" y1="0" x2="1" y2="1"><stop stop-color="var(--soft)"/><stop offset=".45" stop-color="var(--bg)"/><stop offset="1" stop-color="var(--panel)"/></linearGradient>
      <linearGradient id="cr-red" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#8d0829"/><stop offset=".4" stop-color="#ff7289"/><stop offset=".54" stop-color="#cf173d"/><stop offset="1" stop-color="#530e23"/></linearGradient>
      <linearGradient id="cr-sheen"><stop stop-color="#fff" stop-opacity="0"/><stop offset=".48" stop-color="#fff" stop-opacity=".7"/><stop offset=".51" stop-color="#fff" stop-opacity="1"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
      <radialGradient id="cr-aura"><stop stop-color="var(--ruby)" stop-opacity=".3"/><stop offset=".52" stop-color="var(--ruby)" stop-opacity=".09"/><stop offset="1" stop-color="var(--ruby)" stop-opacity="0"/></radialGradient>
      <filter id="cr-glow" x="-90%" y="-90%" width="280%" height="280%"><feGaussianBlur stdDeviation="2.4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
      <pattern id="cr-grain" width="4" height="4" patternUnits="userSpaceOnUse"><path d="M0 .5H4" stroke="var(--silver)" stroke-opacity=".025"/></pattern>
      <radialGradient id="haze"><stop stop-color="var(--ruby)" stop-opacity=".2"/><stop offset="1" stop-color="var(--ruby)" stop-opacity="0"/></radialGradient>
      <linearGradient id="scan-grad"><stop stop-color="var(--ruby)" stop-opacity="0"/><stop offset="1" stop-color="var(--ruby)" stop-opacity=".28"/></linearGradient>
    </defs>'''

def enhance_art(markup):
    """Add a machined instrument surface and stronger packet trails to each scene."""
    first = markup.index('>')+1
    frame = '<rect x="-5" y="-6" width="286" height="218" rx="20" fill="url(#cr-glass)" stroke="url(#cr-edge)" stroke-opacity=".4"/><path d="M8 19V7H29M247 7H269V19M269 182V199H251M27 199H8V182" fill="none" stroke="var(--ruby)" stroke-opacity=".6" stroke-width="1.4"/>'
    frame += '<path class="cr-trace" pathLength="100" d="M13 -6H261Q281 -6 281 14V193Q281 212 261 212H15Q-5 212 -5 193V14Q-5 -6 13 -6Z" fill="none" stroke="var(--ruby)" stroke-width="1.5"/>'
    markup = markup[:first]+frame+markup[first:]
    markup = markup.replace('stroke="var(--silver)"','stroke="url(#cr-edge)"')
    markup = markup.replace('fill="var(--panel)"','fill="url(#cr-glass)"')
    return markup

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Check assets without rewriting them.')
    args = parser.parse_args()
    outputs = generate_outputs()
    stale = []
    for name, content in outputs.items():
        path = OUT / name
        if args.check:
            if not path.exists() or path.read_text(encoding='utf-8') != content:
                stale.append(path.relative_to(ROOT).as_posix())
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding='utf-8', newline='\n')
    if stale:
        print('Out-of-date Chrome / Ruby assets:', file=sys.stderr)
        print('\n'.join(stale), file=sys.stderr)
        return 1
    print(f'Chrome / Ruby: {len(outputs)} assets ' + ('are up to date.' if args.check else 'generated.'))
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
