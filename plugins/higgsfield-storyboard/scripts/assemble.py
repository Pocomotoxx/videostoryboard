#!/usr/bin/env python3
"""Jóváhagyott jelenetek összefűzése helyben, ffmpeggel.

A Higgsfield klipek rövidek (jellemzően legfeljebb 15 mp), ezért a kész
videó mindig több darabból áll össze. Ez a lépés nem az MCP-n keresztül
fut, hanem a saját gépeden, így nem kerül kreditbe és korlátlanul
ismételhető.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys

# Windowson a konzol alapértelmezett kódlapja cp1252, amin az ő és ű betű
# UnicodeEncodeError-ral elszáll. Minden kimenetet UTF-8-ra állítunk.
for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")

ASPECT = {"16:9": (1920, 1080), "9:16": (1080, 1920), "1:1": (1080, 1080),
          "4:5": (1080, 1350)}


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode:
        print(p.stderr[-2000:], file=sys.stderr)
        sys.exit(f"ffmpeg hiba: {' '.join(cmd[:6])} ...")


def run_in(cwd, cmd):
    """Ugyanaz, mint a run(), de adott munkakönyvtárból.

    A feliratszűrő útvonalkezelése platformfüggő és kényes (Windowson a meghajtóbetű
    kettőspontját is escape-elni kellene), ezért a feliratfájlra mindig puszta
    fájlnévvel hivatkozunk, a munkakönyvtárból.
    """
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if p.returncode:
        print(p.stderr[-2000:], file=sys.stderr)
        sys.exit(f"ffmpeg hiba: {' '.join(cmd[:6])} ...")


def fix_ass(path, w, h):
    """A felirat vászonméretét a videóhoz igazítja, a betűméretet a magassághoz.

    Így a felirat 16:9-ben és 9:16-ban is ugyanakkora arányban látszik.
    """
    fontsize = max(16, round(h / 26))
    margin = max(20, round(h / 24))
    out = []
    for sor in open(path, encoding="utf-8-sig").read().splitlines():
        if sor.startswith("PlayResX:"):
            sor = f"PlayResX: {w}"
        elif sor.startswith("PlayResY:"):
            sor = f"PlayResY: {h}"
        elif sor.startswith("Style: "):
            # Az ASS stílussor mezősorrendje kötött; a fontosak indexe:
            # 2 betűméret, 15 keretstílus, 16 keretvastagság, 17 árnyék,
            # 18 igazítás, 21 alsó margó.
            mezok = sor[len("Style: "):].split(",")
            if len(mezok) >= 23:
                mezok[2] = str(fontsize)
                mezok[15] = "3"               # keret helyett háttérdoboz
                mezok[16] = "2"
                mezok[17] = "0"
                mezok[18] = "2"               # alul középre
                mezok[21] = str(margin)
                sor = "Style: " + ",".join(mezok)
        out.append(sor)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", default=".")
    ap.add_argument("--aspect", default="16:9", choices=list(ASPECT))
    ap.add_argument("--music", help="zenei alapsáv fájl")
    ap.add_argument("--music-db", type=float, default=-18.0, help="zene hangereje dB-ben")
    ap.add_argument("--subtitles", help="SRT feliratfájl, ráégetve a képre")
    ap.add_argument("--no-loudnorm", action="store_true",
                    help="a hangerő egységesítésének kihagyása")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    if not shutil.which("ffmpeg"):
        sys.exit("Nincs telepítve ffmpeg.")

    board = json.load(open(os.path.join(args.project, "storyboard.json"), encoding="utf-8"))
    order = board.get("assembly", {}).get("sorrend") or [s["id"] for s in board["shots"]]
    by_id = {s["id"]: s for s in board["shots"]}

    w, h = ASPECT[args.aspect]
    tmp = os.path.join(args.project, "output", "_tmp")
    os.makedirs(tmp, exist_ok=True)

    # 1. minden klip azonos felbontásra, képkockasebességre és hangformátumra
    norm = []
    for sid in order:
        src = os.path.join(args.project, by_id[sid].get("video") or f"shots/{sid}.mp4")
        if not os.path.exists(src):
            sys.exit(f"Hiányzó jelenet: {src}")
        dst = os.path.join(tmp, f"{sid}.mp4")
        vf = (f"scale={w}:{h}:force_original_aspect_ratio=increase,"
              f"crop={w}:{h},fps=30,format=yuv420p")
        run(["ffmpeg", "-y", "-i", src, "-vf", vf,
             "-c:v", "libx264", "-crf", "18", "-preset", "medium",
             "-af", "aresample=48000", "-c:a", "aac", "-b:a", "192k",
             "-shortest", dst])
        norm.append(dst)

    # 2. összefűzés
    lst = os.path.join(tmp, "concat.txt")
    with open(lst, "w", encoding="utf-8") as f:
        for p in norm:
            f.write(f"file '{os.path.abspath(p)}'\n")
    joined = os.path.join(tmp, "joined.mp4")
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", joined])

    # 3. felirat ráégetése
    if args.subtitles:
        srt = os.path.abspath(args.subtitles)
        if not os.path.exists(srt):
            sys.exit(f"Nincs meg a feliratfájl: {srt}")
        # A subtitles szűrő útvonalkezelése platformfüggő és kényes (Windowson a
        # meghajtóbetű kettőspontja is escape-elendő), ezért a fájlt a munkakönyvtárba
        # másoljuk, és onnan, puszta fájlnévvel hivatkozunk rá.
        shutil.copyfile(srt, os.path.join(tmp, "felirat.srt"))
        # Az SRT-t előbb ASS-re alakítjuk, mert csak ott adható meg a felirat saját
        # vászonmérete. Enélkül a szűrő egy alapértelmezett kis felbontásból nagyít,
        # és a betűméret a videó felbontásától függően elszáll.
        run_in(tmp, ["ffmpeg", "-y", "-i", "felirat.srt", "felirat.ass"])
        fix_ass(os.path.join(tmp, "felirat.ass"), w, h)
        subbed = os.path.join(tmp, "subbed.mp4")
        run_in(tmp, ["ffmpeg", "-y", "-i", os.path.abspath(joined), "-vf", "ass=felirat.ass",
                     "-c:v", "libx264", "-crf", "18", "-preset", "medium",
                     "-c:a", "copy", os.path.abspath(subbed)])
        joined = subbed

    # 4. zenei alapsáv és hangerő-egységesítés
    out = args.out or os.path.join(
        args.project, "output", f"{board.get('nev', 'vagas')}_{args.aspect.replace(':', 'x')}.mp4")
    # A loudnorm a teljes műsorhangerőt hozza egységes szintre. Enélkül a jelenetek
    # hangereje ugrál, mert minden klip külön generálásból származik.
    norm_af = "" if args.no_loudnorm else ",loudnorm=I=-16:TP=-1.5:LRA=11"
    if args.music:
        run(["ffmpeg", "-y", "-i", joined, "-i", args.music,
             "-filter_complex",
             f"[1:a]volume={args.music_db}dB,afade=t=out:st=0:d=2[m];"
             f"[0:a][m]amix=inputs=2:duration=first:dropout_transition=0{norm_af}[a]",
             "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", out])
    elif not args.no_loudnorm:
        run(["ffmpeg", "-y", "-i", joined, "-af", norm_af.lstrip(","),
             "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", out])
    else:
        shutil.move(joined, out)

    shutil.rmtree(tmp, ignore_errors=True)
    print(f"Kész: {out}")


if __name__ == "__main__":
    main()
