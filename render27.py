#!/usr/bin/env python3
"""Render news-image-20261127 entry.png (1024x1024, <1 MiB).

Entry for the 27 November 2026 world-news image (make.fun
news-image-20261127). TARGET: top 1. Benchmark is the news-23
winner regian (35 dated stories, 9 regions, verification labels,
UTC timeline, world map with numbered pins, DATE CHECK footer).

Lineup (35 stories): 3 heroes (Nor'easter 900,000 without power +
Macy's 100th parade postponed / Gulf: 2 Italians killed in Kuwait
+ 1 Nepali dead at Jazan refinery + Brent $96.57 / Ukraine: record
55,629 Russian losses in 25 days) + 10 medium cards + 22 dated
briefs + timeline strip + map.

Accuracy rules baked in (from research-2026-11-27.md):
- 27 Nov 2026 is a FRIDAY (verified with `date -d`); masthead
  says FRIDAY, not Thursday.
- Hong Kong fire was 26 Nov 2025, NOT 2026; 26 Nov 2026 is the
  1-YEAR ANNIVERSARY (168 dead). Never write "fire kills 168 on
  26 Nov 2026".
- Nvidia: last verified close is 25 Nov ($149.30, -3.91%);
  27 Nov close NOT available at build time (market opens 14:30
  UTC, early close 18:00 UTC). Write the 25 Nov close + a note
  that markets reopen 27 Nov. Never invent a 27 Nov close.
  $142.90 was the 25 Nov INTRADAY low, not the close.
- 55,629 is Russian personnel KILLED OR WOUNDED (Ukraine claim,
  REPORTED), NOT deaths. Never write "55,629 killed". Never mix
  with 490,334 (leaked Rosstat DEATHS, Feb 2022-Sep 2026).
- Gulf = 4 SEPARATE incidents: Hormuz 25 Nov (2 tankers, 0 dead),
  Jazan 26 Nov (1 Nepali dead), Kuwait 26 Nov (2 Italians dead,
  Iran DENIES, attribution CLAIM), Ras Tanura 24 Nov. Never one
  combined casualty figure, never "Iran attacked Kuwait" as fact.
- Macy's 100th parade was POSTPONED 26 Nov -> Sat 28 Nov 08:30
  ET (first postponement in 100 years). It did NOT take place
  on 26 Nov. What happened 26 Nov was the storm.
- ICJ Myanmar ruling was 19 Nov; Myanmar's REJECTION was 25 Nov.
- Ebola uses the NEW numbers: 12,021 cases / 5,904 dead (data
  26 Nov), NOT the old 11,042 / 5,387.
- NZ election was 7 Nov; the FINAL COUNT was announced 27 Nov.
- Items 17-30 + 32 are single-aggregator REPORTED (not confirmed);
  they sit in the briefs only, labelled REPORTED.

Adapted from render27.py (news-26, same layout family).
Flat colours, simple pictograms, DejaVu type. Fully deterministic:
fixed palette, fixed fonts, no randomness, no clock -- repeated
runs produce byte-identical output.

Usage: python3 render27.py   # writes entry.png next to this script
"""
import hashlib
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

W, H = 1024, 1024

# ---- palette ------------------------------------------------------------
NAVY = (13, 30, 52)        # masthead / footer / map
NAVY2 = (22, 42, 68)       # hero 2 background
HERO1 = (16, 62, 84)       # hero 1 background (storm teal)
HERO2 = (96, 24, 24)       # hero 2 background (deep red)
HERO3 = (22, 42, 68)       # hero 3 background (navy)
GREEN = (16, 120, 70)
GREEN2 = (34, 160, 100)
PAPER = (247, 243, 234)    # page background
CARD = (255, 255, 255)
INK = (18, 24, 33)
MUTED = (84, 92, 104)
GOLD = (212, 165, 65)
FIRE = (232, 96, 34)
TEAL = (15, 118, 110)
STEEL = (46, 92, 138)
RED = (178, 34, 34)
RED2 = (214, 48, 49)
AMBER = (176, 118, 8)
STAT_BG = (240, 236, 226)
RULE = (214, 206, 190)
MAP_LAND = (58, 104, 148)
MAP_SEA = (13, 30, 52)

