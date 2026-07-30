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
import shutil
import sys
import time

# Windowson a konzol alapértelmezett kódlapja cp1252, amin az ő és ű betű
# UnicodeEncodeError-ral elszáll. Minden kimenetet UTF-8-ra állítunk.
for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")

STATE = "project.json"
BOARD = "storyboard.json"

# Gépszintű beállítások: előfizetés, kreditárak, MCP-eszköznevek. Ezek nem
# projektfüggők, ezért a felhasználó könyvtárában élnek, és az `init` innen
# veszi az új projekt alapértékeit.
CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".higgsfield-storyboard")
CONFIG = os.path.join(CONFIG_DIR, "config.json")
# Ügyfélprofilok: egyszer jóváhagyott stíluskód, arculat és betanított szereplők,
# amiket az adott ügyfél minden további videója újrahasznál.
UGYFELEK = os.path.join(CONFIG_DIR, "ugyfelek")

# Kiindulási kreditköltségek. NEM valós árak, csak azért vannak, hogy a
# projekt kalibrálás nélkül is elinduljon. A tényleges árak modellenként és
# felbontásonként eltérnek, ezért a `config set cost.*` paranccsal kell
# felvenni őket a saját Higgsfield-csomag alapján.
DEFAULT_COSTS = {
    "image": 5,
    "video_per_second": 10,
    "character_train": 60,
    "upscale": 20,
}

COST_KEYS = tuple(DEFAULT_COSTS)
TOOL_ROLES = ("image_gen", "image_to_video", "character_train", "upscale", "history")

# A kreditár modellenként eltér, ezért rögzítjük, melyik modellel mértünk.
# Ha a modell változik, a mérést meg kell ismételni.
MODEL_ROLES = ("image", "video", "tts")

# Marketing Studio reklámformátumok. A kulcs a jelenetlistában használt azonosító,
# az érték azt mondja meg, támogat-e zárt listás nyitóhookot.
AD_PRESETS = {
    "ugc": True,
    "tutorial": True,
    "ugc_unboxing": True,
    "hyper_motion": False,
    "product_review": True,
    "tv_spot": False,
    "wild_card": False,
    "ugc_virtual_try_on": True,
    "virtual_try_on": False,
}
# Az egyetlen formátum, ami avatár nélkül is működik.
AD_PRESETS_NO_AVATAR = ("hyper_motion",)
AD_MAX_SECONDS = 15

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


def load_config():
    c = {}
    if os.path.exists(CONFIG):
        with open(CONFIG, encoding="utf-8") as f:
            c = json.load(f)
    c.setdefault("plan", None)
    c.setdefault("monthly_credits", None)
    c.setdefault("costs", {})
    c.setdefault("tools", {})
    c.setdefault("models", {})
    c.setdefault("cli", None)          # "van" | "nincs" — felderítéssel, nem kérdezéssel
    return c


def save_config(c):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG, "w", encoding="utf-8") as f:
        json.dump(c, f, ensure_ascii=False, indent=2)


def missing_config(c):
    """A még kitöltetlen telepítési tételek listája."""
    miss = []
    if not c.get("plan"):
        miss.append("plan")
    if not c.get("monthly_credits"):
        miss.append("monthly_credits")
    miss += [f"cost.{k}" for k in COST_KEYS if c["costs"].get(k) is None]
    miss += [f"tool.{r}" for r in TOOL_ROLES if not c["tools"].get(r)]
    miss += [f"model.{r}" for r in ("image", "video") if not c["models"].get(r)]
    if not c.get("cli"):
        miss.append("cli")
    return miss


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
    # A képes poszt tételeiből nem lesz mozgókép: ott a kezdőkocka maga a
    # végtermék, nem egy közbülső lépés.
    mozgo_ids = [s["id"] for s in shots if s.get("tipus", "filmes") != "kep"]
    kep_ids = [s["id"] for s in shots if s.get("tipus") == "kep"]

    for s in shots:
        kf = f"keyframe:{s['id']}"
        mo = f"motion:{s['id']}"
        deps_kf = ["shotlist", "look"]
        if s.get("continuity_from"):
            deps_kf.append(f"keyframe:{s['continuity_from']}")
        nodes.setdefault(kf, new_node(4, deps_kf))["deps"] = deps_kf
        if s.get("tipus") == "kep":
            nodes.pop(mo, None)
        else:
            nodes.setdefault(mo, new_node(5, [kf]))["deps"] = [kf]

    # elhagyott jelenetek node-jainak takarítása
    for key in list(nodes):
        if ":" in key:
            sid = key.split(":", 1)[1]
            if sid not in shot_ids:
                del nodes[key]

    if mozgo_ids:
        nodes["assembly"]["deps"] = [f"motion:{i}" for i in mozgo_ids]
        nodes["sound"]["deps"] = ["assembly"]
        nodes["finish"]["deps"] = ["sound"] + [f"keyframe:{i}" for i in kep_ids]
    else:
        # Tisztán képes poszt: nincs mit összefűzni és nincs mit hangosítani.
        nodes.pop("assembly", None)
        nodes.pop("sound", None)
        nodes["finish"]["deps"] = [f"keyframe:{i}" for i in kep_ids]

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
            {k: s.get(k) for k in ("camera_move", "duration_s", "model", "prompt_en", "audio",
                                   "tipus", "preset", "hook_id", "setting_id", "avatar",
                                   "termekkep", "generate_audio")},
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

