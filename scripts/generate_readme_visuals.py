"""Generate the SVG assets used by README.md. Run with --check to verify generated files."""

import argparse
import math
import sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets' / 'neon-lab'
THEMES = {'dark': dict(bg='#111218', panel='#181a22', line='#323541', ink='#f2f2f7', muted='#a6abba', lime='#d2fa69', violet='#b1a0ff', soft='#232333'), 'light': dict(bg='#f5f5f0', panel='#ffffff', line='#d3d5cc', ink='#20222b', muted='#5a6270', lime='#587d13', violet='#7356bf', soft='#e9e5f5')}

def t(x, y, s, size=18, c='ink', weight=400, extra=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="var(--{c})" font-weight="{weight}" {extra}>{escape(s)}</text>'

def lines(x, y, ss, size=18, c='muted', step=26, weight=400):
    return ''.join((t(x, y + i * step, s, size, c, weight) for i, s in enumerate(ss)))

def label(x, y, s, c='muted', size=12):
    return t(x, y, s, size, c, 500, 'class="mono" letter-spacing="1.1"')

def panel(w, h, c='bg'):
    return f'<rect x=".75" y=".75" width="{w - 1.5}" height="{h - 1.5}" rx="22" fill="var(--{c})" stroke="var(--line)" stroke-width="1.5"/>'

def rule(x, y, xx):
    return f'<path d="M{x} {y}H{xx}" stroke="var(--line)"/>'

def arrow(x, y, c='muted'):
    return f'<path d="M{x} {y + 12}L{x + 12} {y}M{x} {y}H{x + 12}V{y + 12}" fill="none" stroke="var(--{c})" stroke-width="1.7"/>'

def star(x, y, r=16, c='lime', moving=False):
    pts = []
    for i in range(16):
        a = i * math.pi / 8
        rr = r if i % 2 == 0 else r * 0.46
        pts.append(f'{rr * math.cos(a):.2f},{rr * math.sin(a):.2f}')
    return f'<g transform="translate({x} {y})"><polygon class="{('star-spin' if moving else '')}" points="{' '.join(pts)}" fill="var(--{c})"/></g>'
CSS = """text{font-family:Arial,"Segoe UI",sans-serif}
.mono{font-family:Consolas,"Courier New",monospace}
.star-spin{animation:spin 18s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}"""

def svg(name, w, h, body, theme, static=False):
    colors = THEMES[theme]
    variables = ';'.join((f'--{k}:{v}' for k, v in colors.items()))
    style = CSS + '@media (prefers-reduced-motion: reduce){*{animation:none!important}}' + ('*{animation:none!important}' if static else '')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc" style="{variables}">\n<title id="title">{escape(name)}</title><desc id="desc">AI engineering profile. Written content stays visible; motion is decorative.</desc><defs><style>{style}</style>\n<radialGradient id="haze"><stop stop-color="{colors['violet']}" stop-opacity=".15"/><stop offset="1" stop-color="{colors['violet']}" stop-opacity="0"/></radialGradient>\n<linearGradient id="scan-grad"><stop stop-color="{colors['lime']}" stop-opacity="0"/><stop offset="1" stop-color="{colors['lime']}" stop-opacity=".2"/></linearGradient>\n</defs>{body}</svg>'

def brain_art(x, y, scale=1):
    """A multimodal brain: inputs, scanning activations, then generated tokens.

    CSS-only choreography keeps the complete scene still in reduced-motion
    variants. All geometry stays inside the existing hero illustration area.
    """
    definitions = '''<defs>
      <style>
        .brain-float{animation:brain-float 5.4s ease-in-out infinite}
        .brain-aura{opacity:.55;animation:brain-aura 2.7s ease-in-out infinite}
        .brain-packet{stroke-dasharray:12 88;animation:brain-packet 1.8s linear infinite}
        .brain-contour{stroke-dasharray:135 865;animation:brain-contour 2.7s linear infinite}
        .brain-synapse{opacity:.7;animation:brain-synapse 2.7s ease-in-out infinite}
        .brain-halo{opacity:.16;transform-box:fill-box;transform-origin:center;animation:brain-halo 2.7s ease-out infinite}
        .brain-scan{animation:brain-scan 2.7s ease-in-out infinite alternate}
        .brain-echo{opacity:0;animation:brain-echo 2.7s ease-out infinite}
        .brain-input{animation:brain-input 2.7s ease-in-out infinite}
        .brain-wave{transform-box:fill-box;transform-origin:center;animation:brain-wave .9s ease-in-out infinite alternate}
        .brain-phase{opacity:0;animation:brain-phase 5.4s linear infinite}
        .brain-phase:first-child{opacity:1}
        .brain-reveal{transform:scaleX(1);animation:brain-reveal 5.4s steps(23,end) infinite}
        .brain-caret{opacity:.8;transform:translateX(190px);animation:brain-caret 5.4s steps(23,end) infinite}
        .brain-scene .star-spin{animation-duration:10.8s}
        .brain-progress{stroke-dasharray:18 82;animation:brain-packet 1.35s linear infinite}
        @keyframes brain-float{0%,100%{transform:translateY(3px) rotate(-2deg)}50%{transform:translateY(-5px) rotate(2deg)}}
        @keyframes brain-aura{0%,100%{opacity:.35}50%{opacity:.9}}
        @keyframes brain-packet{from{stroke-dashoffset:100}to{stroke-dashoffset:0}}
        @keyframes brain-contour{from{stroke-dashoffset:1000}to{stroke-dashoffset:0}}
        @keyframes brain-synapse{0%,100%{opacity:.22}30%,46%{opacity:1}70%{opacity:.4}}
        @keyframes brain-halo{0%{transform:scale(.45);opacity:0}30%{opacity:.45}75%,100%{transform:scale(2.2);opacity:0}}
        @keyframes brain-scan{from{transform:translateY(-10px)}to{transform:translateY(198px)}}
        @keyframes brain-echo{0%{transform:scale(.96);opacity:0}20%{opacity:.26}100%{transform:scale(1.2);opacity:0}}
        @keyframes brain-input{0%,100%{transform:translateX(0);opacity:.65}30%,52%{transform:translateX(5px);opacity:1}}
        @keyframes brain-wave{from{transform:scaleY(.3)}to{transform:scaleY(1)}}
        @keyframes brain-phase{0%,29%{opacity:1}33.3%,100%{opacity:0}}
        @keyframes brain-reveal{0%,38%{transform:scaleX(0)}82%,96%{transform:scaleX(1)}100%{transform:scaleX(0)}}
        @keyframes brain-caret{0%,38%{transform:translateX(0);opacity:1}82%,96%{transform:translateX(190px);opacity:1}100%{transform:translateX(0);opacity:0}}
      </style>
      <radialGradient id="brain-aura"><stop stop-color="var(--violet)" stop-opacity=".35"/><stop offset=".6" stop-color="var(--violet)" stop-opacity=".12"/><stop offset="1" stop-color="var(--violet)" stop-opacity="0"/></radialGradient>
      <linearGradient id="brain-surface" x1="0" y1="0" x2="1" y2="1"><stop stop-color="var(--violet)" stop-opacity=".13"/><stop offset=".55" stop-color="var(--violet)" stop-opacity=".035"/><stop offset="1" stop-color="var(--lime)" stop-opacity=".14"/></linearGradient>
      <linearGradient id="brain-spectrum"><stop stop-color="var(--violet)"/><stop offset=".5" stop-color="var(--ink)"/><stop offset="1" stop-color="var(--lime)"/></linearGradient>
      <linearGradient id="brain-scan-fill" x1="0" y1="0" x2="0" y2="1"><stop stop-color="var(--lime)" stop-opacity="0"/><stop offset="1" stop-color="var(--lime)" stop-opacity=".24"/></linearGradient>
      <filter id="brain-glow" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="1.4" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
      <clipPath id="brain-output-clip"><rect class="brain-reveal" x="0" y="-19" width="190" height="25"/></clipPath>
    </defs>'''
    # Two explicitly drawn hemispheres make the silhouette readable at profile size.
    hemisphere = 'M-4 -78C-12 -98 -31 -105 -49 -96C-73 -103 -94 -91 -97 -72C-119 -65 -127 -43 -116 -25C-131 -4 -125 17 -112 29C-117 50 -100 70 -80 68C-70 91 -45 98 -28 81C-12 80 -4 66 -4 48Z'
    folds = [
        'M-49 -96C-62 -78 -38 -69 -43 -52S-73 -34 -61 -13C-55 -4 -41 -8 -36 3',
        'M-97 -72C-77 -73 -65 -62 -72 -47C-79 -34 -95 -36 -97 -17S-83 4 -73 2',
        'M-116 -25C-101 -29 -85 -16 -91 -2C-99 16 -83 29 -68 22S-42 21 -40 38',
        'M-112 29C-94 25 -88 37 -89 50S-77 65 -65 58C-48 48 -29 53 -28 81',
        'M-5 -66C-23 -75 -28 -58 -21 -46S-12 -21 -26 -16C-39 -11 -48 -19 -46 -32',
        'M-5 4C-25 -5 -24 15 -17 27S-9 51 -26 55',
        'M-80 68C-80 83 -58 84 -51 72',
    ]
    brain_paths = f'<path d="{hemisphere}"/><path d="{hemisphere}" transform="scale(-1 1)"/>'
    definitions += f'<defs><clipPath id="brain-shape">{brain_paths}</clipPath></defs>'
    shell = '<ellipse class="brain-aura" cx="15" cy="-18" rx="169" ry="148" fill="url(#brain-aura)"/>'
    shell += label(-154, -143, 'AI / MULTIMODAL', 'violet', 10)
    for i in range(3):
        shell += f'<circle class="brain-synapse" cx="{132 + i * 9}" cy="-147" r="2" fill="var(--lime)" style="animation-delay:-{i * .3}s"/>'
    # Registration corners and a faint field give the brain room to move.
    shell += '<path d="M-128 -118H-140V-106M147 -118H159V-106M-128 84H-140V72M147 84H159V72" fill="none" stroke="var(--line)"/>'
    for gx in range(-125, 157, 16):
        for gy in range(-107, 86, 16):
            shell += f'<circle cx="{gx}" cy="{gy}" r=".6" fill="var(--violet)" opacity=".12"/>'

    # Irregular, deterministic synapses, clipped to the organic silhouette.
    points = []
    for row in range(8):
        for col in range(9):
            px = -102 + col * 25 + math.sin(row * 7 + col * 3) * 6
            py = -83 + row * 24 + math.cos(col * 4 + row * 2) * 5
            if (px / 113) ** 2 + (py / 98) ** 2 < 1.03:
                points.append((px, py))
    edges, nodes = [], []
    for index, (px, py) in enumerate(points):
        color = 'violet' if px < -12 else 'lime'
        delay = -(index * .137) % 2.7
        near = sorted([(j, qx, qy) for j, (qx, qy) in enumerate(points) if j > index], key=lambda q: (q[1] - px) ** 2 + (q[2] - py) ** 2)[:2]
        for branch, (_, qx, qy) in enumerate(near):
            if math.hypot(qx - px, qy - py) > 45:
                continue
            route = f'M{px:.2f} {py:.2f}L{qx:.2f} {qy:.2f}'
            edges.append(f'<path d="{route}" stroke="var(--{color})" stroke-opacity=".19" stroke-width=".65"/>')
            if (index + branch) % 2 == 0:
                edges.append(f'<path class="brain-packet" d="{route}" pathLength="100" stroke="var(--{color})" stroke-width="1.9" stroke-linecap="round" style="animation-delay:-{delay:.2f}s"/>')
        nodes.append(f'<g transform="translate({px:.2f} {py:.2f})"><circle class="brain-synapse" r="{2.3 if index % 4 == 0 else 1.35}" fill="var(--{color})" style="animation-delay:-{delay:.2f}s"/>')
        if index % 4 == 0:
            nodes.append(f'<circle class="brain-halo" r="6" fill="var(--{color})" style="animation-delay:-{delay:.2f}s"/><circle r="4" fill="none" stroke="var(--{color})" stroke-width=".5" opacity=".5"/>')
        nodes.append('</g>')
    brain = '<g transform="translate(17 -18) scale(.95)"><g class="brain-float">'
    brain += '<path d="M-17 72Q-10 84 -11 104Q0 115 11 104Q10 84 17 72" fill="url(#brain-surface)" stroke="var(--violet)" stroke-opacity=".45"/>'
    brain += f'<g class="brain-echo" fill="none" stroke="var(--violet)" stroke-width=".9">{brain_paths}</g>'
    brain += f'<g fill="url(#brain-surface)" stroke="url(#brain-spectrum)" stroke-width="1.8" stroke-opacity=".7">{brain_paths}</g>'
    brain += '<g clip-path="url(#brain-shape)">' + ''.join(edges) + ''.join(nodes)
    for sign in (1, -1):
        brain += f'<g transform="scale({sign} 1)" fill="none" stroke="var(--{"violet" if sign == 1 else "lime"})" stroke-linecap="round">'
        for index, route in enumerate(folds):
            brain += f'<path d="{route}" stroke-width="1.3" stroke-opacity=".55"/><path class="brain-packet" d="{route}" pathLength="100" stroke-width="2.5" style="animation-delay:-{index * .27:.2f}s" filter="url(#brain-glow)"/>'
        brain += '</g>'
    brain += '<g class="brain-scan"><rect x="-132" y="-129" width="264" height="35" fill="url(#brain-scan-fill)"/><path d="M-132 -94H132" stroke="var(--lime)" stroke-width="1.5" filter="url(#brain-glow)"/></g></g>'
    brain += f'<g fill="none" stroke="url(#brain-spectrum)" stroke-width="2.8" filter="url(#brain-glow)"><path class="brain-contour" pathLength="1000" d="{hemisphere}"/><path class="brain-contour" pathLength="1000" d="{hemisphere}" transform="scale(-1 1)" style="animation-delay:-1.8s"/></g>'
    brain += '<path class="brain-packet" pathLength="100" d="M0 -74V98" stroke="var(--lime)" stroke-width="2" filter="url(#brain-glow)"/></g></g>'

    inputs = ''
    for index, yy in enumerate([-79, -25, 29]):
        route = f'M-133 {yy}C-107 {yy} -113 {yy - 12} -78 {yy - 12}'
        inputs += f'<path d="{route}" fill="none" stroke="var(--violet)" stroke-opacity=".4"/><path class="brain-packet" pathLength="100" d="{route}" fill="none" stroke="var(--violet)" stroke-width="2.6" style="animation-delay:-{index * .42}s" filter="url(#brain-glow)"/>'
        inputs += f'<g transform="translate(-153 {yy})"><g class="brain-input" style="animation-delay:-{index * .42}s"><rect x="-17" y="-17" width="34" height="34" rx="9" fill="var(--panel)" stroke="var(--violet)" stroke-opacity=".65"/>'
        if index == 0:
            inputs += t(-9, 6, 'T', 19, 'ink', 700) + '<path d="M5 8H11" stroke="var(--lime)" stroke-width="2"/>'
        elif index == 1:
            inputs += '<rect x="-10" y="-9" width="20" height="18" rx="3" fill="none" stroke="var(--ink)" stroke-width="1.3"/><circle cx="4" cy="-4" r="2" fill="var(--lime)"/><path d="M-8 6L-2 -1L4 6L8 2" fill="none" stroke="var(--violet)" stroke-width="1.4"/>'
        else:
            for col, hh in enumerate([8, 17, 24, 14, 9]):
                inputs += f'<rect class="brain-wave" x="{-10 + col * 4.5}" y="{-hh / 2}" width="2" height="{hh}" rx="1" fill="var(--lime)" style="animation-delay:-{col * .15}s"/>'
        inputs += '</g></g>'
    output = '<path d="M137 -16H152V73Q152 90 137 90H89" fill="none" stroke="var(--lime)" stroke-opacity=".28"/>'
    output += '<path class="brain-progress" pathLength="100" d="M137 -16H152V73Q152 90 137 90H89" fill="none" stroke="var(--lime)" stroke-width="2.3" filter="url(#brain-glow)"/>'
    output += '<g>'
    for index, caption in enumerate(['01 / PERCEIVE', '02 / REASON', '03 / GENERATE']):
        output += f'<g class="brain-phase" style="animation-delay:{index * 1.8}s">' + t(12, 103, caption, 10, 'lime', 500, 'class="mono" text-anchor="middle" letter-spacing="1.6"') + '</g>'
    output += '</g><rect x="-116" y="116" width="257" height="39" rx="10" fill="var(--panel)" stroke="var(--line)"/>'
    output += star(-98, 136, 7, 'lime', True)
    output += '<g transform="translate(-79 141)"><g clip-path="url(#brain-output-clip)">' + t(0, 0, 'see. reason. create.', 14, 'ink', 500, 'class="mono" textLength="185" lengthAdjust="spacingAndGlyphs"') + '</g><path class="brain-caret" d="M0 -12V3" stroke="var(--lime)" stroke-width="1.7"/></g>'
    return definitions + f'<g class="brain-scene" transform="translate({x} {y}) scale({scale})">' + shell + brain + inputs + output + '</g>'

def hero(m):
    w, h = (400, 548) if m else (1000, 440)
    s = panel(w, h) + label(26 if m else 38, 36, 'NGUYEN XUAN TRUNG', size=11 if m else 12) + star(w - 34, 31, 11, moving=True)
    if m:
        s += t(25, 105, 'xuan trung.', 55, weight=750, extra='letter-spacing="-3"') + label(26, 136, 'AI ENGINEER / HCMC, VIETNAM', 'lime', 10) + brain_art(200, 286, 0.82)
        s += t(26, 438, 'Curiosity, engineered.', 25, weight=700, extra='letter-spacing="-1"') + lines(26, 470, ['Evidence-grounded AI. Multimodal search.', 'RAG systems built to be inspected.'], 15, step=23) + label(26, 523, 'BUILD / EVALUATE / ITERATE', 'violet', 10)
    else:
        s += label(38, 83, 'AI ENGINEER / HCMC, VIETNAM', 'lime') + t(32, 184, 'xuan', 112, weight=750, extra='letter-spacing="-7"') + t(32, 286, 'trung.', 112, weight=750, extra='letter-spacing="-7"')
        s += t(39, 332, 'Curiosity, engineered.', 25, weight=600, extra='letter-spacing="-.7"') + lines(40, 371, ['Evidence-grounded AI. Multimodal search.', 'RAG systems built to be inspected.'], 18, step=27) + brain_art(755, 210, 1.12) + label(623, 403, 'BUILD / EVALUATE / ITERATE', 'violet')
    return (w, h, s)

def work(m):
    w, h = (400, 92) if m else (1000, 100)
    return (w, h, label(8, 24, '01 / SELECTED SYSTEMS', 'lime', 10 if m else 12) + t(6, 68, 'Proof of work.', 32 if m else 44, weight=700, extra='letter-spacing="-1.8"') + label(w - 47, 66, '[04]', size=12))

def project_defs():
    """Local animation vocabulary shared by the four project illustrations."""
    return '''<defs><style>
      .sys-packet{stroke-dasharray:14 86;animation:sys-packet 1.5s linear infinite}
      .sys-float{animation:sys-float 3s ease-in-out infinite alternate}
      .sys-fire{opacity:.7;animation:sys-fire 3s ease-in-out infinite}
      .sys-halo{transform-box:fill-box;transform-origin:center;opacity:.16;animation:sys-halo 3s ease-out infinite}
      .sys-scan-x{animation:sys-scan-x 3s ease-in-out infinite alternate}
      .sys-track{animation:sys-track 6s ease-in-out infinite}
      .sys-wave{transform-box:fill-box;transform-origin:center;animation:sys-wave .75s ease-in-out infinite alternate}
      .sys-playhead{animation:sys-playhead 6s linear infinite}
      .sys-paper{animation:sys-paper 3s ease-in-out infinite alternate}
      .sys-chunk{opacity:.8;animation:sys-chunk 3s ease-in-out infinite}
      .sys-answer{transform:scaleX(1);animation:sys-answer 6s ease-in-out infinite}
      .sys-scan-y{animation:sys-scan-y 3s ease-in-out infinite alternate}
      .sys-compress{opacity:.7;animation:sys-compress 1.5s ease-in infinite}
      .sys-chip{animation:sys-chip 3s ease-in-out infinite}
      .sys-check{stroke-dasharray:100;stroke-dashoffset:0;animation:sys-check 3s ease-in-out infinite}
      .sys-runner{transform:translate(192px,39px);animation:sys-runner 6s linear infinite}
      .sys-rank{transform:scaleX(1);animation:sys-rank 3s ease-in-out infinite}
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
    <filter id="sys-glow" x="-70%" y="-70%" width="240%" height="240%"><feGaussianBlur stdDeviation="1.2" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <linearGradient id="sys-scan-y" x1="0" y1="0" x2="0" y2="1"><stop stop-color="var(--lime)" stop-opacity="0"/><stop offset="1" stop-color="var(--lime)" stop-opacity=".3"/></linearGradient>
    </defs>'''

def signal(route, c='lime', width=2.2, delay=0):
    return f'<path d="{route}" fill="none" stroke="var(--{c})" stroke-opacity=".24"/><path class="sys-packet" d="{route}" pathLength="100" fill="none" stroke="var(--{c})" stroke-width="{width}" stroke-linecap="round" filter="url(#sys-glow)" style="animation-delay:-{delay}s"/>'

def art_footer(captions):
    s = signal('M19 212H261', 'violet', 1.8)
    for i, caption in enumerate(captions):
        cx = [19, 140, 261][i]
        s += f'<circle cx="{cx}" cy="212" r="3" fill="var(--bg)" stroke="var(--lime)"/><circle class="sys-fire" cx="{cx}" cy="212" r="1.7" fill="var(--lime)" style="animation-delay:-{i}s"/>'
        s += t(cx, 231, caption, 8.5, 'muted', 500, f'class="mono" text-anchor="{["start", "middle", "end"][i]}" letter-spacing=".5"')
    return s

def video_art(x, y, scale=1):
    s = f'<g transform="translate({x} {y}) scale({scale})"><ellipse cx="141" cy="102" rx="144" ry="115" fill="url(#haze)"/>'
    s += '<g class="sys-float"><rect x="35" y="10" width="227" height="139" rx="12" fill="var(--soft)" stroke="var(--line)"/></g><rect x="25" y="20" width="228" height="140" rx="12" fill="var(--panel)" stroke="var(--violet)" stroke-opacity=".3"/><rect x="14" y="30" width="228" height="141" rx="12" fill="var(--bg)" stroke="var(--violet)" stroke-opacity=".65"/>'
    s += '<defs><clipPath id="video-window"><rect x="15" y="31" width="226" height="139" rx="11"/></clipPath></defs><g clip-path="url(#video-window)">'
    for i, hh in enumerate([43, 72, 53, 89, 67, 42, 75]):
        s += f'<rect x="{24+i*31}" y="{146-hh}" width="24" height="{hh}" rx="2" fill="var(--soft)" opacity=".45"/>'
    for yy in [55, 80, 105, 130, 155]:
        s += f'<path d="M18 {yy}H240" stroke="var(--line)" stroke-width=".55"/>'
    s += '<g transform="translate(46 71)"><g class="sys-track"><circle cx="21" cy="16" r="9" fill="var(--violet)" opacity=".7"/><path d="M7 54Q5 30 21 30Q37 30 35 54M15 54L11 73M27 54L32 73" fill="none" stroke="var(--violet)" stroke-width="7" stroke-linecap="round" opacity=".6"/><rect x="0" y="0" width="43" height="81" rx="4" fill="var(--lime)" fill-opacity=".035" stroke="var(--lime)" stroke-width="1.4"/><path d="M-3 11V-3H10M33 -3H46V11M46 70V84H33M10 84H-3V70" fill="none" stroke="var(--lime)" stroke-width="2.3"/>'
    s += label(2, -7, 'TRACK', 'lime', 7) + '</g></g>'
    s += '<rect x="181" y="108" width="32" height="36" rx="4" fill="var(--violet)" fill-opacity=".08" stroke="var(--violet)" stroke-dasharray="3 3"/><g class="sys-scan-x"><rect x="-9" y="32" width="28" height="136" fill="url(#scan-grad)"/><path d="M19 32V168" stroke="var(--lime)" stroke-width="2" filter="url(#sys-glow)"/></g></g>'
    s += '<rect x="30" y="43" width="37" height="12" rx="4" fill="var(--panel)"/>' + label(36, 52, 'VIDEO', 'violet', 6.5)
    for i in range(31):
        hh = 3 + (i * 7 % 11)
        s += f'<rect class="sys-wave" x="{26+i*4}" y="{186-hh/2}" width="2" height="{hh}" rx="1" fill="var(--violet)" style="animation-delay:-{i*.08:.2f}s"/>'
    s += '<path d="M28 164H232" stroke="var(--line)"/><g class="sys-playhead"><path d="M28 159V168" stroke="var(--lime)" stroke-width="2"/><circle cx="28" cy="159" r="2.4" fill="var(--lime)"/></g><g class="sys-fire"><rect x="170" y="179" width="74" height="19" rx="6" fill="var(--lime)" fill-opacity=".09" stroke="var(--lime)" stroke-opacity=".65"/>' + label(180, 192, 'CITED ↗', 'lime', 8) + '</g>'
    return s + art_footer(['TRACK', 'RETRIEVE', 'CITE']) + '</g>'

def docs_art(x, y, scale=1):
    s = f'<g transform="translate({x} {y}) scale({scale})"><ellipse cx="138" cy="107" rx="142" ry="112" fill="url(#haze)"/>'
    s += '<g class="sys-paper"><rect x="26" y="20" width="65" height="95" rx="8" fill="var(--soft)" stroke="var(--line)"/></g><g class="sys-paper" style="animation-delay:-1.5s"><rect x="16" y="36" width="67" height="96" rx="8" fill="var(--panel)" stroke="var(--violet)" stroke-opacity=".6"/></g><rect x="7" y="53" width="67" height="101" rx="8" fill="var(--bg)" stroke="var(--violet)"/>'
    s += label(18, 75, 'PDF', 'violet', 10)
    for i, yy in enumerate([89, 102, 115, 128]):
        s += f'<rect x="18" y="{yy}" width="{43 if i%2==0 else 32}" height="3" rx="1" fill="var(--muted)" opacity=".4"/><rect class="sys-fire" x="15" y="{yy-4}" width="49" height="11" rx="3" fill="var(--violet)" fill-opacity=".16" style="animation-delay:-{i*.5}s"/>'
    for i in range(5):
        s += f'<g transform="translate(54 {79+i*12})"><rect class="sys-chunk" width="22" height="5" rx="2" fill="var(--violet)" style="animation-delay:-{i*.6}s"/></g>'
    s += signal('M70 105C101 105 98 128 118 128', 'violet', 2.3)
    s += '<g class="sys-chip"><path d="M113 89V147C113 158 162 158 162 147V89" fill="var(--bg)" stroke="var(--violet)"/><ellipse cx="137.5" cy="89" rx="24.5" ry="10" fill="var(--soft)" stroke="var(--violet)"/><path d="M113 112C113 124 162 124 162 112M113 135C113 147 162 147 162 135" fill="none" stroke="var(--violet)" stroke-opacity=".45"/></g>'
    for row in range(3):
        for col in range(5):
            s += f'<rect class="sys-fire" x="{120+col*7}" y="{101+row*22}" width="3" height="5" rx="1" fill="var(--lime)" style="animation-delay:-{(row+col)*.24:.2f}s"/>'
    s += signal('M162 113H185V77H197', 'lime', 2.5, .4)
    s += '<g transform="translate(188 36)"><g class="sys-float"><rect width="81" height="133" rx="10" fill="var(--bg)" stroke="var(--lime)" stroke-opacity=".7"/>' + label(11, 22, 'ANSWER', 'lime', 8)
    for i, width in enumerate([58, 47, 54, 34]):
        s += f'<g transform="translate(11 {38+i*13})"><rect class="sys-answer" width="{width}" height="3" rx="1" fill="var(--ink)" opacity=".75" style="animation-delay:{i*.15}s"/></g>'
    s += '<rect x="10" y="99" width="61" height="23" rx="5" fill="var(--lime)" fill-opacity=".1" stroke="var(--lime)" stroke-opacity=".4"/>' + label(18, 114, 'CITED ↗', 'lime', 8) + '</g></g>'
    s += signal('M40 158V183H229V173', 'violet', 1.8, .7) + label(104, 190, 'VERSIONED', 'muted', 7)
    return s + art_footer(['INGEST', 'RETRIEVE', 'GROUND']) + '</g>'

def latent_art(x, y, scale=1):
    s = f'<g transform="translate({x} {y}) scale({scale})"><ellipse cx="145" cy="110" rx="140" ry="111" fill="url(#haze)"/>'
    s += '<rect x="7" y="28" width="95" height="142" rx="13" fill="var(--bg)" stroke="var(--violet)" stroke-opacity=".65"/><defs><clipPath id="face-window"><rect x="8" y="29" width="93" height="140" rx="12"/></clipPath></defs><g clip-path="url(#face-window)">'
    face = [(54,48),(34,58),(73,58),(27,81),(81,81),(34,108),(74,108),(43,129),(65,129),(54,141),(42,81),(66,81),(54,100),(42,116),(66,116)]
    s += '<path d="M54 47C20 47 23 99 32 115Q54 153 76 115C85 99 88 47 54 47Z" fill="var(--violet)" fill-opacity=".055" stroke="var(--violet)" stroke-opacity=".7"/>'
    for a,b in [(0,1),(0,2),(1,3),(2,4),(3,5),(4,6),(5,7),(6,8),(7,9),(8,9),(1,10),(2,11),(10,11),(10,12),(11,12),(12,13),(12,14),(13,14),(13,7),(14,8),(3,10),(4,11),(5,13),(6,14)]:
        s += f'<path d="M{face[a][0]} {face[a][1]}L{face[b][0]} {face[b][1]}" stroke="var(--violet)" stroke-opacity=".45" stroke-width=".8"/>'
    for i,(cx,cy) in enumerate(face):
        s += f'<circle class="sys-fire" cx="{cx}" cy="{cy}" r="2" fill="var(--lime)" style="animation-delay:-{i*.16:.2f}s"/>'
    s += '<g class="sys-scan-y"><rect x="8" y="24" width="93" height="28" fill="url(#sys-scan-y)"/><path d="M8 52H101" stroke="var(--lime)" stroke-width="2" filter="url(#sys-glow)"/></g></g>'
    for i in range(11):
        yy=46+i*10
        s += f'<path d="M103 {yy}L152 98" stroke="var(--violet)" stroke-opacity=".12"/><g transform="translate(101 {yy})"><rect class="sys-compress" x="-2" y="-2" width="5" height="5" rx="1" fill="var(--violet)" style="--dx:52px;--dy:{98-yy}px;animation-delay:-{i*.136:.3f}s"/></g>'
    s += '<g class="sys-chip"><rect x="144" y="58" width="72" height="80" rx="12" fill="var(--lime)" fill-opacity=".035" stroke="var(--lime)" stroke-opacity=".35"/><rect x="151" y="65" width="58" height="66" rx="9" fill="var(--bg)" stroke="var(--lime)"/></g>'
    for row in range(8):
        for col in range(8):
            s += f'<rect class="sys-fire" x="{159+col*5.5}" y="{76+row*5.5}" width="3" height="3" rx=".7" fill="var(--lime)" style="animation-delay:-{(row*8+col)*.046:.3f}s"/>'
    s += t(180, 153, '64 B', 15, 'lime', 600, 'class="mono" text-anchor="middle"')
    s += signal('M211 98H239', 'lime', 2.7)
    s += '<path d="M253 79L268 85V100Q267 114 253 123Q239 114 238 100V85Z" fill="var(--lime)" fill-opacity=".06" stroke="var(--lime)" stroke-width="1.5"/><path class="sys-check" pathLength="100" d="M245 99L251 105L262 92" fill="none" stroke="var(--lime)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>'
    s += label(34, 188, 'EDGE', 'violet', 8) + label(223, 188, 'SERVER', 'lime', 8)
    return s + art_footer(['ENCODE', 'QUANTIZE', 'VERIFY']) + '</g>'

def trajectory_art(x, y, scale=1):
    s = f'<g transform="translate({x} {y}) scale({scale})"><ellipse cx="140" cy="108" rx="145" ry="115" fill="url(#haze)"/><rect x="9" y="17" width="204" height="173" rx="13" fill="var(--bg)" stroke="var(--violet)" stroke-opacity=".6"/>'
    for xx in range(24,207,14):
        for yy in range(31,184,14):
            s += f'<circle cx="{xx}" cy="{yy}" r=".7" fill="var(--violet)" opacity=".2"/>'
    s += '<path d="M47 17V65H91M9 99H45V140M85 190V147H140V110H190M132 17V50H104V86H80M188 58H213" fill="none" stroke="var(--soft)" stroke-width="9" stroke-linejoin="round"/>'
    routes=['M29 163H64V121H112V76H164V39H192','M29 163V117H65V84H110V61H162V39H192','M29 163H64V178H157V141H174V87H193V39']
    for i,route in enumerate(routes):
        s += signal(route, 'lime' if i==0 else 'violet', 2.5 if i==0 else 1.6, i*.42)
    s += '<circle cx="29" cy="163" r="4" fill="var(--bg)" stroke="var(--violet)"/><circle cx="192" cy="39" r="5" fill="var(--bg)" stroke="var(--lime)"/><g class="sys-runner"><circle class="sys-halo" r="7" fill="var(--lime)"/><circle r="3.7" fill="var(--lime)" filter="url(#sys-glow)"/></g>'
    s += '<circle class="sys-halo" cx="112" cy="121" r="11" fill="var(--violet)"/><circle cx="112" cy="121" r="6" fill="var(--bg)" stroke="var(--violet)"/><path d="M109 121H115M112 118V124" stroke="var(--violet)"/>'
    s += signal('M213 101H228', 'violet', 2.4) + label(225, 37, 'UTILITY', 'violet', 7)
    for i,ww in enumerate([34,25,29,19,13]):
        yy=53+i*23
        s += f'<rect x="228" y="{yy}" width="39" height="14" rx="4" fill="var(--soft)"/><g transform="translate(231 {yy+4})"><rect class="sys-rank" width="{ww}" height="6" rx="2" fill="var(--{"lime" if i==0 else "violet"})" opacity="{1-i*.14}" style="animation-delay:-{i*.35}s"/></g>'
    s += label(229, 182, 'OFFLINE', 'muted', 7)
    return s + art_footer(['SCORE', 'INTERVENE', 'EVALUATE']) + '</g>'

PROJECTS = {
    'tracevision': dict(name='TraceVision', tag='MULTIMODAL / VIDEO SEARCH', metric='52.3×', ml='cache-reuse speedup', mobile_metric=['cache-reuse', 'speedup'], scope=['Recorded local benchmark.', 'Persisted outputs reused.'], desc=['Find the moment. Show the evidence.', 'Bilingual video search with timestamped citations.'], md=['Bilingual video search with', 'timestamped evidence.'], stack='PYTORCH · MULTIMODAL RETRIEVAL · STAGE CACHES', art=video_art),
    'knowledge': dict(name='Subject Knowledge Hub', tag='RAG / RELIABLE INGESTION', metric='3/3', ml='interrupted jobs recovered', mobile_metric=['interrupted jobs', 'recovered'], scope=['Controlled process-kill tests.', 'Fixture embeddings.'], desc=['PDF answers that know their source.', 'Version-aware citations and resumable ingestion.'], md=['Version-aware PDF citations.', 'Ingestion that can resume.'], stack='FASTAPI · PGVECTOR · CELERY · REDIS', art=docs_art),
    'aqb': dict(name='AQB-FAS', tag='COMPUTER VISION / EDGE AI', metric='64 B', ml='serialized latent payload', mobile_metric=['serialized', 'latent payload'], scope=['97.01% CelebA-Spoof test accuracy.', 'Validation-selected operating threshold.'], desc=['A smaller payload. A testable interface.', 'Split-computing face anti-spoofing for edge devices.'], md=['Split-computing face anti-spoofing.', 'A compact edge-to-server interface.'], stack='PYTORCH · QUANTIZATION · HELD-OUT EVALUATION', art=latent_art),
    'datu': dict(name='DATU / Offline RL', tag='REINFORCEMENT LEARNING / INDEPENDENT STUDY', metric='86', ml='completed training jobs', mobile_metric=['completed', 'training jobs'], scope=['Frozen original experiment matrix.', 'Four offline-RL learners; 17.8M updates.'], desc=['Which trajectories change a policy?', 'Offline ranking, frozen interventions and paired evaluation.'], md=['Which trajectories change a policy?', 'Offline ranking. Paired evaluation.'], stack='PYTORCH · IQL / REBRAC / CQL / BC · REPRODUCIBLE EVAL', art=trajectory_art),
}

def project(key, m):
    p = PROJECTS[key]
    w, h = (400, 594) if m else (1000, 338)
    s = project_defs() + panel(w, h, 'panel')
    if m:
        s += label(24, 32, p['tag'], 'violet', 8 if key == 'datu' else 9) + arrow(360, 22)
        s += lines(23, 74, ['Subject', 'Knowledge Hub'], 29, 'ink', 33, 700) if key == 'knowledge' else t(23, 78, p['name'], 32, weight=700, extra='letter-spacing="-1.1"')
        s += p['art'](39, 112, 1.15) + lines(24, 412, p['md'], 15.5, step=23)
        s += t(22, 493, p['metric'], 49, 'lime', 600, extra='letter-spacing="-2"') + lines(179, 472, p['mobile_metric'], 14, 'ink', 21)
        s += rule(24, 513, 376) + lines(24, 535, p['scope'], 12.5, step=19) + label(24, 578, 'VIEW SOURCE ↗', 'violet', 10)
    else:
        s += '<path d="M334 24V314" stroke="var(--line)"/>' + p['art'](23, 45, 1.07) + label(367, 38, p['tag'], 'violet', 10.5) + arrow(953, 25)
        s += t(364, 85, p['name'], 33, weight=700, extra='letter-spacing="-1.1"') + lines(367, 125, p['desc'], 18, step=27) + t(364, 235, p['metric'], 56, 'lime', 600, extra='letter-spacing="-2"')
        mx = 545 if key == 'tracevision' else 514
        s += t(mx, 212, p['ml'], 17, 'ink', 500) + lines(mx, 238, p['scope'], 12.5, step=19) + rule(367, 280, 962) + label(367, 309, p['stack'], size=10)
    return (w, h, s)

def profile_defs():
    """Motion for the experience, research and toolkit sections only."""
    return '''<defs><style>
      .prof-packet{stroke-dasharray:17 83;animation:prof-packet 1.5s linear infinite}
      .prof-pulse{opacity:.7;animation:prof-pulse 3s ease-in-out infinite}
      .prof-cluster{animation:prof-cluster 6s ease-in-out infinite}
      .prof-halo{transform-box:fill-box;transform-origin:center;opacity:.15;animation:prof-halo 3s ease-out infinite}
      .prof-paper{animation:prof-paper 3s ease-in-out infinite alternate}
      .prof-scan{animation:prof-scan 3s ease-in-out infinite alternate}
      .prof-draw{stroke-dasharray:100;stroke-dashoffset:0;animation:prof-draw 6s ease-in-out infinite}
      .prof-bar{transform-box:fill-box;transform-origin:left center;animation:prof-bar 3s ease-in-out infinite alternate}
      .prof-rack{animation:prof-rack 3s ease-in-out infinite alternate}
      .prof-sweep{animation:prof-sweep 6s linear infinite}
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
    <filter id="prof-glow" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="1.15" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <linearGradient id="prof-scan-fill" x1="0" y1="0" x2="0" y2="1"><stop stop-color="var(--lime)" stop-opacity="0"/><stop offset="1" stop-color="var(--lime)" stop-opacity=".22"/></linearGradient>
    <linearGradient id="prof-sweep-fill"><stop stop-color="var(--violet)" stop-opacity="0"/><stop offset="1" stop-color="var(--lime)" stop-opacity=".85"/></linearGradient>
    </defs>'''

def profile_signal(route, c='lime', delay=0, width=2):
    return f'<path d="{route}" fill="none" stroke="var(--{c})" stroke-opacity=".23"/><path class="prof-packet" pathLength="100" d="{route}" fill="none" stroke="var(--{c})" stroke-width="{width}" stroke-linecap="round" filter="url(#prof-glow)" style="animation-delay:-{delay}s"/>'

def delivery_stage(index, x, y, width):
    captions = [('SEGMENT', 'RFM / K-MEANS'), ('RESEARCH', 'GEMINI / SERPAPI'), ('SERVE', 'FASTAPI / POSTGRES'), ('DEPLOY', 'DOCKER / AWS EC2')]
    caption, tools = captions[index]
    scale = (width - 20) / 180
    s = f'<g transform="translate({x} {y})"><rect width="{width}" height="104" rx="12" fill="var(--panel)" stroke="var(--line)"/>'
    s += label(12, 19, f'0{index+1} / {caption}', 'violet', 9) + label(12, 94, tools, 'muted', 7.5)
    s += f'<g transform="translate(10 25) scale({scale} .85)">'
    if index == 0:
        centers = [(37, 26), (93, 38), (145, 24)]
        colors = ['violet', 'lime', 'ink']
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
            s += f'<rect x="6" y="{yy}" width="31" height="12" rx="4" fill="var(--soft)" stroke="var(--violet)" stroke-opacity=".4"/>'
            s += profile_signal(f'M37 {yy+6}Q62 {yy+6} 83 29', 'violet', i*.4)
        s += '<circle class="prof-halo" cx="90" cy="29" r="17" fill="var(--lime)"/>' + star(90, 29, 11, 'lime')
        s += profile_signal('M102 29H132', 'lime', .6)
        for i in range(3):
            s += f'<rect class="prof-bar" x="137" y="{12+i*15}" width="{36-i*7}" height="5" rx="2" fill="var(--lime)" style="animation-delay:-{i*.5}s"/>'
    elif index == 2:
        s += '<rect x="67" y="3" width="49" height="52" rx="9" fill="var(--bg)" stroke="var(--violet)"/>'
        s += t(91, 37, '{ }', 24, 'lime', 500, 'text-anchor="middle" class="mono"')
        for i in range(3):
            yy=11+i*18
            s += profile_signal(f'M5 {yy}H65', 'violet', i*.35, 2.5)
            s += profile_signal(f'M118 {yy}H176', 'lime', i*.35+.6, 2.5)
    else:
        s += '<path d="M37 43C11 43 16 19 37 20C41 -1 70 -3 78 15C97 7 113 17 112 30H149" fill="none" stroke="var(--violet)" stroke-opacity=".6"/>'
        s += profile_signal('M17 52H66V29H103', 'violet', .5)
        for row in range(2):
            for col in range(3):
                xx=103+col*21;yy=14+row*22
                s += f'<g transform="translate({xx} {yy})"><g class="prof-rack" style="animation-delay:-{(row+col)*.45}s"><rect width="17" height="18" rx="3" fill="var(--bg)" stroke="var(--lime)" stroke-opacity=".65"/><circle class="prof-pulse" cx="5" cy="5" r="1.5" fill="var(--lime)"/><path d="M4 11H13M4 14H10" stroke="var(--violet)" stroke-opacity=".55"/></g></g>'
    return s + '</g></g>'

def experience(m):
    w, h = (400, 610) if m else (1000, 398)
    p = 24 if m else 36
    s = profile_defs() + panel(w, h) + label(p, 34, '02 / IN THE FIELD', 'lime', 10 if m else 12)
    s += t(p-1, 79, 'Built beyond the notebook.', 24 if m else 36, weight=700, extra='letter-spacing="-1"')
    if m:
        s += t(p, 123, 'ECE Technology', 23, weight=600) + t(p, 151, 'AI Engineer Intern', 16, 'violet') + label(p, 176, 'JAN–APR 2026 · E-COMMERCE MVP', size=9)
        s += lines(p, 213, ['RFM segmentation · Mini-Batch K-Means.', 'Market research · Gemini + SerpAPI.', 'FastAPI / PostgreSQL microservice.', 'Docker deployment on AWS EC2.'], 14.5, step=23)
        s += '<g transform="translate(24 321)">' + profile_signal('M164 52H188', 'lime') + profile_signal('M270 104V123H82V142', 'violet', .6) + profile_signal('M164 194H188', 'lime', 1)
        for i, (xx, yy) in enumerate([(0,0),(188,0),(0,142),(188,142)]):
            s += delivery_stage(i, xx, yy, 164)
        s += '</g>' + label(p, 589, 'PROBLEM → MODEL → SERVICE → DEPLOYMENT', 'violet', 8.5)
    else:
        s += t(p, 130, 'ECE Technology', 23, weight=600) + t(p, 160, 'AI Engineer Intern', 17, 'violet') + label(p, 190, 'JAN–APR 2026 · E-COMMERCE MVP', size=10)
        s += '<path d="M329 107V201" stroke="var(--line)"/>' + lines(361, 130, ['RFM segmentation with Mini-Batch K-Means.', 'Market intelligence with Gemini and SerpAPI.', 'FastAPI / PostgreSQL microservice, deployed on AWS EC2.'], 18, step=29)
        s += '<g transform="translate(36 237)">'
        for i in range(3):
            s += profile_signal(f'M{204+i*242} 52H{242+i*242}', 'lime' if i%2==0 else 'violet', i*.4)
        for i in range(4):
            s += delivery_stage(i, i*242, 0, 204)
        s += '</g>' + label(p, 375, 'PROBLEM → MODEL → SERVICE → DEPLOYMENT', 'violet', 10)
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

def research_art(x, y, scale=1):
    s = f'<g transform="translate({x} {y}) scale({scale})"><ellipse cx="122" cy="100" rx="130" ry="111" fill="url(#haze)"/>'
    for i, (xx, yy) in enumerate([(12,42),(224,24),(231,160),(21,169)]):
        s += profile_signal(f'M{xx} {yy}Q125 {yy} 124 106', 'violet' if i%2==0 else 'lime', i*.4, 1.9)
        s += f'<circle class="prof-halo" cx="{xx}" cy="{yy}" r="7" fill="var(--violet)" style="animation-delay:-{i*.6}s"/><rect x="{xx-6}" y="{yy-8}" width="12" height="16" rx="3" fill="var(--bg)" stroke="var(--violet)"/><path d="M{xx-3} {yy-2}H{xx+3}M{xx-3} {yy+2}H{xx+1}" stroke="var(--lime)" stroke-width=".8"/>'
    s += '<g class="prof-paper" style="animation-delay:-1.5s"><rect x="75" y="15" width="113" height="144" rx="10" fill="var(--soft)" stroke="var(--line)"/></g><g class="prof-paper"><rect x="64" y="25" width="113" height="144" rx="10" fill="var(--panel)" stroke="var(--violet)" stroke-opacity=".45"/></g><rect x="51" y="37" width="113" height="146" rx="10" fill="var(--bg)" stroke="var(--violet)"/>'
    s += label(65, 57, 'EXPERIMENT', 'violet', 8)
    s += '<path d="M66 69H143M66 77H119" stroke="var(--muted)" stroke-width="2" opacity=".4"/>'
    for row in range(4):
        for col in range(7):
            s += f'<rect class="prof-pulse" x="{67+col*11}" y="{89+row*10}" width="6" height="5" rx="1.5" fill="var(--{"lime" if (row+col)%3==0 else "violet"})" style="animation-delay:-{(row*7+col)*.11:.2f}s"/>'
    route='M66 159L82 152L98 156L112 143L126 147L146 131'
    s += f'<path d="{route}" fill="none" stroke="var(--violet)" stroke-opacity=".25"/><path class="prof-draw" pathLength="100" d="{route}" fill="none" stroke="var(--lime)" stroke-width="2" filter="url(#prof-glow)"/>'
    s += '<defs><clipPath id="research-page"><rect x="52" y="38" width="111" height="144" rx="9"/></clipPath></defs><g clip-path="url(#research-page)"><g class="prof-scan"><rect x="53" y="57" width="109" height="25" fill="url(#prof-scan-fill)"/><path d="M53 82H162" stroke="var(--lime)" stroke-width="1.4"/></g></g>'
    s += '<g transform="translate(166 135)"><circle r="22" fill="var(--bg)" stroke="var(--lime)" stroke-opacity=".75"/><circle class="prof-halo" r="20" fill="var(--lime)"/><path class="prof-draw" pathLength="100" d="M-11 0L-3 8L12 -9" fill="none" stroke="var(--lime)" stroke-width="2.5" stroke-linecap="round"/><path d="M17 17L33 33" stroke="var(--violet)" stroke-width="5" stroke-linecap="round"/></g>'
    return s + label(38, 209, 'QUESTION / TEST / REPRODUCE', 'muted', 8) + '</g>'

def research(m):
    w, h = (400, 916) if m else (1000, 680)
    p = 24 if m else 36
    s = profile_defs() + panel(w, h) + label(p, 34, '03 / RESEARCH NOTES', 'lime', 10 if m else 12)
    s += t(p-1, 79, 'Ask better questions.', 28 if m else 36, weight=700, extra='letter-spacing="-1.2"') + arrow(w-53, 29, 'violet')
    s += research_art(62 if m else 44, 112 if m else 239, 1.1)
    if not m:
        s += label(36, 112, '07 PAPERS & MANUSCRIPTS', 'muted', 10) + '<path d="M330 132V590" stroke="var(--line)"/>'
    mobile_y = 455
    for i, paper in enumerate(PAPERS):
        xx=24 if m else 366; yy=mobile_y if m else (153+i*65)
        color = {'published':'lime', 'accepted':'violet', 'submitted':'muted'}[paper['status']]
        titles = paper.get('mobile', [paper['short']]) if m else [paper['short']]
        for j, title in enumerate(titles):
            s += t(xx, yy+j*24, title, 19 if m else 21, weight=600, extra='letter-spacing="-.35"')
        status_y = yy+(len(titles)-1)*24+23
        s += t(xx, status_y, f"{paper['status'].upper()} · {paper['venue']}", 10.5 if m else 12, color, 500, 'class="mono"')
        if i < len(PAPERS)-1:
            s += rule(xx, status_y+14, 376 if m else 963)
        mobile_y = status_y+36
    for i, (status, color) in enumerate([('published','lime'),('accepted','violet'),('submitted','muted')]):
        count=sum(paper['status']==status for paper in PAPERS)
        xx=(24+i*121) if m else (36+i*314); yy=360 if m else 619; ww=110 if m else 300
        s += f'<rect x="{xx}" y="{yy}" width="{ww}" height="{54 if m else 40}" rx="9" fill="var(--panel)" stroke="var(--line)"/>'
        s += t(xx+12, yy+(26 if m else 27), f'{count:02}', 24 if m else 25, color, 600)
        s += label(xx+12 if m else xx+53, yy+43 if m else yy+25, status.upper(), color, 8 if m else 9)
    return (w, h, s)

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
            s += profile_signal(f'M3 {yy}L22 18L39 {36-yy}', 'violet', yy/20, 1.4)
        for xx,yy in [(3,5),(3,18),(3,31),(22,18),(39,5),(39,18),(39,31)]:
            s += f'<circle class="prof-pulse" cx="{xx}" cy="{yy}" r="2.5" fill="var(--lime)" style="animation-delay:-{xx*.05}s"/>'
    elif index==1:
        for row in range(4):
            for col in range(5):
                s += f'<rect class="prof-pulse" x="{col*8}" y="{row*9}" width="4" height="5" rx="1" fill="var(--{"lime" if col==2 else "violet"})" style="animation-delay:-{(row+col)*.35}s"/>'
    elif index==2:
        s += '<path d="M12 2H6V13L2 18L6 23V34H12M29 2H35V13L39 18L35 23V34H29" fill="none" stroke="var(--violet)" stroke-width="1.4"/>'
        s += profile_signal('M11 18H30', 'lime', 0, 2.3)
    elif index==3:
        for i in range(3):
            s += f'<g class="prof-rack" style="animation-delay:-{i*.5}s"><rect x="2" y="{i*12}" width="36" height="9" rx="2" fill="none" stroke="var(--violet)"/><circle class="prof-pulse" cx="8" cy="{4.5+i*12}" r="1.5" fill="var(--lime)"/><path d="M15 {4.5+i*12}H31" stroke="var(--lime)" stroke-opacity=".4"/></g>'
    else:
        s += '<path d="M7 2H34Q40 2 40 8V23Q40 29 34 29H17L8 36V29H7Q1 29 1 23V8Q1 2 7 2Z" fill="none" stroke="var(--violet)" stroke-width="1.3"/>'
        s += t(21, 19, 'B2', 12, 'lime', 600, 'class="mono" text-anchor="middle"')
        for i in range(3):
            s += f'<circle class="prof-pulse" cx="{15+i*6}" cy="24" r="1" fill="var(--lime)" style="animation-delay:-{i*.4}s"/>'
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
    s = profile_defs() + panel(w, h, 'panel') + label(p, 32, 'THE TOOLKIT', 'lime', 10 if m else 12)
    if m:
        s += lines(p-1, 77, ['A practical stack,', 'tied to real work.'], 28, 'ink', 32, 700)
    else:
        s += t(p-1, 77, 'A practical stack, tied to real work.', 34, weight=700, extra='letter-spacing="-1.2"')
    for i,(group,text_lines,yy,hh) in enumerate(rows):
        ww=352 if m else 928
        s += f'<rect x="{p}" y="{yy}" width="{ww}" height="{hh}" rx="10" fill="var(--bg)" stroke="var(--line)"/>'
        s += stack_glyph(i, p+14, yy+(hh-36)/2)
        s += t(p+71, yy+25, group['name'], 14 if m else 16, 'violet', 600)
        s += lines(p+71, yy+50 if m else yy+55, text_lines, 14 if m else 16.5, 'ink', 21 if m else 25)
        if not m:
            for j in range(7):
                s += f'<rect class="prof-pulse" x="{873+j*9}" y="{yy+16}" width="4" height="12" rx="2" fill="var(--lime)" style="animation-delay:-{i*.5+j*.2}s"/>'
        s += f'<defs><clipPath id="stack-lane-{i}"><rect x="{p+8}" y="{yy+hh-4}" width="{ww-16}" height="2"/></clipPath></defs><g clip-path="url(#stack-lane-{i})"><g transform="translate({p-92} {yy+hh-4})"><rect class="prof-sweep" width="100" height="2" fill="url(#prof-sweep-fill)" style="--travel:{ww+100}px;animation-delay:-{i*1.5}s"/></g></g>'
    return (w, h, s)

def footer(m):
    w, h = (400, 368) if m else (1000, 270)
    p = 24 if m else 36
    s = panel(w, h) + label(p, 34, 'OPEN TO AI ENGINEERING OPPORTUNITIES', 'lime', 9 if m else 12)
    if m:
        s += t(21, 106, 'let’s build', 48, weight=700, extra='letter-spacing="-2"') + t(21, 158, 'what’s next.', 48, weight=700, extra='letter-spacing="-2"') + star(349, 193, 17, 'violet', True) + t(p, 207, 'nxt276651@gmail.com ↗', 18, 'violet', 500) + lines(p, 252, ['Part-time through Jun 2027.', 'Full-time from Jul 2027.'], 15, step=23) + rule(24, 296, 376) + lines(p, 324, ['B.Sc. AI · FPT University · GPA 3.75/4.0', 'Expected graduation: Jun 2027'], 13, step=21)
    else:
        s += t(31, 112, 'let’s build what’s next.', 58, weight=700, extra='letter-spacing="-3"') + star(926, 97, 28, 'violet', True) + t(p, 157, 'nxt276651@gmail.com ↗', 22, 'violet', 500) + t(p, 196, 'Part-time through Jun 2027 · Full-time from Jul 2027', 17, 'muted') + rule(36, 217, 962) + t(p, 248, 'B.Sc. AI · FPT University · GPA 3.75/4.0 · Expected graduation: Jun 2027', 14, 'muted')
    return (w, h, s)
BUILDERS = {'hero': hero, 'work': work, 'tracevision': lambda m: project('tracevision', m), 'knowledge': lambda m: project('knowledge', m), 'aqb': lambda m: project('aqb', m), 'datu': lambda m: project('datu', m), 'experience': experience, 'research': research, 'toolkit': toolkit, 'footer': footer}
MOVING = {'hero', 'tracevision', 'knowledge', 'aqb', 'datu', 'experience', 'research', 'toolkit', 'footer'}

def generate_outputs():
    outputs = {}
    for theme in THEMES:
        for name, builder in BUILDERS.items():
            for mobile in (False, True):
                width, height, body = builder(mobile)
                size = 'mobile' if mobile else 'desktop'
                for static in (False, True) if name in MOVING else (False,):
                    suffix = '-still' if static else ''
                    outputs[f'{name}-{theme}-{size}{suffix}.svg'] = svg(name, width, height, body, theme, static)
        for name, caption in (('portfolio', 'Portfolio'), ('resume', 'Résumé'), ('linkedin', 'LinkedIn'), ('email', 'Email')):
            primary = name == 'portfolio'
            background = 'lime' if primary else 'panel'
            ink = 'bg' if primary else 'ink'
            body = f'<rect x=".75" y=".75" width="158.5" height="44.5" rx="10" fill="var(--{background})" stroke="var(--line)" stroke-width="1.5"/>'
            body += t(14, 29, caption, 16, ink, 600) + arrow(131, 16, ink)
            outputs[f'nav-{name}-{theme}.svg'] = svg(caption, 160, 46, body, theme, True)
    return outputs

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
        print('Out-of-date Neon Lab assets:', file=sys.stderr)
        print('\n'.join(stale), file=sys.stderr)
        return 1
    print(f'Neon Lab: {len(outputs)} assets ' + ('are up to date.' if args.check else 'generated.'))
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