LABEL_COL = {"OFFICIAL": (16, 120, 70), "CONFIRMED": (46, 92, 138),
             "REPORTED": (84, 92, 104), "CLAIM": (176, 118, 8)}


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_TITLE = font("DejaVuSans-Bold.ttf", 46)
F_DATE = font("DejaVuSans-Bold.ttf", 24)
F_SUB = font("DejaVuSans-Bold.ttf", 15)
F_TAB = font("DejaVuSans-Bold.ttf", 11)
F_KICK = font("DejaVuSans-Bold.ttf", 12)
F_HERO_NUM = font("DejaVuSans-Bold.ttf", 44)
F_HERO_H = font("DejaVuSans-Bold.ttf", 20)
F_HERO_SUB = font("DejaVuSans-Bold.ttf", 14)
F_HERO_ATT = font("DejaVuSans.ttf", 12)
F_CHIP = font("DejaVuSans-Bold.ttf", 12)
F_MED_K = font("DejaVuSans-Bold.ttf", 10)
F_MED_H = font("DejaVuSans-Bold.ttf", 14)
F_MED_B = font("DejaVuSans.ttf", 11)
F_MED_S = font("DejaVuSans-Bold.ttf", 10)
F_TL_H = font("DejaVuSans-Bold.ttf", 12)
F_TL = font("DejaVuSans.ttf", 11)
F_TL_B = font("DejaVuSans-Bold.ttf", 11)
F_MAP_T = font("DejaVuSans-Bold.ttf", 14)
F_MAP_L = font("DejaVuSans.ttf", 11)
F_PIN = font("DejaVuSans-Bold.ttf", 11)
F_BR_H = font("DejaVuSans-Bold.ttf", 13)
F_BR = font("DejaVuSans.ttf", 11)
F_BR_B = font("DejaVuSans-Bold.ttf", 11)
F_FOOT = font("DejaVuSans.ttf", 11)
F_FOOT_B = font("DejaVuSans-Bold.ttf", 11)
F_SRC = font("DejaVuSans.ttf", 11)


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning a list of lines fitting `width` px."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading=None):
    if leading is None:
        leading = fnt.size + 5
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ================= MASTHEAD =================
    d.rectangle([0, 0, W, 76], fill=NAVY)
    d.rectangle([0, 76, W, 79], fill=GOLD)
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=F_TITLE)
    d.text(((W - tw) / 2, 4), title, font=F_TITLE, fill=(255, 255, 255))
    sub = "FRIDAY 27 NOVEMBER 2026  \u2022  35 DATED STORIES \u2022 9 REGIONS \u2022 14 FIELDS"
    sw = d.textlength(sub, font=F_SUB)
    d.text(((W - sw) / 2, 54), sub, font=F_SUB, fill=GOLD)

    # ================= REGION TABS =================
    tabs = [("NORTH AMERICA", 5), ("SOUTH AMERICA", 2), ("EUROPE", 5),
            ("MIDDLE EAST", 6), ("AFRICA", 3), ("SOUTH ASIA", 2),
            ("EAST ASIA", 5), ("OCEANIA", 3), ("WORLD", 4)]
    tx = 24
    ty = 84
    for name, n in tabs:
        label = f"{name} {n}"
        lw = d.textlength(label, font=F_TAB)
        d.rounded_rectangle([tx, ty, tx + lw + 14, ty + 18], radius=4,
                            fill=NAVY2)
        d.text((tx + 7, ty + 3), label, font=F_TAB, fill=(255, 255, 255))
        tx += lw + 14 + 5
    assert tx <= 1000, tx

    # ================= 3 HEROES =================
    heroes = [
        dict(bg=HERO1, kick="WEATHER  \u2022  U.S. EAST COAST  \u2022  OFFICIAL",
             num="900,000+", head="WITHOUT POWER",
             sub="Nor'easter hits Thanksgiving",
             att=("820+ flights cancelled; gusts to ~70 mph. Macy's "
                  "Parade moved to Sat 28 Nov."),
             chip="NJ EMERGENCY: 21 COUNTIES"),
        dict(bg=HERO2, kick="MIDDLE EAST  \u2022  GULF  \u2022  CONFIRMED",
             num="3 DEAD", head="GULF ATTACKS ESCALATE",
             sub="Brent $96.57 \u2014 highest since 6 Nov",
             att=("2 Italians killed in Kuwait, 1 Nepali dead at Jazan. "
                  "Iran denies attack (CLAIM)."),
             chip="BRENT +2.1% IN ONE DAY"),
        dict(bg=HERO3, kick="EUROPE  \u2022  WAR IN UKRAINE  \u2022  REPORTED",
             num="55,629", head="RUSSIAN LOSSES",
             sub="Killed or wounded \u2014 record",
             att=("Zelensky warns of a new mass strike on energy. "
                  "Ukraine drones hit Slavyansk refinery."),
             chip=">2,200 LOSSES A DAY"),
    ]
    HW, HH = 320, 192
    for i, h in enumerate(heroes):
        x = 24 + i * (HW + 8)
        y = 108
        d.rectangle([x, y, x + HW, y + HH], fill=h["bg"])
        d.rectangle([x, y, x + HW, y + 4], fill=GOLD)
        px = x + 16
        d.text((px, y + 10), h["kick"], font=F_KICK, fill=GOLD)
        d.text((px, y + 28), h["num"], font=F_HERO_NUM, fill=(255, 255, 255))
        head_lines = wrap(d, h["head"], F_HERO_H, HW - 32)
        assert len(head_lines) <= 1, (h["kick"], head_lines)
        text_block(d, px, y + 80, head_lines, F_HERO_H,
                   (255, 255, 255), 25)
        sub_lines = wrap(d, h["sub"], F_HERO_SUB, HW - 32)
        assert len(sub_lines) <= 1, (h["kick"], sub_lines)
        text_block(d, px, y + 108, sub_lines, F_HERO_SUB,
                   (220, 226, 235), 17)
        att_lines = wrap(d, h["att"], F_HERO_ATT, HW - 32)
        assert len(att_lines) <= 2, (h["kick"], att_lines)
        text_block(d, px, y + 128, att_lines, F_HERO_ATT,
                   (196, 205, 218), 15)
        cw = d.textlength(h["chip"], font=F_CHIP) + 20
        assert cw <= HW - 32, (h["kick"], cw)
        d.rounded_rectangle([px, y + HH - 30, px + cw, y + HH - 30 + 22],
                            radius=4, fill=RED)
        d.text((px + 10, y + HH - 25), h["chip"], font=F_CHIP,
               fill=(255, 255, 255))

    # ================= 10 MEDIUM CARDS (5 x 2) =================
    cards = [
        dict(bar=STEEL, kick="OCEANIA  \u2022  OFFICIAL",
             head="NZ ELECTION DEADLOCK",
             body="Final count: coalition 65/130, one short; Opportunity (7 seats) is kingmaker.",
             stat="27 NOV  \u2022  PM LUXON"),
        dict(bar=RED, kick="HEALTH  \u2022  CONFIRMED",
             head="EBOLA: 12,021 CASES, 5,904 DEAD",
             body="2nd-largest outbreak ever; fastest-growing; Bundibugyo, no approved vaccine.",
             stat="26 NOV DATA  \u2022  8 PROVINCES"),
        dict(bar=FIRE, kick="DISASTER  \u2022  CONFIRMED",
             head="CAIRO TANKER BLAST: 31 DEAD",
             body="25 Nov blast; driver arrested after admitting 110 km/h; 21 hurt, 27 vehicles burnt.",
             stat="25 NOV  \u2022  ARREST 26 NOV"),
        dict(bar=NAVY2, kick="DIPLOMACY  \u2022  CONFIRMED",
             head="TRUMP TO PUTIN: PULL BACK",
             body="Truth Social: end all military aggression in Europe.",
             stat="26 NOV  \u2022  MAR-A-LAGO"),
        dict(bar=RED2, kick="MIDDLE EAST  \u2022  REPORTED",
             head="ISRAEL KILLS 9 IN GAZA",
             body="Senior Hamas official Abu Nada + wife killed in Deir al-Balah; 3rd night of strikes.",
             stat="25\u201326 NOV  \u2022  CEASEFIRE HOLDS"),
        dict(bar=AMBER, kick="JUSTICE  \u2022  CONFIRMED",
             head="MYANMAR REJECTS ICJ RULING",
             body="Min Aung Hlaing refuses full compliance; ICJ ruled genocide on 19 Nov \u2014 a first.",
             stat="25 NOV  \u2022  RULING 19 NOV"),
        dict(bar=TEAL, kick="SECURITY  \u2022  REPORTED",
             head="KIM ORDERS MORE NUKES",
             body="Inspects nuclear site 25 Nov; wider tactical deployment; Hwasan-31 warheads shown.",
             stat="25 NOV  \u2022  KCNA 26 NOV"),
        dict(bar=GREEN, kick="ECONOMY  \u2022  OFFICIAL",
             head="S. KOREA RATE UP TO 3.25%",
             body="Bank of Korea +25bp, 5\u20132 vote; 3rd hike since July; GDP forecast raised to 3.9%.",
             stat="26 NOV  \u2022  3.25%  \u2022  5\u20132"),
        dict(bar=STEEL, kick="TECH LAW  \u2022  OFFICIAL",
             head="AUSTRALIA: DUTY OF CARE",
             body="Big Tech fines up to 5% of global revenue; users can opt out of algorithms.",
             stat="25 NOV  \u2022  97\u201343 + 36\u201323"),
        dict(bar=AMBER, kick="SPORT  \u2022  CONFIRMED",
             head="EUROPA LEAGUE: PLZEN 4\u20130",
             body="Benfica's perfect run ends; Milan come back 2\u20134; Bournemouth 5/5, a first.",
             stat="26 NOV  \u2022  MD5  \u2022  56 GOALS"),
    ]
    CW, CH = 188, 118
    for i, c in enumerate(cards):
        x = 24 + (i % 5) * (CW + 9)
        y = 308 + (i // 5) * (CH + 8)
        d.rectangle([x, y, x + CW, y + CH], fill=CARD)
        d.rectangle([x, y, x + CW, y + 5], fill=c["bar"])
        d.rectangle([x, y, x + 5, y + CH], fill=c["bar"])
        px, py = x + 12, y + 10
        d.text((px, py), c["kick"], font=F_MED_K, fill=c["bar"])
        head_lines = wrap(d, c["head"], F_MED_H, CW - 24)
        assert len(head_lines) <= 2, (c["kick"], head_lines)
        hy = text_block(d, px, py + 15, head_lines, F_MED_H, INK, 16)
        body_lines = wrap(d, c["body"], F_MED_B, CW - 24)
        assert len(body_lines) <= 3, (c["kick"], body_lines)
        text_block(d, px, hy + 2, body_lines, F_MED_B, MUTED, 13)
        d.rectangle([x + 5, y + CH - 20, x + CW, y + CH], fill=STAT_BG)
        d.text((px, y + CH - 16), c["stat"], font=F_MED_S, fill=c["bar"])

    # ================= TIMELINE STRIP (UTC) =================
    TY = 552
    d.rectangle([0, TY, W, TY + 44], fill=(233, 228, 216))
    d.rectangle([0, TY, W, TY + 2], fill=GOLD)
    d.text((24, TY + 4), "TIMELINE \u2014 UTC", font=F_TL_H, fill=NAVY)
    tl = [
        [("25 NOV 17:08", "Cairo tanker blast: 31 dead"),
         ("25 NOV 21:22", "Kim nuclear inspection reported"),
         ("26 NOV ~09:00", "Ebola data: 12,021 cases")],
        [("26 NOV", "Nor'easter: 900,000+ lose power"),
         ("27 NOV 01:46", "NZ final count: 65/130"),
         ("27 NOV 14:30", "U.S. markets reopen")],
    ]
    for row, items in enumerate(tl):
        y = TY + 19 + row * 12
        x = 24
        for t, ev in items:
            d.text((x, y), t + "  ", font=F_TL_B, fill=NAVY)
            twd = d.textlength(t + "  ", font=F_TL_B)
            d.text((x + twd, y), ev, font=F_TL, fill=INK)
            x += twd + d.textlength(ev, font=F_TL) + 18
        assert x <= 1000, (row, x)

    # ================= WORLD MAP =================
    MY = 604
    d.rectangle([24, MY, 1000, MY + 180], fill=MAP_SEA)
    d.rectangle([24, MY, 1000, MY + 2], fill=GOLD)
    d.text((36, MY + 8), "WHERE IT HAPPENED \u2014 12 PLACES",
           font=F_MAP_T, fill=(255, 255, 255))
    # schematic continents
    continents = [
        [(70, 640), (150, 625), (230, 635), (260, 660), (240, 690),
         (180, 700), (120, 695), (70, 675)],                                   # N America
        [(250, 705), (290, 710), (300, 745), (270, 775), (245, 745)],          # S America
        [(480, 630), (540, 625), (565, 645), (550, 665), (500, 665),
         (475, 650)],                                                          # Europe
        [(480, 675), (560, 675), (575, 710), (550, 760), (505, 765),
         (480, 720)],                                                          # Africa
        [(580, 630), (860, 625), (900, 650), (880, 700), (800, 715),
         (700, 705), (620, 680), (575, 655)],                                  # Asia
        [(820, 745), (890, 745), (895, 765), (830, 770)],                      # Australia
    ]
    for poly in continents:
        d.polygon(poly, fill=MAP_LAND)
    pins = [(175, 655), (235, 675), (660, 645), (745, 685), (535, 690),
            (600, 640), (880, 720), (505, 735), (568, 712), (760, 640),
            (740, 660), (860, 740)]
    for i, (px, py) in enumerate(pins, start=1):
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED2,
                  outline=(255, 255, 255), width=1)
        num = str(i)
        nw = d.textlength(num, font=F_PIN)
        d.text((px - nw / 2, py - 6), num, font=F_PIN, fill=(255, 255, 255))
    legend = ("1 NYC \u2022 2 US EAST \u2022 3 KUWAIT \u2022 4 JAZAN \u2022 5 KYIV "
              "\u2022 6 SLAVYANSK \u2022 7 WELLINGTON \u2022 8 ITURI \u2022 9 CAIRO "
              "\u2022 10 PYONGYANG \u2022 11 SEOUL \u2022 12 CANBERRA")
    leg_lines = wrap(d, legend, F_MAP_L, 952)
    assert len(leg_lines) <= 1, leg_lines
    text_block(d, 36, MY + 158, leg_lines, F_MAP_L, (205, 212, 224), 13)

    # ================= 22 MORE DATED BRIEFS =================
    BY = 790
    d.text((24, BY), "22 MORE DATED BRIEFS", font=F_BR_H, fill=NAVY)
    briefs = [
        ("23 Nov", "Indonesia mine flood: 13 dead, 13 missing", "CONFIRMED"),
        ("26 Nov", "Costa Rica bars UN rapporteur Albanese at airport", "REPORTED"),
        ("26 Nov", "Hong Kong marks 1 year since fire (168 dead, 2025)", "CONFIRMED"),
        ("24 Nov", "Landmine Monitor: 5 states quit Ottawa treaty", "OFFICIAL"),
        ("26 Nov", "Russia: 343 drones downed; Kyiv: >55% refining hit", "CLAIM"),
        ("27 Nov", "U.S. markets reopen; Nvidia last close $149.30 (25 Nov)", "CONFIRMED"),
        ("27 Nov", "Starshield back to normal in Ukrainian areas", "REPORTED"),
        ("26\u201327 Nov", "Georgia: Russia set to absorb occupied land", "CLAIM"),
        ("24\u201327 Nov", "IISS: Russia subversion risk to EU trains, energy", "REPORTED"),
        ("26\u201327 Nov", "Drone briefly enters Latvia airspace", "REPORTED"),
        ("26 Nov", "Argentina bars central bank money-printing", "REPORTED"),
        ("26 Nov", "Kenya court halts U.S.-backed Ebola facility", "REPORTED"),
        ("26 Nov", "Lebanon transport demos amid fuel emergency", "REPORTED"),
        ("26\u201327 Nov", "EU backs Hern\u00e1ndez de Cos as next ECB chief", "REPORTED"),
        ("26 Nov", "Japan to test 1,000 km missiles on Indian soil", "REPORTED"),
        ("26 Nov", "CENTCOM hails Syria seizing Iran arms for Lebanon", "REPORTED"),
        ("26 Nov", "NATO + Jordan widen military partnership", "REPORTED"),
        ("26 Nov", "Colombia aid for Villavicencio after car bomb", "REPORTED"),
        ("26 Nov", "$500M+ for F-16 upkeep for Ukraine", "REPORTED"),
        ("26\u201327 Nov", "Russian general Grekhov detained in Moscow", "REPORTED"),
        ("26 Nov", "Kushner: Putin 'showed restraint' on nukes", "REPORTED"),
        ("26\u201327 Nov", "Sudan rejects Ethiopian PM dialogue bid", "REPORTED"),
    ]
    col_w = 476
    for i, (dt, txt, lab) in enumerate(briefs):
        col = i // 11
        row = i % 11
        x = 24 + col * (col_w + 12)
        y = BY + 20 + row * 12
        num = f"{14 + i} \u00b7 "
        d.text((x, y), num, font=F_BR_B, fill=NAVY)
        nw = d.textlength(num, font=F_BR_B)
        d.text((x + nw, y), dt + " \u00b7 ", font=F_BR_B, fill=INK)
        dw = d.textlength(dt + " \u00b7 ", font=F_BR_B)
        full = txt + "  [" + lab + "]"
        lines = wrap(d, full, F_BR, col_w - nw - dw)
        assert len(lines) <= 1, (14 + i, full)
        d.text((x + nw + dw, y), lines[0], font=F_BR, fill=INK)

    # ================= FOOTER =================
    FY = 956
    d.rectangle([0, FY, W, H], fill=NAVY)
    d.rectangle([0, FY, W, FY + 2], fill=GOLD)
    dc = ("DATE CHECK \u2014 EXCLUDED: Hong Kong fire was 26 Nov 2025, not "
          "2026 (26 Nov 2026 is the 1-year mark) \u2022 ICJ Myanmar ruling "
          "was 19 Nov (rejection 25 Nov) \u2022 Macy's Parade did NOT run "
          "26 Nov \u2014 postponed to 28 Nov \u2022 No Nvidia close 27 Nov yet "
          "\u2014 last close $149.30 (25 Nov) \u2022 55,629 = killed OR wounded")
    dc_lines = wrap(d, dc, F_FOOT, W - 48)
    assert len(dc_lines) <= 2, dc_lines
    ly = text_block(d, 24, FY + 7, dc_lines, F_FOOT, (205, 212, 224), 13)
    hs = ("HOW SURE: OFFICIAL = official statement/document \u2022 CONFIRMED = "
          "2+ independent sources \u2022 REPORTED = media report \u2022 CLAIM = "
          "one-sided claim, no public evidence")
    hs_lines = wrap(d, hs, F_FOOT, W - 48)
    assert len(hs_lines) <= 1, hs_lines
    ly = text_block(d, 24, ly + 1, hs_lines, F_FOOT, (160, 170, 185), 13)
    src = ("Sources: Reuters \u2022 WSJ \u2022 AP \u2022 The Times \u2022 NWS/NOAA "
           "\u2022 PowerOutage.us \u2022 Ukrinform \u2022 KCNA \u2022 UEFA.com "
           "\u2022 Electoral Commission NZ \u2022 Finnhub \u2022 ICBL")
    sw = d.textlength(src, font=F_SRC)
    d.text(((W - sw) / 2, H - 17), src, font=F_SRC, fill=(140, 150, 165))

    img.save(OUT, format="PNG")
    data = open(OUT, "rb").read()
    print(f"wrote {OUT} ({len(data)} bytes, "
          f"sha256={hashlib.sha256(data).hexdigest()})")


if __name__ == "__main__":
    main()