def cmd_config_show(args):
    c = load_config()
    miss = missing_config(c)
    print("\n  Higgsfield-storyboard telepítési adatok")
    print(f"  ({CONFIG})\n")
    print(f"  Előfizetési csomag      {c['plan'] or 'HIÁNYZIK'}")
    print(f"  Havi kredit             {c['monthly_credits'] or 'HIÁNYZIK'}")
    print(f"  Parancssori eszköz      {c.get('cli') or 'HIÁNYZIK'}"
          f"{'  (nem kötelező, MCP-vel is megy)' if c.get('cli') == 'nincs' else ''}")
    print("\n  Kreditárak")
    for k in COST_KEYS:
        v = c["costs"].get(k)
        print(f"    {k:<20} {v if v is not None else 'HIÁNYZIK'}")
    print("\n  Modellek (ezekkel mértük az árakat)")
    for r in MODEL_ROLES:
        kell = "" if r != "tts" else "  (csak narrációhoz)"
        print(f"    {r:<20} {(c['models'].get(r) or 'HIÁNYZIK') + kell}")
    print("\n  MCP-eszközök")
    for r in TOOL_ROLES:
        print(f"    {r:<20} {c['tools'].get(r) or 'HIÁNYZIK'}")
    if miss:
        print(f"\n  Hiányzik {len(miss)} adat. Derítsd fel őket (egyenleg, modellséma, "
              f"árbecslés), és vedd fel a `config set` paranccsal.\n  Amit nem tudsz "
              f"lekérdezni, azt kérdezd meg a felhasználótól — de ne tippelj helyette.\n")
    else:
        print("\n  A telepítés teljes.\n")


def cmd_config_set(args):
    c = load_config()
    key, val = args.key, args.value
    if key == "cli":
        if val not in ("van", "nincs"):
            die("a cli értéke csak 'van' vagy 'nincs' lehet")
        c["cli"] = val
    elif key == "plan":
        c["plan"] = val
    elif key == "monthly_credits":
        c["monthly_credits"] = int(val)
    elif key.startswith("cost."):
        k = key.split(".", 1)[1]
        if k not in COST_KEYS:
            die(f"ismeretlen költségtétel: {k}. Lehetséges: {', '.join(COST_KEYS)}")
        c["costs"][k] = float(val) if "." in val else int(val)
    elif key.startswith("tool."):
        r = key.split(".", 1)[1]
        if r not in TOOL_ROLES:
            die(f"ismeretlen szerepkör: {r}. Lehetséges: {', '.join(TOOL_ROLES)}")
        c["tools"][r] = val
    elif key.startswith("model."):
        r = key.split(".", 1)[1]
        if r not in MODEL_ROLES:
            die(f"ismeretlen modellszerep: {r}. Lehetséges: {', '.join(MODEL_ROLES)}")
        c["models"][r] = val
    else:
        die(f"ismeretlen kulcs: {key}. Lehetséges: plan, monthly_credits, "
            f"cost.<tétel>, tool.<szerepkör>, model.<szerep>")
    save_config(c)
    print(f"{key} -> {val}")
    miss = missing_config(c)
    if miss:
        print(f"Még hiányzik: {', '.join(miss)}")


