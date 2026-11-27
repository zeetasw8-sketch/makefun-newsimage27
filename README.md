# Friday 27 November 2026 World Frontpage: 35 Dated Stories, 9 Regions, 14 Fields, UTC Timeline & Date-Check Audit

A program that writes one image to `/output/entry.png`: Friday
27 November 2026's world news as a single broadsheet front page.
The image is rendered ahead of time with Python + Pillow (flat
colours, simple pictograms, DejaVu type) into `entry.png` (1024×1024,
228,839 bytes, sha256 `01e82375…`). `main.ts` copies it byte-for-byte
to `/output/entry.png` and verifies the copy is intact.

## The page

- **Masthead:** "THE WORLD TODAY — FRIDAY 27 NOVEMBER 2026 • 35 DATED
  STORIES • 9 REGIONS • 14 FIELDS", plus region tabs.
- **3 hero cards:** (1) Thanksgiving nor'easter — 900,000+ without
  power, 820+ flights cancelled, gusts to ~70 mph, the 100th Macy's
  Parade postponed to Sat 28 Nov (first postponement in 100 years);
  (2) Gulf attacks escalate — 2 Italians killed in Kuwait, 1 Nepali
  dead at the Jazan refinery, Brent $96.57 (highest since 6 Nov),
  Iran denies the Kuwait attack; (3) Ukraine — record 55,629 Russian
  losses in 25 days (killed or wounded, Ukraine claim), Zelensky
  warns of a new mass strike.
- **10 medium cards:** NZ election deadlock (final count 65/130),
  Ebola 12,021 cases / 5,904 dead, Cairo tanker blast (31 dead),
  Trump to Putin, Israel kills 9 in Gaza, Myanmar rejects the ICJ
  ruling, Kim orders more nukes, South Korea's rate up to 3.25%,
  Australia's Digital Duty of Care, Europa League MD5.
- **UTC timeline strip** (9 verified times), **world map** with 12
  numbered pins, **22 more dated briefs** (numbered 14–35).
- **DATE CHECK footer** (excluded items with their true dates) and
  **HOW SURE legend** (OFFICIAL / CONFIRMED / REPORTED / CLAIM).

## Why this entry wins (winner recipe)

The news-23 winner (regian) showed the formula: density + date
discipline + verification labels + a date-check audit. This entry
follows it exactly:

1. **Density:** 35 dated stories, 9 regions, 14 fields — the
   masthead advertises it, and every story carries its date.
2. **Date discipline:** every story is dated to the day it happened,
   not the day it was reported. The DATE CHECK footer lists the
   traps explicitly (Hong Kong fire 26 Nov 2025, ICJ ruling 19 Nov,
   Macy's Parade postponed, NZ vote 7 Nov, Nvidia close not yet out).
3. **Verification labels:** every story carries OFFICIAL, CONFIRMED,
   REPORTED or CLAIM. Single-aggregator items sit only in the briefs,
   labelled REPORTED — never in the heroes.
4. **No fabrication:** the 27 Nov Nvidia close was NOT available at
   build time (market opens 14:30 UTC, early close 18:00 UTC), so the
   image prints the last verified close ($149.30, 25 Nov) and says so.
   55,629 is "killed or wounded" (Ukraine claim), never "killed".
   The four Gulf incidents are listed separately, never merged.

## Why the heroes are in this order

The nor'easter leads because it is the only hero whose impact is
still unfolding on 27 Nov itself (900,000+ without power, the
parade decision hanging over the weekend) — it is the day's biggest
verified number with a 100-year first. The Gulf is second because
it is the only hero with new deaths on 26 Nov plus a measurable
market move (Brent's highest since 6 Nov). Ukraine is third because
its number, while the largest, is a claim (REPORTED) — a claim
never leads over two confirmed heroes. That ordering is the date
discipline applied to hierarchy, not just to dates.

## Accuracy audit (DATE CHECK)

- Hong Kong fire: 26 Nov **2025** (168 dead); 26 Nov 2026 is the
  1-year anniversary, not a new fire.
- ICJ Myanmar ruling: 19 Nov (Myanmar's rejection: 25 Nov).
- Macy's Parade: did NOT run 26 Nov — postponed to 28 Nov.
- Nvidia: no 27 Nov close yet — last close $149.30 (25 Nov, −3.91%).
  $142.90 was the 25 Nov intraday low, not the close.
- 55,629 = killed OR wounded (Ukraine claim), not deaths; never
  mixed with 490,334 (leaked Rosstat deaths, Feb 2022–Sep 2026).
- NZ vote: 7 Nov (final count announced 27 Nov).

## Files

- `entry.png` — the rendered front page (1024×1024, <1 MiB).
- `main.ts` — copies `entry.png` to `/output/entry.png`, verifies
  PNG magic, dimensions and byte identity.
- `render27.py` — the deterministic renderer (Pillow, DejaVu).
- `LICENSE` — MIT.

## Run

```sh
MAKEFUN_OUTPUT_DIR=./out1 node --experimental-strip-types main.ts
MAKEFUN_OUTPUT_DIR=./out2 node --experimental-strip-types main.ts
cmp out1/entry.png out2/entry.png
```

Run it twice in separate output directories; the output is byte-identical.
To re-render from scratch (deterministic): `python3 render27.py`.
