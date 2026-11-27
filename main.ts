// The World Today — 27 November 2026 in one image
// (make.fun news-image-20261127 entry).
//
// Friday 27 November 2026's world news, drawn as a single
// broadsheet front page with 35 dated stories across 9 regions:
// three heroes — a Thanksgiving nor'easter leaving 900,000+
// without power on the U.S. East Coast as the 100th Macy's Parade
// is postponed to Saturday 28 Nov (first postponement in 100
// years); Gulf attacks escalating (2 Italians killed in Kuwait,
// 1 Nepali dead at the Jazan refinery, Brent $96.57 — highest
// since 6 Nov; Iran denies the Kuwait attack); Ukraine's record
// 55,629 Russian losses in 25 days (killed or wounded, Ukraine
// claim) as Zelensky warns of a new mass strike — plus
// ten medium cards (NZ election deadlock, Ebola 12,021 cases,
// Cairo tanker blast 31 dead, Trump to Putin, Israel kills 9 in
// Gaza, Myanmar rejects the ICJ ruling, Kim orders more nukes,
// South Korea's rate up to 3.25%, Australia's Digital Duty of
// Care, Europa League MD5), a UTC timeline strip, a world map
// with 12 numbered pins, 22 more dated briefs, a DATE CHECK
// footer, and a HOW SURE verification legend
// (OFFICIAL / CONFIRMED / REPORTED / CLAIM).
// Sources: Reuters, WSJ, AP, The Times, NWS/NOAA, PowerOutage.us,
// Ukrinform, KCNA, UEFA.com, Electoral Commission NZ, Finnhub, ICBL.
//
// Accuracy notes (from research-2026-11-27.md): the Hong Kong fire
// was 26 Nov 2025, not 2026 (26 Nov 2026 is the 1-year mark);
// Nvidia's last verified close is $149.30 on 25 Nov (the 27 Nov
// close was not yet out at build time — never invented); 55,629
// is killed OR wounded (Ukraine claim), never deaths; the Gulf
// incidents are four separate events, never one combined attack;
// the Macy's Parade did NOT run on 26 Nov (postponed to 28 Nov);
// the ICJ Myanmar ruling was 19 Nov (rejection 25 Nov); Ebola
// uses the new 12,021 / 5,904 figures (data 26 Nov).
//
// The page was rendered ahead of time with Python + Pillow (flat
// colours, simple pictograms, DejaVu type) into entry.png, which
// sits next to this file. This program has one job only: place an
// exact copy of that image at $MAKEFUN_OUTPUT_DIR/entry.png
// (default /output/entry.png) and prove the copy is intact. It
// needs no network and takes no arguments.
//
// Local check:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
//   sha256sum out/entry.png entry.png   # the two hashes must match

import { createHash } from "node:crypto";
import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const MAX_BYTES = 1024 * 1024; // the rules cap the image at 1 MiB
const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const EXPECTED_WIDTH = 1024;
const EXPECTED_HEIGHT = 1024;
const ENTRY_FILENAME = "entry.png";

function digest(bytes) {
  return createHash("sha256").update(bytes).digest("hex");
}

function readBundledImage(path) {
  // The bundled image must exist, be a genuine PNG, and fit the size
  // cap — verify all three before writing anything to the output dir.
  const info = statSync(path, { throwIfNoEntry: false });
  if (info === undefined) {
    throw new Error(`bundled entry.png is missing: ${path}`);
  }
  if (info.size > MAX_BYTES) {
    throw new Error(`entry.png is ${info.size} bytes, over the 1 MiB limit`);
  }
  const bytes = readFileSync(path);
  if (!bytes.subarray(0, PNG_MAGIC.length).equals(PNG_MAGIC)) {
    throw new Error("entry.png does not start with the PNG magic bytes");
  }
  // The PNG header (IHDR) stores the pixel dimensions at fixed offsets;
  // this entry must be exactly 1024x1024, so check both numbers.
  const [picWidth, picHeight] = [bytes.readUInt32BE(16), bytes.readUInt32BE(20)];
  if (picWidth !== EXPECTED_WIDTH || picHeight !== EXPECTED_HEIGHT) {
    throw new Error(
      `entry.png is ${picWidth}x${picHeight}, expected ${EXPECTED_WIDTH}x${EXPECTED_HEIGHT}`,
    );
  }
  return bytes;
}

function main() {
  const destDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
  const here = dirname(fileURLToPath(import.meta.url));
  const bundled = join(here, ENTRY_FILENAME);
  const target = join(destDir, ENTRY_FILENAME);

  const image = readBundledImage(bundled);

  mkdirSync(destDir, { recursive: true });
  copyFileSync(bundled, target);

  // Read the copy back and compare it byte for byte: a truncated or
  // corrupted write must fail loudly instead of grading a broken image.
  const delivered = readFileSync(target);
  if (!delivered.equals(image)) {
    throw new Error("output entry.png differs from the bundled entry.png");
  }
  console.log(
    `wrote ${target} (${delivered.length} bytes, sha256=${digest(delivered)}, verified identical)`,
  );
}

main();
