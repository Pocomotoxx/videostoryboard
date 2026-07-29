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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", default=".")
    ap.add_argument("--aspect", default="16:9", choices=list(ASPECT))
    ap.add_argument("--music", help="zenei alapsáv fájl")
    ap.add_argument("--music-db", type=float, default=-18.0, help="zene hangereje dB-ben")
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

    # 3. zenei alapsáv
    out = args.out or os.path.join(
        args.project, "output", f"{board.get('nev', 'vagas')}_{args.aspect.replace(':', 'x')}.mp4")
    if args.music:
        run(["ffmpeg", "-y", "-i", joined, "-i", args.music,
             "-filter_complex",
             f"[1:a]volume={args.music_db}dB,afade=t=out:st=0:d=2[m];"
             f"[0:a][m]amix=inputs=2:duration=first:dropout_transition=0[a]",
             "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", out])
    else:
        shutil.move(joined, out)

    shutil.rmtree(tmp, ignore_errors=True)
    print(f"Kész: {out}")


if __name__ == "__main__":
    main()
