#!/usr/bin/env python3
"""
Gera o banner "terminal Kali" do perfil: banner-dark.svg e banner-light.svg.

Tudo que você quer mudar (nome, cargo, stack, contatos, comandos do terminal)
está em CONFIG lá embaixo. Rode:  python3 generate_banner.py .
e ele escreve os dois SVGs no diretório passado (padrão: diretório atual).

Estética: janela de terminal com prompt root@kali, verde-neon sobre preto,
cursor piscando, "digitação" animada, linhas com dotted-leaders e barra de scan.
"""
import html, os, sys

# ----------------------------- temas -----------------------------
THEMES = {
    "dark": {
        "BG": "#0B0614", "PANEL": "#140A20", "BAR": "#0E0718",
        "GREEN": "#A855F7", "GREEN_DIM": "#5B21B6", "CYAN": "#C084FC",
        "RED": "#F43F5E", "AMBER": "#FBBF24", "TEXT": "#EDE4FB",
        "MUTED": "#A78BFA", "DIM": "#3B2A5F", "WHITE": "#F5EFFF",
        "LEADER": "rgba(168,85,247,0.20)", "GRIDLINE": "rgba(168,85,247,0.05)",
        "BORDER": "rgba(168,85,247,0.35)", "PANEL_STROKE": "rgba(168,85,247,0.22)",
        "SCAN": "rgba(168,85,247,0.05)",
    },
    "light": {
        "BG": "#F7F3FC", "PANEL": "#FFFFFF", "BAR": "#EDE4F7",
        "GREEN": "#7C3AED", "GREEN_DIM": "#5B21B6", "CYAN": "#9333EA",
        "RED": "#E11D48", "AMBER": "#B45309", "TEXT": "#2E1065",
        "MUTED": "#7C3AED", "DIM": "#B69DD8", "WHITE": "#2E1065",
        "LEADER": "rgba(124,58,237,0.22)", "GRIDLINE": "rgba(124,58,237,0.05)",
        "BORDER": "rgba(124,58,237,0.35)", "PANEL_STROKE": "rgba(124,58,237,0.20)",
        "SCAN": "rgba(124,58,237,0.04)",
    },
}

# ----------------------------- CONFIG ----------------------------
# >>> edite aqui <<<
CONFIG = {
    "user": "daniel",
    "host": "kali",
    "prompt_cmd": "./whoami.sh --live",
    "title_bar": "daniel@kali: ~/profile",
    # comandos que aparecem "digitados" no bloco esquerdo, em sequência
    "boot_lines": [
        ("$ ", "whoami", None),
        ("", "marcos daniel figueredo ferrari", "out"),
        ("$ ", "cat role.txt", None),
        ("", "Red Teamer / Pentester", "out"),
        ("$ ", "id --focus", None),
        ("", "eJPT  ·  PNPT  ·  OSCP", "out"),
        ("$ ", "uname -a", None),
        ("", "Kali GNU/Linux  ·  homelab red-team", "out"),
        ("$ ", "./engage.sh --scope", None),
    ],
    # painel direito: rótulo ........... valor
    "info": [
        ("Subject", "Marcos Daniel F. Ferrari"),
        ("Role", "Red Teamer / Pentester"),
        ("Origin", "Tres Rios, RJ - Brazil"),
        ("Focus", "Offensive Security / AdvSim"),
        ("Status", "Learning + Building + Breaking"),
        ("Toolchain", "Burp, PortSwigger, Metasploit, Wireshark"),
        ("Core.Lang", "C, Python, Bash"),
        ("Core.Sec", "Pentest, IDOR/BAC, AD, PrivEsc"),
        ("Core.Infra", "pfSense, Wazuh, Suricata, Docker"),
    ],
    "contact": [
        ("Grid.Mail", "mdaniel.main@gmail.com"),
        ("Grid.GitHub", "@Daniel16Bit"),
        ("Grid.LinkedIn", "mdaniel-main"),
        ("Grid.Brand", "@daniel8bit"),
    ],
    "footer": "More about me & projects below in README",
}
# -----------------------------------------------------------------

W, H = 1180, 500
FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"


def esc(s):
    return html.escape(str(s), quote=True)


