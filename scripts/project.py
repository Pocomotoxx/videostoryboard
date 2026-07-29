#!/usr/bin/env python3
"""Rétegelt AI-videóprojekt állapotgépe.

A projekt build-rendszerként működik. Minden node tárolja a bemeneteinek
ujjlenyomatát; ha egy réteg megváltozik, a ráépülő rétegek elévülnek és
újra jóváhagyást igényelnek.

A `can-spend` parancs a rendszer egyetlen kemény szabálya: generáló
MCP-hívás csak akkor futhat, ha minden szülő node jóváhagyott és friss.
"""

import argparse
import hashlib
import json
import os
import sys
import time

# Windowson a konzol alapértelmezett kódlapja cp1252, amin az ő és ű betű
# UnicodeEncodeError-ral elszáll. Minden kimenetet UTF-8-ra állítunk.
for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")

STATE = "project.json"
BOARD = "storyboard.json"

# Alapértelmezett kreditköltségek. Kalibráld a saját Higgsfield-csomagodhoz,
# mert modellenként és felbontásonként eltér.
DEFAULT_COSTS = {
    "image": 5,
    "video_per_second": 10,
    "character_train": 60,
    "upscale": 20,
}

LAYERS = {
    "brief": 0,
    "treatment": 1,
    "shotlist": 2,
    "look": 3,
    "assembly": 6,
    "sound": 7,
    "finish": 8,
}


def die(msg, code=1):
    print(f"HIBA: {msg}", file=sys.stderr)
    sys.exit(code)


def sha(*parts):
    h = hashlib.sha256()
    for p in parts:
        h.update(str(p).encode("utf-8"))
    return h.hexdigest()[:16]


def file_hash(path):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()[:16]