def cmd_init(args):
    root = os.path.abspath(args.name)
    os.makedirs(root, exist_ok=True)
    for d in ("characters", "shots", "output", "delivery"):
        os.makedirs(os.path.join(root, d), exist_ok=True)
    if os.path.exists(os.path.join(root, STATE)):
        die("már létezik projekt ebben a könyvtárban")
    cfg = load_config()
    costs = dict(DEFAULT_COSTS)
    costs.update({k: v for k, v in cfg["costs"].items() if v is not None})
    state = {
        "name": args.name,
        "created": time.strftime("%Y-%m-%d %H:%M"),
        "tools": {r: cfg["tools"].get(r) for r in TOOL_ROLES},
        "models": {r: cfg["models"].get(r) for r in MODEL_ROLES},
        "costs": costs,
        "costs_calibrated": all(cfg["costs"].get(k) is not None for k in COST_KEYS),
        "plan": cfg["plan"],
        "monthly_credits": cfg["monthly_credits"],
        "nodes": {},
        "spend_log": [],
    }
    BRIEF_VAZ = """# Brief

## Mit akarunk elérni
<!-- Egy mondatban: mi az üzenet, és mit tegyen a néző. -->

## Kinek szól
<!-- Célcsoport, és amit róla tudni kell. -->

## Hol fut
<!-- Felület, képarány, hossz. Ebből következik a formátum. -->

## Kulcsszavak
<!-- Amire optimalizálunk. Kutatásból, ne fejből. A posztszöveg és a felirat ezekre épül. -->

## Referenciák
<!-- Meglévő videó, versenytárs anyag, "ilyet szeretnék". Nézd meg, ne a leírásból dolgozz. -->

## Zene és ritmus
<!-- Van-e már kiválasztott zene? Ha igen, a jelenethosszak ehhez igazodnak. -->

## Amit kerülni kell
<!-- Tiltott elemek, jogi korlátok, márkaszabályok. -->
"""
    for f, txt in (("brief.md", BRIEF_VAZ), ("treatment.md", "# Kezelés\n\n")):
        p = os.path.join(root, f)
        if not os.path.exists(p):
            open(p, "w", encoding="utf-8").write(txt)
    profil = load_ugyfel(args.ugyfel) if args.ugyfel else None
    if profil:
        state["ugyfel"] = profil.get("nev")
    board = os.path.join(root, BOARD)
    if not os.path.exists(board):
        # A profil látványa bemásolódik, nem hivatkozásként marad. Így ha az
        # ügyfél később arculatot vált, a régi munkák érintetlenek maradnak.
        json.dump({"look": (profil["look"] if profil else {}),
                   "shots": [], "assembly": {}, "sound": {}, "finish": {}},
                  open(board, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    save(root, sync(root, state))
    print(f"Projekt létrehozva: {root}")
    if profil:
        kar = profil["look"].get("characters", [])
        bet = [k for k in kar if k.get("soul_id")]
        print(f"Ügyfélprofil betöltve: {profil.get('nev')}. A látvány készen van.")
        if bet:
            print(f"  {len(bet)} betanított szereplő átvéve, újratanítás nem kell.")
        print("  A look réteg jóváhagyható, ha a felhasználó megerősíti, hogy ehhez "
              "a munkához is ez a stílus kell.")
    miss = missing_config(cfg)
    if miss:
        print(f"FIGYELEM: a telepítés hiányos ({', '.join(miss)}). "
              f"Futtasd: project.py config show")


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

    # Automata futásnál a jóváhagyott előzmény nem elég: kell a kreditplafon is.
    run = state.get("run") or {}
    if run.get("active"):
        marad = run["max_credits"] - run["spent"]
        if args.node.startswith("motion:") and not run.get("allow_motion"):
            print(f"TILOS. Automata futásban a mozgásréteg le van tiltva. Ez a drága "
                  f"lépés, itt emberi jóváhagyás kell. Állítsd le a futást "
                  f"(run stop), vagy indítsd --allow-motion kapcsolóval.", file=sys.stderr)
            sys.exit(1)
        if args.cost is None:
            print(f"TILOS. Automata futásban a becsült árat meg kell adni "
                  f"(--cost), különben a plafon nem véd. Ha az ár nem kérdezhető le "
                  f"előre — például a Marketing Studiónál —, akkor ezt a lépést "
                  f"nem szabad felügyelet nélkül futtatni.", file=sys.stderr)
            sys.exit(1)
        if args.cost > marad:
            print(f"TILOS. A lépés {args.cost} kredit, a futásból {marad} maradt "
                  f"({run['spent']}/{run['max_credits']} elköltve). A futás itt megáll.",
                  file=sys.stderr)
            sys.exit(1)
        print(f"Mehet: {args.node}  [{args.cost} kredit, marad {marad - args.cost}]")
        return
    print(f"Mehet: {args.node}")


def cmd_run_start(args):
    state = load(args.project)
    if args.max_credits <= 0:
        die("a plafon pozitív legyen")
    state["run"] = {
        "active": True,
        "max_credits": args.max_credits,
        "spent": 0,
        "allow_motion": bool(args.allow_motion),
        "started": time.strftime("%Y-%m-%d %H:%M"),
    }
    save(args.project, state)
    mozgas = "engedélyezve" if args.allow_motion else "letiltva"
    print(f"Automata futás elindítva. Plafon: {args.max_credits} kredit. "
          f"Mozgásréteg: {mozgas}.")
    havi = state.get("monthly_credits")
    if havi:
        arany = round(args.max_credits / havi * 100)
        print(f"Ez a havi keret ({havi} kredit) {arany}%-a.")
        if arany > 25:
            print("FIGYELEM: a plafon a havi keret jelentős része. "
                  "Felügyelet nélküli futáshoz ez soknak tűnik.")
    print("A futás magától megáll, ha a plafon elfogy. Leállítás: run stop")


def cmd_run_status(args):
    run = (load(args.project).get("run") or {})
    if not run.get("active"):
        print("\n  Nincs futó automata menet. A kiadások emberi jóváhagyáshoz kötöttek.\n")
        return
    print(f"\n  Automata futás — indult {run['started']}")
    print(f"  Elköltve {run['spent']} / {run['max_credits']} kredit, "
          f"marad {run['max_credits'] - run['spent']}")
    print(f"  Mozgásréteg: {'engedélyezve' if run.get('allow_motion') else 'letiltva'}\n")


def cmd_run_stop(args):
    state = load(args.project)
    run = state.get("run") or {}
    if not run.get("active"):
        print("Nem volt futó automata menet.")
        return
    run["active"] = False
    state["run"] = run
    save(args.project, state)
    print(f"Automata futás leállítva. Ebben a menetben {run['spent']} kredit ment el.")


def cmd_spend(args):
    state = load(args.project)
    n = state["nodes"].get(args.node) or die(f"nincs ilyen node: {args.node}")
    n["spend"] += args.credits
    state["spend_log"].append({
        "ts": time.strftime("%Y-%m-%d %H:%M"), "node": args.node,
        "credits": args.credits, "note": args.note or "",
    })
    run = state.get("run") or {}
    if run.get("active"):
        run["spent"] += args.credits
        state["run"] = run
    save(args.project, state)
    print(f"Rögzítve: {args.credits} kredit ({args.node})")
    if run.get("active"):
        marad = run["max_credits"] - run["spent"]
        print(f"Automata futás: {run['spent']}/{run['max_credits']} kredit, marad {marad}.")
        if marad <= 0:
            print("A plafon elfogyott, a következő lépés már nem indulhat.")


def cmd_estimate(args):
    state = sync(args.project, load(args.project))
    board = load_board(args.project)
    c = state["costs"]
    shots = board.get("shots", [])
    filmes = [s for s in shots if s.get("tipus", "filmes") == "filmes"]
    reklam = [s for s in shots if s.get("tipus") == "reklam"]
    kepek = [s for s in shots if s.get("tipus") == "kep"]
    chars = len(board.get("look", {}).get("characters", []))
    # A képes tételnél a kép maga a végtermék, mozgókép nem készül belőle.
    img = (len(filmes) + len(kepek)) * c["image"]
    vid = sum(s.get("duration_s", 5) for s in filmes) * c["video_per_second"]
    train = chars * c["character_train"]
    spent = sum(n["spend"] for n in state["nodes"].values())
    mozgohossz = sum(s.get("duration_s", 5) for s in filmes + reklam)
    reszek = [f"{len(filmes)} filmes", f"{len(reklam)} reklám", f"{len(kepek)} kép"]
    print(f"\n  Tétel: {len(shots)} db ({', '.join(reszek)}), "
          f"mozgókép összhossz {mozgohossz} mp")
    print(f"  Karaktertanítás   {train:>6} kredit")
    print(f"  Kezdőkockák       {img:>6} kredit")
    print(f"  Mozgókép          {vid:>6} kredit")
    print(f"  Alapösszeg        {train + img + vid:>6} kredit")
    teljes = int((train + img + vid) * 1.4)
    print(f"  +40% újrafuttatási tartalék -> {teljes:>6} kredit")
    print(f"  Eddig elköltve    {spent:>6} kredit")

    if reklam:
        mp = sum(s.get("duration_s", 5) for s in reklam)
        print(f"\n  Ezen felül {len(reklam)} reklámjelenet ({mp} mp), amire a platform "
              f"nem ad előzetes árat.\n  A tényleges költségük csak utólag olvasható ki; "
              f"a fenti összeg ezt NEM tartalmazza.")

    havi = state.get("monthly_credits")
    if havi:
        arany = round(teljes / havi * 100)
        print(f"\n  A(z) {state.get('plan') or '?'} csomag havi kerete {havi} kredit, "
              f"ez a projekt ennek {arany}%-a.")
        if teljes > havi:
            print("  FIGYELEM: a becslés meghaladja a havi keretet. Vagy rövidítsd a "
                  "videót, vagy előre beszéld meg az ügyféllel a kreditvásárlást.")
    if not state.get("costs_calibrated", False):
        print("\n  FIGYELEM: a kreditárak nincsenek kalibrálva, ez a becslés kitalált "
              "alapértékekkel készült. Ne mutasd meg ügyfélnek. Javítás: "
              "project.py config show")
    else:
        m = state.get("models") or {}
        print(f"  Mért modellek: kép {m.get('image') or '?'}, videó {m.get('video') or '?'} "
              f"— más modellel az ár eltér.")
    print()


def cmd_report(args):
    state = load(args.project)
    print(f"\n{state['name']} - költségjelentés\n")
    for e in state["spend_log"]:
        print(f"  {e['ts']}  {e['credits']:>5}  {e['node']}  {e['note']}")
    print(f"\n  Összesen: {sum(e['credits'] for e in state['spend_log'])} kredit\n")


def ugyfel_ut(nev):
    biztonsagos = "".join(c for c in nev.lower() if c.isalnum() or c in "-_")
    if not biztonsagos:
        die(f"értelmezhetetlen ügyfélnév: {nev!r}")
    return os.path.join(UGYFELEK, f"{biztonsagos}.json")


def load_ugyfel(nev):
    p = ugyfel_ut(nev)
    if not os.path.exists(p):
        die(f"nincs ilyen ügyfélprofil: {nev}. Lista: project.py ugyfel list")
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def cmd_ugyfel_add(args):
    """Ügyfélprofil létrehozása, lehetőleg egy már jóváhagyott projektből.

    A profilt nem kézzel írjuk: egy elkészült munka jóváhagyott látványát
    léptetjük elő újrahasznosítható profillá.
    """
    p = ugyfel_ut(args.nev)
    if os.path.exists(p) and not args.felulir:
        die(f"már létezik: {p}. Felülíráshoz: --felulir")

    if args.forras:
        board = load_board(args.forras)
        look = board.get("look", {})
        if not look:
            die(f"a(z) {args.forras} projektben nincs kitöltött look réteg")
        allapot = sync(args.forras, load(args.forras))
        if effective(allapot, "look") != "approved":
            die("a forrásprojekt look rétege nincs jóváhagyva. Ügyfélprofilba csak "
                "jóváhagyott látvány kerülhet.")
        profil = {
            "nev": args.nev,
            "keszult": time.strftime("%Y-%m-%d %H:%M"),
            "forras_projekt": os.path.abspath(args.forras),
            "look": look,
        }
    else:
        profil = {
            "nev": args.nev,
            "keszult": time.strftime("%Y-%m-%d %H:%M"),
            "forras_projekt": None,
            "look": {"brand": {}, "stilus": "", "paletta": "", "objektiv": "",
                     "characters": []},
        }

    os.makedirs(UGYFELEK, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(profil, f, ensure_ascii=False, indent=2)
    print(f"Ügyfélprofil mentve: {p}")
    kar = profil["look"].get("characters", [])
    betanitott = [k for k in kar if k.get("soul_id")]
    if betanitott:
        print(f"  {len(betanitott)} betanított szereplő átvéve — ezeket a további "
              f"munkáknál nem kell újratanítani.")
    if not args.forras:
        print("  Üres profil készült. Töltsd ki a fájlt, vagy hozd létre inkább egy "
              "jóváhagyott projektből a --forras kapcsolóval.")


def cmd_ugyfel_list(args):
    if not os.path.isdir(UGYFELEK):
        print("\n  Még nincs ügyfélprofil.\n")
        return
    fajlok = sorted(f for f in os.listdir(UGYFELEK) if f.endswith(".json"))
    if not fajlok:
        print("\n  Még nincs ügyfélprofil.\n")
        return
    print(f"\n  Ügyfélprofilok ({UGYFELEK})\n")
    for f in fajlok:
        with open(os.path.join(UGYFELEK, f), encoding="utf-8") as fp:
            pr = json.load(fp)
        kar = pr.get("look", {}).get("characters", [])
        bet = sum(1 for k in kar if k.get("soul_id"))
        print(f"    {pr.get('nev', f[:-5]):<24} {pr.get('keszult', '')}   "
              f"{len(kar)} szereplő ({bet} betanítva)")
    print()


def cmd_ugyfel_show(args):
    pr = load_ugyfel(args.nev)
    look = pr.get("look", {})
    print(f"\n  {pr.get('nev')} — készült {pr.get('keszult')}")
    if pr.get("forras_projekt"):
        print(f"  Forrás: {pr['forras_projekt']}")
    print(f"\n  Stíluskód: {look.get('stilus') or '(üres)'}")
    print(f"  Paletta:   {look.get('paletta') or '(üres)'}")
    brand = look.get("brand") or {}
    if brand:
        print(f"  Arculat:   {brand.get('nev', '?')}, "
              f"{brand.get('elsodleges_szin', '?')}, {brand.get('betutipus', '?')}")
    for k in look.get("characters", []):
        allapot = k.get("soul_id") or "NINCS BETANÍTVA"
        print(f"    - {k.get('id')}: {allapot}")
    print()


def cmd_package(args):
    """Gyártásra kész csomag legyártása, egyetlen kredit elköltése nélkül.

    Ez a generálás nélküli végigfutás kimenete: minden megvan, ami a
    generáláshoz kell, csak maga a generálás nincs meg.
    """
    state = sync(args.project, load(args.project))
    board = load_board(args.project)
    shots = board.get("shots", [])
    if not shots:
        die("üres a jelenetlista, előbb a shotlist réteget kell megcsinálni")

    look = board.get("look", {})
    c = state["costs"]
    filmes = [s for s in shots if s.get("tipus", "filmes") == "filmes"]
    reklam = [s for s in shots if s.get("tipus") == "reklam"]
    kepek = [s for s in shots if s.get("tipus") == "kep"]
    ossz = sum(s.get("duration_s", 5) for s in filmes + reklam)

    sorok = []
    add = sorok.append
    add(f"# {state['name']} — gyártási csomag\n")
    add(f"Készült: {time.strftime('%Y-%m-%d %H:%M')}. "
        f"Ez a csomag generálás nélkül készült, kreditbe nem került.\n")

    add("## Áttekintés\n")
    add(f"- Tétel: {len(shots)} db ({len(filmes)} filmes, {len(reklam)} reklám, "
        f"{len(kepek)} kép)")
    if ossz:
        add(f"- Mozgókép összhossz: {ossz} másodperc")
    if state.get("models", {}).get("image"):
        add(f"- Tervezett modellek: kép `{state['models']['image']}`, "
            f"videó `{state['models'].get('video') or '?'}`")
    add("")

    if look.get("stilus"):
        add("## Stíluskód\n")
        add("Ez minden angol promptba szó szerint bekerül, változatlanul.\n")
        add(f"> {look.get('stilus')}")
        if look.get("paletta"):
            add(f">\n> Paletta: {look.get('paletta')}")
        add("")

    if look.get("characters"):
        add("## Szereplők\n")
        for k in look["characters"]:
            allapot = "betanítva" if k.get("soul_id") else "MÉG NINCS BETANÍTVA"
            add(f"- **{k.get('id')}** — {k.get('leiras', '')} ({allapot})")
        add("")

    add("## Jelenetek\n")
    add("| # | Típus | Hossz | Gépállás | Leírás |")
    add("|---|---|---|---|---|")
    for s in shots:
        add(f"| {s.get('id')} | {s.get('tipus', 'filmes')} | {s.get('duration_s', 5)} mp "
            f"| {s.get('shot_size') or s.get('preset') or '—'} "
            f"| {(s.get('leiras') or '').replace('|', '/')} |")
    add("")

    add("## Promptok\n")
    for s in shots:
        add(f"### {s.get('id')} — {s.get('duration_s', 5)} mp\n")
        if s.get("tipus") == "reklam":
            add(f"- Formátum: `{s.get('preset')}`")
            add(f"- Termékkép: `{s.get('termekkep')}`")
            av = s.get("avatar")
            if isinstance(av, dict):
                add(f"- Avatár: {av.get('tipus', '?')} — {av.get('id') or av.get('leiras') or '?'}")
            else:
                add(f"- Avatár: {av or 'nincs megadva'}")
            if s.get("hook_id"):
                add(f"- Nyitóhook: {s['hook_id']}")
        else:
            add(f"- Kameramozgás: {s.get('camera_move', '—')}")
            if s.get("continuity_from"):
                add(f"- Folytonosság innen: {s['continuity_from']}")
        add(f"\n```\n{s.get('prompt_en', '(hiányzik)')}\n```\n")

    add("## Költségbecslés\n")
    img = (len(filmes) + len(kepek)) * c["image"]
    vid = sum(s.get("duration_s", 5) for s in filmes) * c["video_per_second"]
    train = len(look.get("characters", [])) * c["character_train"]
    alap = img + vid + train
    add(f"- Karaktertanítás: {train} kredit")
    add(f"- Kezdőkockák és képek: {img} kredit")
    add(f"- Mozgókép: {vid} kredit")
    add(f"- **Alapösszeg: {alap} kredit**, 40% újrafuttatási tartalékkal "
        f"{int(alap * 1.4)} kredit")
    if reklam:
        add(f"- Ezen felül {len(reklam)} reklámjelenet, amire a platform nem ad "
            f"előzetes árat — a költségük csak utólag derül ki.")
    if not state.get("costs_calibrated", False):
        add("\n**Figyelem:** a kreditárak nincsenek kalibrálva, ez a becslés kitalált "
            "alapértékekkel készült. Ügyfélnek ne add oda.")
    add("")

    add("## Mi kell a gyártás indításához\n")
    hianyzik = []
    if not state.get("costs_calibrated", False):
        hianyzik.append("a kreditárak kalibrálása")
    for k in look.get("characters", []):
        if not k.get("soul_id"):
            hianyzik.append(f"a(z) {k.get('id')} szereplő betanítása")
    for s in shots:
        if not s.get("prompt_en"):
            hianyzik.append(f"{s.get('id')}: hiányzik az angol prompt")
        if s.get("tipus") == "reklam" and not s.get("termekkep"):
            hianyzik.append(f"{s.get('id')}: hiányzik a termékkép")
    if hianyzik:
        for h in hianyzik:
            add(f"- {h}")
    else:
        add("Minden megvan. A gyártás indítható.")
    add("")

    ki = os.path.join(args.project, "output", "gyartasi-csomag.md")
    os.makedirs(os.path.dirname(ki), exist_ok=True)
    with open(ki, "w", encoding="utf-8") as f:
        f.write("\n".join(sorok))
    print(f"\n  Gyártási csomag: {ki}")
    print(f"  {len(shots)} tétel, becsült {int(alap * 1.4)} kredit")
    print(f"  Elköltött kredit: 0\n")


POSZT_VAZ = """# Posztszöveg — {nev}

<!-- KITÖLTENDŐ: a kísérőszöveget a modell írja meg a references/poszt-szoveg.md
     szabályai szerint. A jelölő sorokat töröld, ahogy kitöltöd. -->

## Kísérőszöveg

<!-- KITÖLTENDŐ. Az első sor önmagában is teljes üzenet legyen, a fontos
     kulcsszóval. A felületek a többit levágják. -->

## Cím

<!-- KITÖLTENDŐ, ahol értelmezhető (YouTube). Máshol törölhető ez a szakasz. -->

## Hashtagek

<!-- KITÖLTENDŐ. Néhány pontos címke: egy-két tág, néhány szűk, plusz a márkáé. -->

## AI-jelölés

Ez a tartalom mesterséges intelligenciával készült.

## Kulcsszavak, amikre optimalizáltunk

<!-- KITÖLTENDŐ a brief alapján. Ha a briefben nincs, kérdezd meg. -->
"""


def cmd_delivery(args):
    """A leszállítandó csomag összeállítása és hiányellenőrzése.

    A fájlokat összegyűjti egy helyre, a posztszöveghez vázat készít, és
    megmondja, mi hiányzik még. A szöveget nem ő írja meg — azt a modell
    írja, a references/poszt-szoveg.md szerint.
    """
    state = sync(args.project, load(args.project))
    board = load_board(args.project)
    shots = board.get("shots", [])
    finish = board.get("finish", {})
    kimenetek = finish.get("kimenetek") or []
    nev = board.get("nev") or state.get("name", "anyag")

    cel = os.path.join(args.project, "delivery")
    os.makedirs(cel, exist_ok=True)
    hianyzik, atmasolt = [], []

    # 1. mozgóképes kimenetek a kért képarányokban
    mozgo = [s for s in shots if s.get("tipus", "filmes") != "kep"]
    if mozgo:
        if not kimenetek:
            hianyzik.append("a storyboard finish.kimenetek mezője üres, "
                            "nem tudni, milyen képarányok kellenek")
        for a in kimenetek:
            fajl = f"{nev}_{a.replace(':', 'x')}.mp4"
            forras = os.path.join(args.project, "output", fajl)
            if os.path.exists(forras):
                shutil.copyfile(forras, os.path.join(cel, fajl))
                atmasolt.append(fajl)
            else:
                hianyzik.append(f"hiányzó vágás: output/{fajl} — "
                                f"futtasd az assemble.py-t {a} képaránnyal")

    # 2. képes tételek
    for s in [x for x in shots if x.get("tipus") == "kep"]:
        forras = s.get("keyframe") or f"shots/{s['id']}.png"
        p = os.path.join(args.project, forras)
        if os.path.exists(p):
            cnev = f"{s['id']}{os.path.splitext(p)[1]}"
            shutil.copyfile(p, os.path.join(cel, cnev))
            atmasolt.append(cnev)
        else:
            hianyzik.append(f"hiányzó kép: {forras} ({s['id']})")

    # 3. posztszöveg
    poszt = os.path.join(cel, "poszt.md")
    if not os.path.exists(poszt):
        with open(poszt, "w", encoding="utf-8") as f:
            f.write(POSZT_VAZ.format(nev=nev))
        hianyzik.append("a poszt.md most készült el vázként, ki kell tölteni")
    else:
        tart = open(poszt, encoding="utf-8").read()
        if "KITÖLTENDŐ" in tart:
            db = tart.count("KITÖLTENDŐ")
            hianyzik.append(f"a poszt.md még {db} kitöltetlen szakaszt tartalmaz")
        if "AI" not in tart:
            hianyzik.append("a poszt.md-ből hiányzik az AI-jelölés")

    print(f"\n  Leszállítási csomag: {cel}")
    for a in atmasolt:
        print(f"    {a}")
    if not atmasolt:
        print("    (még nincs átmásolható fájl)")
    if hianyzik:
        print(f"\n  Hiányzik {len(hianyzik)} dolog:", file=sys.stderr)
        for h in hianyzik:
            print(f"    - {h}", file=sys.stderr)
        print(file=sys.stderr)
        sys.exit(1)
    print("\n  A csomag teljes. Mehet a végső ellenőrzés "
          "(references/vegso-ellenorzes.md), utána átadható.\n")


def cmd_set_tool(args):
    state = load(args.project)
    if args.role not in state["tools"]:
        die(f"ismeretlen szerepkör: {args.role}")
    state["tools"][args.role] = args.tool
    save(args.project, state)
    print(f"{args.role} -> {args.tool}")


def cmd_check_shots(args):
    """A jelenetlista ellenőrzése generálás előtt.

    A reklámjelenetekre a Marketing Studio kemény korlátai vonatkoznak; ezeket
    olcsóbb itt kiszűrni, mint egy elutasított generálás árán.
    """
    board = load_board(args.project)
    shots = board.get("shots", [])
    hibak, megjegyzesek = [], []

    if not shots:
        die("üres a jelenetlista")

    ids = [s.get("id") for s in shots]
    for dup in {i for i in ids if ids.count(i) > 1}:
        hibak.append(f"ismétlődő jelenetazonosító: {dup}")

    for s in shots:
        sid = s.get("id", "?")
        tipus = s.get("tipus", "filmes")
        hossz = s.get("duration_s", 5)

        if tipus not in ("filmes", "reklam", "kep"):
            hibak.append(f"{sid}: ismeretlen tipus '{tipus}' (filmes, reklam vagy kep)")
            continue

        if tipus == "kep":
            if not s.get("prompt_en"):
                hibak.append(f"{sid}: hiányzik a prompt_en")
            if not s.get("aspect"):
                megjegyzesek.append(f"{sid}: nincs megadva képarány, a platform "
                                    f"alapértéke lesz")
            if s.get("camera_move") or s.get("duration_s"):
                megjegyzesek.append(f"{sid}: képnél a kameramozgás és a hossz "
                                    f"értelmezhetetlen, elhagyható")
            continue

        if tipus == "filmes":
            if hossz > 15:
                hibak.append(f"{sid}: {hossz} mp, a klipek legfeljebb 15 mp-esek, bontsd szét")
            if not s.get("prompt_en"):
                hibak.append(f"{sid}: hiányzik a prompt_en")
            continue

        # reklámjelenet
        preset = s.get("preset")
        if preset not in AD_PRESETS:
            hibak.append(f"{sid}: ismeretlen preset '{preset}'. "
                         f"Lehetséges: {', '.join(AD_PRESETS)}")
        if not s.get("termekkep"):
            hibak.append(f"{sid}: a reklámjelenethez kötelező a termekkep")
        if not 4 <= hossz <= AD_MAX_SECONDS:
            hibak.append(f"{sid}: {hossz} mp, a reklámklip 4 és {AD_MAX_SECONDS} mp között lehet")

        avatar = s.get("avatar")
        if preset in AD_PRESETS_NO_AVATAR:
            if avatar:
                megjegyzesek.append(f"{sid}: a(z) {preset} avatár nélkül is működik, "
                                    f"a megadott avatár szándékos-e?")
        elif not avatar:
            hibak.append(f"{sid}: hiányzik az avatar. Üresen hagyva minden generálás "
                         f"más arcot tesz bele")
        elif isinstance(avatar, list) and len(avatar) > 1:
            hibak.append(f"{sid}: {len(avatar)} avatár van megadva, egyszerre pontosan egy lehet")

        if s.get("hook_id") and preset in AD_PRESETS and not AD_PRESETS[preset]:
            hibak.append(f"{sid}: a(z) {preset} formátumhoz nem tartozik hook-lista, "
                         f"a hook_id-t hagyd el")
        if s.get("characters") and len(s.get("characters", [])) > 1:
            megjegyzesek.append(f"{sid}: több szereplő van felsorolva, de a reklámágon "
                                f"az arcazonosság csak egy avatárra garantált")

    for m in megjegyzesek:
        print(f"  megjegyzés: {m}")
    if hibak:
        print()
        for h in hibak:
            print(f"  HIBA: {h}", file=sys.stderr)
        sys.exit(1)
    szam = {"filmes": 0, "reklam": 0, "kep": 0}
    for s in shots:
        szam[s.get("tipus", "filmes")] += 1
    print(f"\n  A lista rendben: {len(shots)} tétel "
          f"({szam['filmes']} filmes, {szam['reklam']} reklám, {szam['kep']} kép).\n")


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

    s = sub.add_parser("init"); s.add_argument("name")
    s.add_argument("--ugyfel", default=None,
                   help="ügyfélprofil neve: a látvány készen indul")
    s.set_defaults(f=cmd_init)

    ug = sub.add_parser("ugyfel", help="ügyfélprofilok kezelése")
    ugsub = ug.add_subparsers(dest="ugyfelcmd", required=True)
    s = ugsub.add_parser("add", help="profil létrehozása, lehetőleg kész projektből")
    s.add_argument("nev")
    s.add_argument("--forras", default=None, help="jóváhagyott projekt könyvtára")
    s.add_argument("--felulir", action="store_true")
    s.set_defaults(f=cmd_ugyfel_add)
    ugsub.add_parser("list").set_defaults(f=cmd_ugyfel_list)
    s = ugsub.add_parser("show"); s.add_argument("nev"); s.set_defaults(f=cmd_ugyfel_show)
    sub.add_parser("status").set_defaults(f=cmd_status)
    sub.add_parser("next").set_defaults(f=cmd_next)
    sub.add_parser("estimate").set_defaults(f=cmd_estimate)
    sub.add_parser("report").set_defaults(f=cmd_report)
    sub.add_parser("check-shots").set_defaults(f=cmd_check_shots)
    sub.add_parser("check-assembly").set_defaults(f=cmd_check_assembly)

    sub.add_parser("package", help="gyártási csomag generálás nélkül").set_defaults(f=cmd_package)
    sub.add_parser("delivery", help="leszállítási csomag összeállítása").set_defaults(f=cmd_delivery)

    for name, fn in (("approve", cmd_approve), ("pending", cmd_pending)):
        s = sub.add_parser(name); s.add_argument("node"); s.set_defaults(f=fn)

    s = sub.add_parser("can-spend"); s.add_argument("node")
    s.add_argument("--cost", type=int, default=None,
                   help="a lépés becsült ára; automata futásban kötelező")
    s.set_defaults(f=cmd_can_spend)

    run = sub.add_parser("run", help="automata futás kreditplafonnal")
    runsub = run.add_subparsers(dest="runcmd", required=True)
    s = runsub.add_parser("start")
    s.add_argument("--max-credits", type=int, required=True, help="kreditplafon a futásra")
    s.add_argument("--allow-motion", action="store_true",
                   help="a drága mozgásréteg engedélyezése (alapból tiltott)")
    s.set_defaults(f=cmd_run_start)
    runsub.add_parser("status").set_defaults(f=cmd_run_status)
    runsub.add_parser("stop").set_defaults(f=cmd_run_stop)

    s = sub.add_parser("reject"); s.add_argument("node")
    s.add_argument("--note", default=""); s.set_defaults(f=cmd_reject)

    s = sub.add_parser("spend"); s.add_argument("node")
    s.add_argument("credits", type=int); s.add_argument("--note", default="")
    s.set_defaults(f=cmd_spend)

    s = sub.add_parser("set-tool"); s.add_argument("role"); s.add_argument("tool")
    s.set_defaults(f=cmd_set_tool)

    cfg = sub.add_parser("config", help="gépszintű telepítési adatok")
    cfgsub = cfg.add_subparsers(dest="cfgcmd", required=True)
    cfgsub.add_parser("show", help="mi van beállítva, mi hiányzik").set_defaults(f=cmd_config_show)
    s = cfgsub.add_parser("set", help="plan | monthly_credits | cost.<tétel> | tool.<szerepkör>")
    s.add_argument("key"); s.add_argument("value"); s.set_defaults(f=cmd_config_set)

    args = ap.parse_args()
    args.f(args)


if __name__ == "__main__":
    main()
