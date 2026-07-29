#!/usr/bin/env python3
"""Vágópontok illesztése a zene ütemére.

Erős ritmusú zenénél a néző azonnal észreveszi, ha a vágás nem ütemre esik —
akkor is, ha nem tudja megnevezni, mi a baj. A tapasztalat szerint körülbelül
három képkocka az érzékelési határ: ennél nagyobb csúszás már látszik.

Ez a script nem elemzi a zenét, csak számol. A BPM-et a zene forrása többnyire
megadja; ha nem, a felhasználó megmérheti egy ütemkopogtatóval. Így nincs
szükség külön hangelemző könyvtárra.
"""

import argparse
import json
import os
import sys

for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")


def main():
    ap = argparse.ArgumentParser(description="Ütemre illesztett vágáshosszak")
    ap.add_argument("--bpm", type=float, required=True, help="a zene tempója")
    ap.add_argument("--utem", type=int, default=4, help="ütés per ütem (alap: 4)")
    ap.add_argument("--fps", type=int, default=30, help="képkocka/másodperc (alap: 30)")
    ap.add_argument("--kezdet", type=float, default=0.0,
                    help="az első ütés helye másodpercben, ha a zene nem ütéssel indul")
    ap.add_argument("--hossz", type=float, help="célhossz másodpercben, javaslatkéréshez")
    ap.add_argument("--project", help="projektkönyvtár: a storyboard.json vágásainak ellenőrzése")
    args = ap.parse_args()

    if args.bpm <= 0:
        sys.exit("a BPM pozitív legyen")

    utes = 60.0 / args.bpm
    bar = utes * args.utem
    print(f"\n  {args.bpm:g} BPM, {args.utem}/4 — egy ütés {utes:.3f} mp, "
          f"egy ütem {bar:.3f} mp")
    print(f"  Egy képkocka {1 / args.fps * 1000:.1f} ms, a tűréshatár "
          f"{3 / args.fps * 1000:.0f} ms (3 képkocka)\n")

    if args.hossz:
        print("  Ütemre eső jelenethosszak (ennyit válassz a jelenetlistába):")
        for db in (1, 2, 3, 4, 6, 8):
            h = bar * db
            if h <= 15.0001:
                print(f"    {db:>2} ütem = {h:6.3f} mp")
        n = round(args.hossz / bar)
        print(f"\n  A {args.hossz:g} mp-es célhossz {n} ütem "
              f"({n * bar:.3f} mp), ez {n * bar - args.hossz:+.3f} mp eltérés.")
        print(f"  Például {n} ütem felosztható így: "
              f"{' + '.join(str(x) for x in bontas(n))} ütem\n")

    if args.project:
        p = os.path.join(args.project, "storyboard.json")
        if not os.path.exists(p):
            sys.exit(f"nincs meg: {p}")
        shots = json.load(open(p, encoding="utf-8")).get("shots", [])
        if not shots:
            sys.exit("üres a jelenetlista")
        print("  Vágópontok ellenőrzése:\n")
        t, baj = 0.0, 0
        for s in shots:
            t += s.get("duration_s", 5)
            # a legközelebbi ütés távolsága
            k = (t - args.kezdet) / utes
            csuszas = abs(k - round(k)) * utes
            kocka = csuszas * args.fps
            jel = "ok" if kocka <= 3 else "CSÚSZIK"
            if kocka > 3:
                baj += 1
            print(f"    {s.get('id', '?'):<6} vágás {t:6.2f} mp-nél   "
                  f"{kocka:4.1f} képkocka az ütéstől   {jel}")
        print()
        if baj:
            print(f"  {baj} vágás csúszik. Igazítsd a jelenethosszakat ütemre eső "
                  f"értékekre, vagy hagyd el a kockapontos illesztést.\n")
            sys.exit(1)
        print("  Minden vágás ütemre esik.\n")


def bontas(n):
    """Egy ütemszám felosztása változatos, de ütemre eső jelenethosszakra."""
    ki = []
    while n > 0:
        d = 4 if n >= 4 else (2 if n >= 2 else 1)
        ki.append(d)
        n -= d
    return ki


if __name__ == "__main__":
    main()