def load(root):
    p = os.path.join(root, STATE)
    if not os.path.exists(p):
        die(f"nincs {STATE} ebben a könyvtárban: {root}. Futtasd: project.py init <nev>")
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def save(root, state):
    with open(os.path.join(root, STATE), "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def load_board(root):
    p = os.path.join(root, BOARD)
    if not os.path.exists(p):
        return {"look": {}, "shots": []}
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def new_node(layer, deps):
    return {
        "layer": layer,
        "deps": deps,
        "status": "draft",       # draft | pending | approved | rejected
        "input_hash": "",
        "approved_hash": "",
        "note": "",
        "spend": 0,
        "assets": [],
    }


# ---------------------------------------------------------------- gráf

def sync(root, state):
    """Node-ok újraszámolása a storyboard.json alapján + friss ujjlenyomatok."""
    board = load_board(root)
    nodes = state["nodes"]

    for name, layer in LAYERS.items():
        nodes.setdefault(name, new_node(layer, []))
    nodes["treatment"]["deps"] = ["brief"]
    nodes["shotlist"]["deps"] = ["treatment"]
    nodes["look"]["deps"] = ["treatment"]

    shots = board.get("shots", [])
    shot_ids = [s["id"] for s in shots]

    for s in shots:
        kf = f"keyframe:{s['id']}"
        mo = f"motion:{s['id']}"
        deps_kf = ["shotlist", "look"]
        if s.get("continuity_from"):
            deps_kf.append(f"keyframe:{s['continuity_from']}")
        nodes.setdefault(kf, new_node(4, deps_kf))["deps"] = deps_kf
        nodes.setdefault(mo, new_node(5, [kf]))["deps"] = [kf]

    # elhagyott jelenetek node-jainak takarítása
    for key in list(nodes):
        if ":" in key:
            sid = key.split(":", 1)[1]
            if sid not in shot_ids:
                del nodes[key]

    nodes["assembly"]["deps"] = [f"motion:{i}" for i in shot_ids]
    nodes["sound"]["deps"] = ["assembly"]
    nodes["finish"]["deps"] = ["sound"]

    # saját ujjlenyomatok
    spec = {
        "brief": file_hash(os.path.join(root, "brief.md")),
        "treatment": file_hash(os.path.join(root, "treatment.md")),
        "shotlist": sha(json.dumps(
            [{k: s.get(k) for k in ("id", "duration_s", "shot_size", "angle", "subject")}
             for s in shots], sort_keys=True, ensure_ascii=False)),
        "look": sha(json.dumps(board.get("look", {}), sort_keys=True, ensure_ascii=False)),
        "assembly": sha(json.dumps(board.get("assembly", {}), sort_keys=True, ensure_ascii=False)),
        "sound": sha(json.dumps(board.get("sound", {}), sort_keys=True, ensure_ascii=False)),
        "finish": sha(json.dumps(board.get("finish", {}), sort_keys=True, ensure_ascii=False)),
    }
    for s in shots:
        spec[f"keyframe:{s['id']}"] = sha(json.dumps(s, sort_keys=True, ensure_ascii=False))
        spec[f"motion:{s['id']}"] = sha(json.dumps(
            {k: s.get(k) for k in ("camera_move", "duration_s", "model", "prompt_en", "audio")},
            sort_keys=True, ensure_ascii=False))

    # input_hash topologikusan (réteg szerinti sorrend elég, a gráf DAG)
    for key in sorted(nodes, key=lambda k: (nodes[k]["layer"], k)):
        n = nodes[key]
        parent = "".join(nodes[d]["approved_hash"] for d in n["deps"] if d in nodes)
        n["input_hash"] = sha(spec.get(key, ""), parent)

    state["shot_ids"] = shot_ids
    return state


def effective(state, key, _seen=None):
    """approved | stale | pending | rejected | ready | blocked"""
    nodes = state["nodes"]
    n = nodes[key]
    for d in n["deps"]:
        if d not in nodes:
            continue
        if effective(state, d) != "approved":
            return "blocked"
    if n["status"] == "approved":
        return "approved" if n["approved_hash"] == n["input_hash"] else "stale"
    if n["status"] in ("pending", "rejected"):
        return n["status"]
    return "ready"


MARK = {"approved": "OK ", "stale": "ELÉVÜLT", "pending": "VÁR", "rejected": "ELUTASÍTVA",
        "ready": "MEHET", "blocked": "zárolt"}


# ---------------------------------------------------------------- parancsok

def cmd_init(args):
    root = os.path.abspath(args.name)
    os.makedirs(root, exist_ok=True)
    for d in ("characters", "shots", "output", "delivery"):
        os.makedirs(os.path.join(root, d), exist_ok=True)
    if os.path.exists(os.path.join(root, STATE)):
        die("már létezik projekt ebben a könyvtárban")
    state = {
        "name": args.name,
        "created": time.strftime("%Y-%m-%d %H:%M"),
        "tools": {r: None for r in
                  ("image_gen", "image_to_video", "character_train", "upscale", "history")},
        "costs": dict(DEFAULT_COSTS),
        "nodes": {},
        "spend_log": [],
    }
    for f, txt in (("brief.md", "# Brief\n\n"), ("treatment.md", "# Kezelés\n\n")):
        p = os.path.join(root, f)
        if not os.path.exists(p):
            open(p, "w", encoding="utf-8").write(txt)
    board = os.path.join(root, BOARD)
    if not os.path.exists(board):
        json.dump({"look": {}, "shots": [], "assembly": {}, "sound": {}, "finish": {}},
                  open(board, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    save(root, sync(root, state))
    print(f"Projekt létrehozva: {root}")


def cmd_status(args):
    state = sync(args.project, load(args.project))
    save(args.project, state)
    nodes = state["nodes"]
    print(f"\n{state['name']}\n")
    for key in sorted(nodes, key=lambda k: (nodes[k]["layer"], k)):
        e = effective(state, key)
        n = nodes[key]
        note = f"  <- {n['note']}" if n["note"] and e in ("rejected", "stale") else ""
        cost = f"  [{n['spend']} kredit]" if n["spend"] else ""
        print(f"  {n['layer']}  {MARK[e]:<11} {key}{cost}{note}")
    total = sum(n["spend"] for n in nodes.values())
    print(f"\n  Elköltött kredit összesen: {total}\n")


def cmd_next(args):
    state = sync(args.project, load(args.project))
    save(args.project, state)
    nodes = state["nodes"]
    pend = [k for k in nodes if effective(state, k) == "pending"]
    if pend:
        print("Jóváhagyásra vár, addig ne haladj tovább:")
        for k in sorted(pend):
            print(f"  {k}")
        return
    ready = [k for k in nodes if effective(state, k) in ("ready", "stale", "rejected")]
    if not ready:
        print("Minden réteg jóváhagyva. A projekt kész a leszállításra.")
        return
    ready.sort(key=lambda k: (nodes[k]["layer"], k))
    layer = nodes[ready[0]]["layer"]
    print(f"Következő réteg ({layer}):")
    for k in ready:
        if nodes[k]["layer"] == layer:
            print(f"  {k}  [{MARK[effective(state, k)].strip()}]")


def cmd_approve(args):
    state = sync(args.project, load(args.project))
    n = state["nodes"].get(args.node) or die(f"nincs ilyen node: {args.node}")
    if effective(state, args.node) == "blocked":
        die(f"{args.node} zárolt, előbb a szülőket kell jóváhagyni")
    n["status"] = "approved"
    n["approved_hash"] = n["input_hash"]
    n["note"] = ""
    save(args.project, sync(args.project, state))
    print(f"Jóváhagyva: {args.node}")


def cmd_reject(args):
    state = sync(args.project, load(args.project))
    n = state["nodes"].get(args.node) or die(f"nincs ilyen node: {args.node}")
    n["status"] = "rejected"
    n["approved_hash"] = ""
    n["note"] = args.note or ""
    save(args.project, sync(args.project, state))
    print(f"Elutasítva: {args.node}. Indok: {n['note'] or 'nincs megadva'}")


def cmd_pending(args):
    state = sync(args.project, load(args.project))
    n = state["nodes"].get(args.node) or die(f"nincs ilyen node: {args.node}")
    n["status"] = "pending"
    save(args.project, state)
    print(f"Jóváhagyásra beküldve: {args.node}. Mutasd meg a felhasználónak.")


def cmd_can_spend(args):
    state = sync(args.project, load(args.project))
    save(args.project, state)
    nodes = state["nodes"]
    if args.node not in nodes:
        die(f"nincs ilyen node: {args.node}")
    bad = [d for d in nodes[args.node]["deps"] if effective(state, d) != "approved"]
    if bad:
        print(f"TILOS a generálás. Jóváhagyatlan vagy elévült előzmény: {', '.join(bad)}",
              file=sys.stderr)
        sys.exit(1)
    print(f"Mehet: {args.node}")


def cmd_spend(args):
    state = load(args.project)
    n = state["nodes"].get(args.node) or die(f"nincs ilyen node: {args.node}")
    n["spend"] += args.credits
    state["spend_log"].append({
        "ts": time.strftime("%Y-%m-%d %H:%M"), "node": args.node,
        "credits": args.credits, "note": args.note or "",
    })
    save(args.project, state)
    print(f"Rögzítve: {args.credits} kredit ({args.node})")


def cmd_estimate(args):
    state = sync(args.project, load(args.project))
    board = load_board(args.project)
    c = state["costs"]
    shots = board.get("shots", [])
    chars = len(board.get("look", {}).get("characters", []))
    img = len(shots) * c["image"]
    vid = sum(s.get("duration_s", 5) for s in shots) * c["video_per_second"]
    train = chars * c["character_train"]
    spent = sum(n["spend"] for n in state["nodes"].values())
    print(f"\n  Jelenet: {len(shots)} db, összhossz {sum(s.get('duration_s', 5) for s in shots)} mp")
    print(f"  Karaktertanítás   {train:>6} kredit")
    print(f"  Kezdőkockák       {img:>6} kredit")
    print(f"  Mozgókép          {vid:>6} kredit")
    print(f"  Alapösszeg        {train + img + vid:>6} kredit")
    print(f"  +40% újrafuttatási tartalék -> {int((train + img + vid) * 1.4):>6} kredit")
    print(f"  Eddig elköltve    {spent:>6} kredit\n")


def cmd_report(args):
    state = load(args.project)
    print(f"\n{state['name']} - költségjelentés\n")
    for e in state["spend_log"]:
        print(f"  {e['ts']}  {e['credits']:>5}  {e['node']}  {e['note']}")
    print(f"\n  Összesen: {sum(e['credits'] for e in state['spend_log'])} kredit\n")


def cmd_set_tool(args):
    state = load(args.project)
    if args.role not in state["tools"]:
        die(f"ismeretlen szerepkör: {args.role}")
    state["tools"][args.role] = args.tool
    save(args.project, state)
    print(f"{args.role} -> {args.tool}")


def cmd_check_assembly(args):
    state = sync(args.project, load(args.project))
    board = load_board(args.project)
    problems = []
    for s in board.get("shots", []):
        key = f"motion:{s['id']}"
        if effective(state, key) != "approved":
            problems.append(f"{key} nem jóváhagyott")
        for a in state["nodes"].get(key, {}).get("assets", []):
            if not os.path.exists(os.path.join(args.project, a)):
                problems.append(f"hiányzó fájl: {a}")
    if problems:
        for p in problems:
            print(f"  {p}", file=sys.stderr)
        sys.exit(1)
    print("Minden jelenet jóváhagyott és letöltött. Mehet az összefűzés.")


def main():
    ap = argparse.ArgumentParser(description="Rétegelt AI-videóprojekt állapotgépe")
    ap.add_argument("--project", default=".", help="projekt könyvtára")
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("init"); s.add_argument("name"); s.set_defaults(f=cmd_init)
    sub.add_parser("status").set_defaults(f=cmd_status)
    sub.add_parser("next").set_defaults(f=cmd_next)
    sub.add_parser("estimate").set_defaults(f=cmd_estimate)
    sub.add_parser("report").set_defaults(f=cmd_report)
    sub.add_parser("check-assembly").set_defaults(f=cmd_check_assembly)

    for name, fn in (("approve", cmd_approve), ("pending", cmd_pending),
                     ("can-spend", cmd_can_spend)):
        s = sub.add_parser(name); s.add_argument("node"); s.set_defaults(f=fn)

    s = sub.add_parser("reject"); s.add_argument("node")
    s.add_argument("--note", default=""); s.set_defaults(f=cmd_reject)

    s = sub.add_parser("spend"); s.add_argument("node")
    s.add_argument("credits", type=int); s.add_argument("--note", default="")
    s.set_defaults(f=cmd_spend)

    s = sub.add_parser("set-tool"); s.add_argument("role"); s.add_argument("tool")
    s.set_defaults(f=cmd_set_tool)

    args = ap.parse_args()
    args.f(args)


if __name__ == "__main__":
    main()