def build(theme):
    t = THEMES[theme]
    g = lambda k: t[k]
    s = []
    a = s.append
    gid = f"scan_{theme}"
    aid = f"accent_{theme}"

    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
      f'viewBox="0 0 {W} {H}" font-family="{FONT}" role="img" '
      f'aria-label="{esc(CONFIG["title_bar"])}">')

    # defs: gradiente animado da borda + barra de varredura
    a('<defs>')
    a(f'<linearGradient id="{aid}" x1="0" y1="0" x2="1" y2="0">'
      f'<stop offset="0" stop-color="{g("GREEN")}"><animate attributeName="stop-color" '
      f'values="{g("GREEN")};{g("CYAN")};{g("GREEN")}" dur="8s" repeatCount="indefinite"/></stop>'
      f'<stop offset="1" stop-color="{g("CYAN")}"><animate attributeName="stop-color" '
      f'values="{g("CYAN")};{g("GREEN")};{g("CYAN")}" dur="8s" repeatCount="indefinite"/></stop>'
      f'</linearGradient>')
    a(f'<clipPath id="clip_{theme}"><rect x="2" y="2" width="{W-4}" height="{H-4}" rx="16"/></clipPath>')
    a(f'<filter id="glow_{theme}" x="-40%" y="-40%" width="180%" height="180%">'
      f'<feGaussianBlur stdDeviation="1.4" result="b"/><feMerge>'
      f'<feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
    a('</defs>')

    # fundo + janela
    a(f'<rect x="2" y="2" width="{W-4}" height="{H-4}" rx="16" fill="{g("BG")}"/>')
    a(f'<g clip-path="url(#clip_{theme})">')
    a(f'<rect x="2" y="2" width="{W-4}" height="{H-4}" fill="{g("PANEL")}"/>')

    # grade sutil de fundo
    for gx in range(0, W, 26):
        a(f'<line x1="{gx}" y1="46" x2="{gx}" y2="{H}" stroke="{g("GRIDLINE")}" stroke-width="1"/>')
    for gy in range(46, H, 26):
        a(f'<line x1="0" y1="{gy}" x2="{W}" y2="{gy}" stroke="{g("GRIDLINE")}" stroke-width="1"/>')

    # barra de título
    a(f'<rect x="2" y="2" width="{W-4}" height="44" fill="{g("BAR")}"/>')
    a(f'<line x1="2" y1="46" x2="{W-2}" y2="46" stroke="{g("BORDER")}" stroke-width="1"/>')
    a(f'<circle cx="30" cy="24" r="5.5" fill="#ff5f56"/>')
    a(f'<circle cx="50" cy="24" r="5.5" fill="#ffbd2e"/>')
    a(f'<circle cx="70" cy="24" r="5.5" fill="#27c93f"/>')
    a(f'<text x="{W//2}" y="28" text-anchor="middle" font-size="12" fill="{g("MUTED")}">'
      f'{esc(CONFIG["title_bar"])} — % {esc(CONFIG["prompt_cmd"])}</text>')

    # ---------- painel esquerdo: terminal "boot" ----------
    LX, LY, LW, LH = 30, 66, 520, 410
    a(f'<text x="{LX+6}" y="{LY-4}" font-size="10" letter-spacing="3" fill="{g("DIM")}">TTY0.LOG</text>')
    a(f'<rect x="{LX}" y="{LY}" width="{LW}" height="{LH}" rx="10" fill="{g("BG")}" '
      f'stroke="{g("PANEL_STROKE")}"/>')

    y = LY + 30
    delay = 0.3
    for prompt, text, kind in CONFIG["boot_lines"]:
        if kind == "out":
            a(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" '
              f'dur="0.3s" begin="{delay:.2f}s" fill="freeze"/>'
              f'<text x="{LX+18}" y="{y}" font-size="14" fill="{g("MUTED")}">'
              f'{esc(text)}</text></g>')
            delay += 0.5
        else:
            full = prompt + text
            a(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" '
              f'dur="0.2s" begin="{delay:.2f}s" fill="freeze"/>'
              f'<text x="{LX+18}" y="{y}" font-size="14" font-weight="600">'
              f'<tspan fill="{g("GREEN")}">{esc(CONFIG["user"])}@{esc(CONFIG["host"])}</tspan>'
              f'<tspan fill="{g("MUTED")}">:~$ </tspan>'
              f'<tspan fill="{g("TEXT")}">{esc(text)}</tspan></text></g>')
            delay += 0.7
        y += 40

    # cursor piscando na última linha
    a(f'<rect x="{LX+18}" y="{y-13}" width="9" height="16" fill="{g("GREEN")}" opacity="0">'
      f'<animate attributeName="opacity" values="0;0;1" keyTimes="0;{max(0.01,(delay-0.3)/(delay+2)):.3f};{min(0.999,(delay-0.29)/(delay+2)):.3f}" '
      f'dur="{delay+2:.1f}s" fill="freeze"/>'
      f'<animate attributeName="opacity" values="1;0;1" dur="1.1s" begin="{delay:.2f}s" '
      f'repeatCount="indefinite"/></rect>')

    # ---------- painel direito: SYSTEM.INFO ----------
    RX = 588
    a(f'<text x="{RX}" y="{LY-4}" font-size="13" letter-spacing="2" fill="{g("GREEN")}" '
      f'filter="url(#glow_{theme})">SYSTEM.INFO</text>')
    a(f'<line x1="{RX+120}" y1="{LY-8}" x2="{W-118}" y2="{LY-8}" stroke="{g("BORDER")}"/>')
    a(f'<text x="{W-30}" y="{LY-4}" text-anchor="end" font-size="12" fill="{g("RED")}" '
      f'font-weight="700"><tspan>&#9679;</tspan> LIVE'
      f'<animate attributeName="opacity" values="1;0.25;1" dur="1.6s" repeatCount="indefinite"/></text>')

    ry = LY + 30
    d = 0.6
    dots = "." * 60
    for label, value in CONFIG["info"]:
        pad = max(2, 46 - len(label) - len(value))
        a(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" '
          f'begin="{d:.2f}s" fill="freeze"/>'
          f'<animateTransform attributeName="transform" type="translate" '
          f'values="-8 0;0 0" dur="0.4s" begin="{d:.2f}s" fill="freeze"/>'
          f'<text x="{RX}" y="{ry}" font-size="14">'
          f'<tspan fill="{g("CYAN")}">{esc(label)} </tspan>'
          f'<tspan fill="{g("LEADER")}">{dots[:pad]}</tspan>'
          f'<tspan fill="{g("WHITE")}" font-weight="600"> {esc(value)}</tspan></text></g>')
        ry += 27
        d += 0.12

    # separador Contact
    ry += 4
    a(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" '
      f'begin="{d:.2f}s" fill="freeze"/>'
      f'<text x="{RX}" y="{ry}" font-size="14"><tspan fill="{g("MUTED")}">- Contact </tspan>'
      f'<tspan fill="{g("LEADER")}">{"-"*58}</tspan></text></g>')
    ry += 27
    d += 0.15

    for label, value in CONFIG["contact"]:
        pad = max(2, 46 - len(label) - len(value))
        a(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" '
          f'begin="{d:.2f}s" fill="freeze"/>'
          f'<animateTransform attributeName="transform" type="translate" '
          f'values="-8 0;0 0" dur="0.4s" begin="{d:.2f}s" fill="freeze"/>'
          f'<text x="{RX}" y="{ry}" font-size="14">'
          f'<tspan fill="{g("CYAN")}">{esc(label)} </tspan>'
          f'<tspan fill="{g("LEADER")}">{dots[:pad]}</tspan>'
          f'<tspan fill="{g("WHITE")}" font-weight="600"> {esc(value)}</tspan></text></g>')
        ry += 27
        d += 0.12

    # footer
    ry += 8
    a(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.5s" '
      f'begin="{d+0.2:.2f}s" fill="freeze"/>'
      f'<text x="{RX}" y="{ry}" font-size="13" fill="{g("MUTED")}">'
      f'&#9656; {esc(CONFIG["footer"])} &#8595; '
      f'<tspan fill="{g("GREEN")}">&#9608;<animate attributeName="fill-opacity" '
      f'values="1;0;1" dur="1s" repeatCount="indefinite"/></tspan></text></g>')

    # barra de varredura (scanline) descendo
    a(f'<rect x="2" y="46" width="{W-4}" height="80" fill="{g("SCAN")}" opacity="0.8">'
      f'<animate attributeName="y" values="46;{H-40};46" dur="6s" repeatCount="indefinite"/></rect>')

    a('</g>')  # fim clip

    # borda animada
    a(f'<rect x="3" y="3" width="{W-6}" height="{H-6}" rx="15" fill="none" '
      f'stroke="url(#{aid})" stroke-width="1.6"/>')

    a('</svg>')
    return "".join(s)


if __name__ == "__main__":
    outdir = sys.argv[1] if len(sys.argv) > 1 else "."
    for theme, fname in (("dark", "banner-dark.svg"), ("light", "banner-light.svg")):
        svg = build(theme)
        path = os.path.join(outdir, fname)
        with open(path, "w") as f:
            f.write(svg)
        print(f"escrito {path}: {theme}, {len(svg)//1024}KB")
