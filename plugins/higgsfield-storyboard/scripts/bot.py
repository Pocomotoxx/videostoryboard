#!/usr/bin/env python3
"""Telefonos jóváhagyás Telegramon keresztül.

Ez a bot **nem generál semmit**, és nem költ kreditet. Egyetlen dolga, hogy a
jóváhagyásra váró anyagot kiküldje a telefonodra, és a döntésedet visszaírja a
projektbe. A generálás marad a gépen, a szokásos kapun és plafonon keresztül.

Ezért nincs szüksége Higgsfield-kulcsra, és ezért nem tud kárt okozni: a
legrosszabb, ami történhet, hogy elfogadsz vagy visszadobsz valamit.

Függőség nélküli: csak a Python szabványos könyvtárát használja, hosszú
lekérdezéssel. Nincs webszerver, nincs nyilvános cím, nincs tanúsítvány.

Beállítás:
    export TG_TOKEN="a BotFathertől kapott token"
    export TG_OWNER="a saját Telegram-azonosítód"

Ellenőrzés indítás előtt:
    python3 bot.py --project . --onteszt

Indítás:
    python3 bot.py --project .
"""

import argparse
import json
import mimetypes
import os
import subprocess
import sys
import time
import urllib.parse
import urllib.request
import uuid

for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_PY = os.path.join(HERE, "project.py")
API = "https://api.telegram.org/bot{}/{}"

SUGO = (
    "Amit tudok:\n"
    "/varo — jóváhagyásra váró anyagok kiküldése\n"
    "/allapot — hol tart a projekt\n"
    "/koltseg — eddig elköltött kredit\n"
    "/megse — a folyamatban lévő visszadobás megszakítása\n\n"
    "Generálni nem tudok, azt a gépen kell elindítani."
)


def form_ertek(v):
    """A Telegram a szerkezetes mezőket JSON-ként várja, nem Python-alakban."""
    return json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else str(v)


def multipart(params, mezonev, path):
    """multipart/form-data test összeállítása egy fájlfeltöltéshez."""
    bound = uuid.uuid4().hex
    body = b""
    for k, v in params.items():
        body += (f"--{bound}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n"
                 f"{form_ertek(v)}\r\n").encode("utf-8")
    fname = os.path.basename(path)
    ctype = mimetypes.guess_type(fname)[0] or "application/octet-stream"
    body += (f"--{bound}\r\nContent-Disposition: form-data; name=\"{mezonev}\"; "
             f"filename=\"{fname}\"\r\nContent-Type: {ctype}\r\n\r\n").encode("utf-8")
    with open(path, "rb") as f:
        body += f.read()
    body += f"\r\n--{bound}--\r\n".encode("utf-8")
    return bound, body


def tg(token, method, _fajl=None, _mezo="document", **params):
    if _fajl:
        bound, body = multipart(params, _mezo, _fajl)
        req = urllib.request.Request(API.format(token, method), data=body)
        req.add_header("Content-Type", f"multipart/form-data; boundary={bound}")
    else:
        data = urllib.parse.urlencode(
            {k: form_ertek(v) for k, v in params.items()}).encode("utf-8")
        req = urllib.request.Request(API.format(token, method), data=data)
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            return json.loads(r.read())
    except Exception as e:
        print(f"telegram hiba ({method}): {e}", file=sys.stderr)
        return {"ok": False}


def pj(project, *args):
    """project.py hívása. A bot csak olvas és jóváhagy, generálni nem tud."""
    r = subprocess.run([sys.executable, PROJECT_PY, "--project", project, *args],
                       capture_output=True, text=True, encoding="utf-8")
    return ((r.stdout or "") + (r.stderr or "")).strip() or "(nincs kimenet)"


def nodes(project, prefix="", state=""):
    a = ["--project", project, "list"]
    if prefix:
        a += ["--prefix", prefix]
    if state:
        a += ["--state", state]
    r = subprocess.run([sys.executable, PROJECT_PY, *a],
                       capture_output=True, text=True, encoding="utf-8")
    try:
        return json.loads(r.stdout)
    except Exception:
        return []


def gombok(node):
    return {"inline_keyboard": [[
        {"text": "Elfogadom", "callback_data": f"ok|{node}"},
        {"text": "Visszadobom", "callback_data": f"no|{node}"},
    ]]}


