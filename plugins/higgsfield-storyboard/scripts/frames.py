#!/usr/bin/env python3
"""Képkockák kimentése egy klipből, hogy a modell meg tudja nézni az eredményt.

A generálás nem determinisztikus, és a modell nem tudja megítélni a saját eredményét,
ha nem is látja. Ez a script egyenletesen elosztott képkockákat ment ki egy klipből,
lekicsinyítve, hogy a modell `Read` hívással végignézhesse őket, mielőtt a felhasználó
elé teszi.

Ez nem helyettesíti az emberi jóváhagyást, csak kiszűri a nyilvánvaló hibákat, mielőtt
azok a felhasználó idejét fogyasztanák.
"""

import argparse
import os
import shutil
import subprocess
import sys

for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")


def hossz(video):
    p = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nw=1:nk=1", video], capture_output=True, text=True)
    if p.returncode:
        sys.exit(f"Nem olvasható a klip hossza: {video}")
    try:
        return float(p.stdout.strip())
    except ValueError:
        sys.exit(f"Értelmezhetetlen hossz: {p.stdout.strip()!r}")


def main():
    ap = argparse.ArgumentParser(description="Képkockák kimentése ellenőrzéshez")
    ap.add_argument("video", help="a vizsgálandó videófájl")
    ap.add_argument("--db", type=int, default=6, help="hány képkocka (alap: 6)")
    ap.add_argument("--szelesseg", type=int, default=768,
                    help="a kimentett kockák szélessége képpontban (alap: 768)")
    ap.add_argument("--ki", default=None, help="célkönyvtár (alap: a videó melletti _kockak)")
    args = ap.parse_args()

    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        sys.exit("Nincs telepítve ffmpeg.")
    if not os.path.exists(args.video):
        sys.exit(f"Nincs meg a fájl: {args.video}")
    if args.db < 1:
        sys.exit("legalább egy képkocka kell")

    d = hossz(args.video)
    ki = args.ki or os.path.join(os.path.dirname(os.path.abspath(args.video)), "_kockak")
    os.makedirs(ki, exist_ok=True)
    alap = os.path.splitext(os.path.basename(args.video))[0]

    # A szélső kockákat kerüljük: az első és az utolsó gyakran fekete vagy elmosódott.
    utak = []
    for i in range(args.db):
        t = d * (i + 0.5) / args.db
        cel = os.path.join(ki, f"{alap}_{i + 1:02d}.jpg")
        p = subprocess.run(
            ["ffmpeg", "-y", "-ss", f"{t:.3f}", "-i", args.video, "-frames:v", "1",
             "-vf", f"scale={args.szelesseg}:-2", "-q:v", "3", cel],
            capture_output=True, text=True)
        if p.returncode:
            print(p.stderr[-800:], file=sys.stderr)
            sys.exit(f"ffmpeg hiba a(z) {t:.2f}. másodpercnél")
        utak.append((t, cel))

    print(f"\n  {os.path.basename(args.video)} — {d:.1f} mp, {args.db} képkocka\n")
    for t, u in utak:
        print(f"  {t:6.2f} mp  {u}")
    print("\n  Nézd végig őket Read hívással, mielőtt a felhasználó elé teszed.\n")


if __name__ == "__main__":
    main()