class Bot:
    def __init__(self, token, owner, project):
        self.t = token
        self.owner = str(owner)
        self.p = project
        self.varakozo_indok = None

    # ---------------------------------------------------------------- küldés

    def uzen(self, szoveg, **kw):
        tg(self.t, "sendMessage", chat_id=self.owner, text=szoveg[:4000], **kw)

    def kuld_anyag(self, node, utvonal, felirat):
        """Fájlként küldjük, nem képként: a tömörítés pont az apró részleteket
        mossa el, amiket ellenőrizni kellene — ujjak, arc, háttérbe rajzolt betűk."""
        if not os.path.exists(utvonal):
            self.uzen(f"{node}: hiányzik a fájl ({utvonal})", reply_markup=gombok(node))
            return
        tg(self.t, "sendDocument", _fajl=utvonal, _mezo="document",
           chat_id=self.owner, caption=felirat[:1000], reply_markup=gombok(node))

    # -------------------------------------------------------------- parancsok

    def c_allapot(self):
        self.uzen(pj(self.p, "status"))

    def c_koltseg(self):
        self.uzen(pj(self.p, "report"))

    def c_megse(self):
        if self.varakozo_indok:
            n, self.varakozo_indok = self.varakozo_indok, None
            self.uzen(f"Rendben, a visszadobás elmarad: {n}")
        else:
            self.uzen("Nincs folyamatban visszadobás.")

    def c_varo(self):
        varo = [n for n in nodes(self.p, "", "pending")]
        if not varo:
            self.uzen("Most nincs jóváhagyásra váró anyag.")
            return
        self.uzen(f"{len(varo)} tétel vár jóváhagyásra.")
        for n in varo:
            felirat = n["node"]
            if n.get("request_stale"):
                felirat += "\nFIGYELEM: a jelenet a beküldés óta megváltozott, " \
                           "ez az eredmény egy korábbi változathoz tartozik."
            if n["note"]:
                felirat += f"\n{n['note']}"
            if n["assets"]:
                self.kuld_anyag(n["node"], os.path.join(self.p, n["assets"][0]), felirat)
            else:
                self.uzen(felirat, reply_markup=gombok(n["node"]))

    # ------------------------------------------------------------------ hurok

    def on_text(self, txt):
        t = txt.strip()
        parancs = t.split()[0].lower().split("@")[0] if t else ""
        tabla = {"/varo": self.c_varo, "/allapot": self.c_allapot,
                 "/koltseg": self.c_koltseg, "/megse": self.c_megse}

        if self.varakozo_indok:
            # Parancsot ne nyeljünk el indokként: a felhasználó meggondolhatta magát.
            if parancs in tabla:
                tabla[parancs]()
                return
            node, self.varakozo_indok = self.varakozo_indok, None
            self.uzen(pj(self.p, "reject", node, "--note", t))
            return

        (tabla.get(parancs) or (lambda: self.uzen(SUGO)))()

    def on_callback(self, cq):
        tg(self.t, "answerCallbackQuery", callback_query_id=cq["id"])
        muvelet, node = cq["data"].split("|", 1)
        if muvelet == "ok":
            self.uzen(pj(self.p, "approve", node))
        else:
            self.varakozo_indok = node
            self.uzen(f"Mi a baj vele? Írd le egy mondatban. ({node})\n"
                      f"Ha meggondoltad magad: /megse")

    def kie(self, u):
        """A küldő azonosítója — gombnyomásnál is a megnyomó számít, nem a chat."""
        if "callback_query" in u:
            return str(u["callback_query"].get("from", {}).get("id", ""))
        return str(u.get("message", {}).get("from", {}).get("id", ""))

    def loop(self):
        self.uzen(f"Elindultam.\nProjekt: "
                  f"{os.path.basename(os.path.abspath(self.p))}\n\n{SUGO}")
        offset, hiba = 0, 0
        while True:
            r = tg(self.t, "getUpdates", offset=offset, timeout=50)
            if not r.get("ok"):
                hiba = min(hiba + 1, 6)
                time.sleep(min(2 ** hiba, 60))
                continue
            hiba = 0
            for u in r.get("result", []):
                offset = u["update_id"] + 1
                if self.kie(u) != self.owner:
                    continue          # más feladótól érkező üzenet: válasz nélkül eldobjuk
                try:
                    if "callback_query" in u:
                        self.on_callback(u["callback_query"])
                    elif "text" in u.get("message", {}):
                        self.on_text(u["message"]["text"])
                except Exception as e:
                    self.uzen(f"Hiba: {e}")


def onteszt(project, token, owner):
    """Indítás előtti ellenőrzés, a Telegram megszólítása nélkül."""
    baj = []
    print("\n  Ellenőrzés\n")

    print(f"    projekt          {project}")
    if not os.path.exists(os.path.join(project, "project.json")):
        baj.append(f"nincs projekt itt: {project}")

    print(f"    project.py       {PROJECT_PY}")
    if not os.path.exists(PROJECT_PY):
        baj.append("nincs meg a project.py a script mellett")

    print(f"    TG_TOKEN         {'megvan' if token else 'HIÁNYZIK'}")
    print(f"    TG_OWNER         {owner or 'HIÁNYZIK'}")
    if not token:
        baj.append("nincs TG_TOKEN")
    if not owner:
        baj.append("nincs TG_OWNER")

    # A gombok szerkezetes mezője JSON-ként kell menjen, különben a Telegram
    # eldobja, és a jóváhagyó gombok nem jelennek meg.
    proba = form_ertek(gombok("keyframe:s001"))
    try:
        json.loads(proba)
        print("    gombok           rendben")
    except Exception as e:
        baj.append(f"a gombok szerializálása hibás: {e}")

    if not baj and os.path.exists(os.path.join(project, "project.json")):
        varo = nodes(project, "", "pending")
        print(f"    jóváhagyásra vár {len(varo)} tétel")

    print()
    for b in baj:
        print(f"    HIBA: {b}", file=sys.stderr)
    if baj:
        sys.exit(1)
    print("  Minden rendben, indítható.\n")


def main():
    ap = argparse.ArgumentParser(description="Telefonos jóváhagyás Telegramon")
    ap.add_argument("--project", default=".")
    ap.add_argument("--onteszt", action="store_true",
                    help="beállítások ellenőrzése indítás nélkül")
    a = ap.parse_args()

    token = os.getenv("TG_TOKEN", "")
    owner = os.getenv("TG_OWNER", "")

    if a.onteszt:
        onteszt(a.project, token, owner)
        return

    if not token:
        sys.exit("nincs TG_TOKEN")
    if not owner:
        sys.exit("nincs TG_OWNER")
    if not os.path.exists(os.path.join(a.project, "project.json")):
        sys.exit(f"nincs projekt itt: {a.project}")

    Bot(token, owner, a.project).loop()


if __name__ == "__main__":
    main()
