import sys
import os
import math
import random
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QFrame, QStackedWidget,
    QScrollArea, QGridLayout, QSizePolicy, QGraphicsDropShadowEffect
)
from PyQt6.QtGui import (
    QPixmap, QColor, QPainter, QPen, QBrush,
    QLinearGradient, QRadialGradient, QFont
)
from PyQt6.QtCore import Qt, QTimer, QRectF

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Palette (identique au login) ──────────────────────────────────────────────
C_BG       = "#060809"
C_SIDEBAR  = "#080d12"
C_CARD     = "#0c1520"
C_CARD2    = "#0e1a28"
C_ACCENT   = "#2a9fd6"
C_ACCENT2  = "#50c8f0"
C_TEXT     = "#c8e0f0"
C_DIM      = "#2a5570"
C_BORDER   = "#112030"
C_RED      = "#d63a3a"
C_GREEN    = "#3ad67a"
C_YELLOW   = "#d6a83a"

FONT       = "Courier New"


# ══════════════════════════════════════════════════════════════════════════════
#  Background Matrix — identique au login
# ══════════════════════════════════════════════════════════════════════════════
class MatrixBackground(QWidget):
    CHARS = "01アイウエオカキクケコサシスセソタチツテトナニヌネノ"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.columns = []
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(80)

    def _init_columns(self):
        cols = max(1, self.width() // 22)
        self.columns = [
            {"x": i * 22 + random.randint(0, 8),
             "y": random.randint(-800, 0),
             "speed": random.uniform(1.0, 2.8),
             "length": random.randint(5, 14),
             "chars": [random.choice(self.CHARS) for _ in range(20)],
             "alpha": random.uniform(0.02, 0.07)}
            for i in range(cols)
        ]

    def resizeEvent(self, e):
        self._init_columns(); super().resizeEvent(e)

    def showEvent(self, e):
        self._init_columns(); super().showEvent(e)

    def _tick(self):
        for col in self.columns:
            col["y"] += col["speed"]
            if col["y"] > self.height() + col["length"] * 18:
                col["y"] = random.randint(-300, -20)
                col["alpha"] = random.uniform(0.02, 0.07)
            if random.random() < 0.06:
                col["chars"][random.randint(0, len(col["chars"]) - 1)] = random.choice(self.CHARS)
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        g = QLinearGradient(0, 0, 0, self.height())
        g.setColorAt(0, QColor("#050708"))
        g.setColorAt(1, QColor("#080d11"))
        p.fillRect(self.rect(), g)
        p.setFont(QFont(FONT, 8))
        for col in self.columns:
            for i in range(col["length"]):
                y = col["y"] - i * 16
                if y < -16 or y > self.height():
                    continue
                b = 1.0 if i == 0 else max(0.08, 1.0 - i / col["length"])
                a = min(255, int(col["alpha"] * b * 255 * 3))
                color = QColor(180, 230, 255, min(255, a * 3)) if i == 0 else QColor(42, 159, 214, a)
                p.setPen(QPen(color))
                p.drawText(int(col["x"]), int(y), col["chars"][i % len(col["chars"])])
        p.end()


# ══════════════════════════════════════════════════════════════════════════════
#  Carte animée (même bordure tournante que le login)
# ══════════════════════════════════════════════════════════════════════════════
class GlowCard(QWidget):
    def __init__(self, w=260, h=110, parent=None):
        super().__init__(parent)
        self.setFixedSize(w, h)
        self._angle = random.uniform(0, 360)
        t = QTimer(self); t.timeout.connect(self._tick); t.start(30)

    def _tick(self):
        self._angle = (self._angle + 0.8) % 360
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        r = QRectF(1, 1, self.width() - 2, self.height() - 2)
        # Fond dégradé carte
        g = QLinearGradient(0, 0, 0, self.height())
        g.setColorAt(0, QColor(C_CARD2))
        g.setColorAt(1, QColor(C_CARD))
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QBrush(g))
        p.drawRoundedRect(r, 6, 6)
        # Bordure lumineuse tournante
        rad = math.radians(self._angle)
        cx = self.width() / 2 + math.cos(rad) * self.width() * 0.7
        cy = self.height() / 2 + math.sin(rad) * self.height() * 0.7
        glow = QRadialGradient(cx, cy, self.width())
        glow.setColorAt(0.0, QColor(42, 159, 214, 80))
        glow.setColorAt(0.6, QColor(42, 159, 214, 15))
        glow.setColorAt(1.0, QColor(42, 159, 214, 0))
        p.setPen(QPen(QBrush(glow), 1.2))
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawRoundedRect(r, 6, 6)
        # Bordure fixe
        p.setPen(QPen(QColor(C_BORDER), 1))
        p.drawRoundedRect(r.adjusted(1, 1, -1, -1), 5.5, 5.5)
        p.end()


# ══════════════════════════════════════════════════════════════════════════════
#  Helpers UI
# ══════════════════════════════════════════════════════════════════════════════
def lbl(text, size=12, color=C_TEXT, bold=False, spacing=0):
    l = QLabel(text)
    weight = "bold" if bold else "normal"
    l.setStyleSheet(f"""
        color: {color};
        font-family: '{FONT}';
        font-size: {size}px;
        font-weight: {weight};
        letter-spacing: {spacing}px;
        background: transparent;
    """)
    return l

def h_sep():
    f = QFrame(); f.setFrameShape(QFrame.Shape.HLine)
    f.setStyleSheet(f"color: {C_BORDER}; margin: 0;"); return f

def field(placeholder, password=False):
    f = QLineEdit()
    f.setPlaceholderText(placeholder)
    f.setFixedHeight(42)
    if password:
        f.setEchoMode(QLineEdit.EchoMode.Password)
    f.setStyleSheet(f"""
        QLineEdit {{
            background-color: #07111a;
            border: 1px solid #152535;
            border-radius: 3px;
            color: {C_TEXT};
            padding: 0 14px;
            font-family: '{FONT}';
            font-size: 12px;
        }}
        QLineEdit:focus {{
            border: 1px solid {C_ACCENT};
            background-color: #091520;
        }}
        QLineEdit::placeholder {{ color: #2a4055; }}
    """)
    return f

def btn(text, color=C_ACCENT, w=None, h=40):
    b = QPushButton(text)
    b.setFixedHeight(h)
    if w: b.setFixedWidth(w)
    b.setCursor(Qt.CursorShape.PointingHandCursor)
    b.setStyleSheet(f"""
        QPushButton {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {color}55, stop:1 {color}22);
            color: {color};
            border: 1px solid {color}88;
            border-radius: 3px;
            font-family: '{FONT}';
            font-size: 11px;
            font-weight: bold;
            letter-spacing: 3px;
            padding: 0 16px;
        }}
        QPushButton:hover {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {color}99, stop:1 {color}44);
            border-color: {color};
        }}
        QPushButton:pressed {{ background: {color}66; }}
    """)
    return b

# Label de section — gros titre blanc comme "Connexion" dans le login
def lbl_title(text):
    l = QLabel(text)
    l.setStyleSheet(f"""
        color: {C_TEXT};
        font-family: '{FONT}';
        font-size: 20px;
        font-weight: bold;
        letter-spacing: 2px;
        background: transparent;
    """)
    return l

# Sous-titre cyan — comme "ACCÈS SÉCURISÉ" dans le login
def lbl_sub(text):
    l = QLabel(text)
    l.setStyleSheet(f"""
        color: {C_ACCENT};
        font-family: '{FONT}';
        font-size: 11px;
        font-weight: bold;
        letter-spacing: 5px;
        background: transparent;
    """)
    return l

# Label de champ — comme "NOM D'UTILISATEUR" dans le login
def lbl_field(text):
    l = QLabel(text)
    l.setStyleSheet(f"""
        color: {C_ACCENT};
        font-family: '{FONT}';
        font-size: 11px;
        font-weight: bold;
        letter-spacing: 3px;
        background: transparent;
    """)
    return l

def scroll_wrap(inner):
    s = QScrollArea()
    s.setWidget(inner); s.setWidgetResizable(True)
    s.setStyleSheet("""
        QScrollArea { background: transparent; border: none; }
        QScrollBar:vertical { background: #080d12; width: 5px; border-radius: 2px; }
        QScrollBar::handle:vertical { background: #1a3040; border-radius: 2px; min-height: 20px; }
        QScrollBar::handle:vertical:hover { background: #2a9fd6; }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
    """)
    return s


# ══════════════════════════════════════════════════════════════════════════════
#  Carte de statistique
# ══════════════════════════════════════════════════════════════════════════════
class StatCard(GlowCard):
    def __init__(self, title, value, color=C_ACCENT, parent=None):
        super().__init__(260, 110, parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 14, 20, 14)
        layout.setSpacing(6)
        layout.addWidget(lbl(title.upper(), size=9, color=C_ACCENT, bold=True, spacing=3))
        layout.addWidget(lbl(value, size=24, color=C_TEXT, bold=True))


# ══════════════════════════════════════════════════════════════════════════════
#  Bouton sidebar
# ══════════════════════════════════════════════════════════════════════════════
class SidebarBtn(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.setFixedHeight(48)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setCheckable(True)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 16, 0)
        layout.setSpacing(0)

        # Barre indicatrice gauche
        self._bar = QFrame()
        self._bar.setFixedSize(3, 22)
        self._bar.setStyleSheet(f"background: {C_ACCENT}; border-radius: 2px;")
        self._bar.hide()

        self._lbl = QLabel(text)
        self._lbl.setStyleSheet(f"color: {C_DIM}; font-family: '{FONT}'; font-size: 11px; letter-spacing: 1px; background: transparent;")

        layout.addWidget(self._bar)
        layout.addSpacing(14)
        layout.addWidget(self._lbl)
        layout.addStretch()

        self._set_style(False)
        self.toggled.connect(self._set_style)

    def _set_style(self, active):
        if active:
            self._bar.show()
            self._lbl.setStyleSheet(f"color: {C_ACCENT2}; font-family: '{FONT}'; font-size: 13px; font-weight: bold; letter-spacing: 1px; background: transparent;")
            self.setStyleSheet(f"QPushButton {{ background: {C_ACCENT}18; border: none; }}")
        else:
            self._bar.hide()
            self._lbl.setStyleSheet(f"color: {C_DIM}; font-family: '{FONT}'; font-size: 13px; letter-spacing: 1px; background: transparent;")
            self.setStyleSheet("QPushButton { background: transparent; border: none; } QPushButton:hover { background: #0d1e2a; }")


# ══════════════════════════════════════════════════════════════════════════════
#  Pages
# ══════════════════════════════════════════════════════════════════════════════

# ── Tableau de bord ────────────────────────────────────────────────────────
def page_dashboard(username):
    outer = QWidget(); outer.setStyleSheet("background: transparent;")
    lay = QVBoxLayout(outer); lay.setContentsMargins(36, 28, 36, 28); lay.setSpacing(20)

    # En-tête
    hdr = QHBoxLayout()
    col = QVBoxLayout(); col.setSpacing(4)
    col.addWidget(lbl_sub("TABLEAU DE BORD"))
    col.addWidget(lbl_title(f"Bienvenue, {username}"))
    hdr.addLayout(col); hdr.addStretch()
    hdr.addWidget(lbl("BEATS BANK  //  v2.0.0", size=9, color=C_DIM))
    lay.addLayout(hdr)
    lay.addWidget(h_sep())

    # Stat cards
    grid = QGridLayout(); grid.setSpacing(12)
    stats = [
        ("Solde Net",       "124 580 $", C_ACCENT),
        ("Clients",         "42",         C_GREEN),
        ("Cartes Actives",  "87",         C_YELLOW),
        ("Montant Investi", "38 200 $",   C_ACCENT2),
    ]
    for i, (t, v, c) in enumerate(stats):
        grid.addWidget(StatCard(t, v, c), 0, i)
    lay.addLayout(grid)

    # Activité récente
    lay.addWidget(lbl_field("ACTIVITE RECENTE"))
    act_w = QWidget()
    act_w.setStyleSheet(f"background: {C_CARD}; border: 1px solid {C_BORDER}; border-radius: 6px;")
    act_l = QVBoxLayout(act_w); act_l.setContentsMargins(20, 16, 20, 16); act_l.setSpacing(12)

    rows = [
        ("Depot — Marie Tremblay",    "+2 500 $",  C_GREEN),
        ("Retrait — Jean Gagnon",     "-800 $",    C_RED),
        ("Virement — Sophie Lavoie",  "-1 200 $",  C_YELLOW),
        ("Depot — Marc Beaulieu",     "+5 000 $",  C_GREEN),
    ]
    for idx, (desc, amount, color) in enumerate(rows):
        r = QHBoxLayout()
        r.addWidget(lbl(desc, size=12))
        r.addStretch()
        r.addWidget(lbl(amount, size=12, color=color, bold=True))
        act_l.addLayout(r)
        if idx < len(rows) - 1:
            act_l.addWidget(h_sep())

    lay.addWidget(act_w)
    lay.addStretch()
    return scroll_wrap(outer)


# ── Clients ────────────────────────────────────────────────────────────────
def page_clients():
    outer = QWidget(); outer.setStyleSheet("background: transparent;")
    lay = QVBoxLayout(outer); lay.setContentsMargins(36, 28, 36, 28); lay.setSpacing(18)

    hdr = QHBoxLayout()
    col = QVBoxLayout(); col.setSpacing(4)
    col.addWidget(lbl_sub("GESTION"))
    col.addWidget(lbl_title("Clients"))
    hdr.addLayout(col); hdr.addStretch()
    hdr.addWidget(btn("NOUVEAU CLIENT", C_GREEN))
    lay.addLayout(hdr)
    lay.addWidget(h_sep())

    lay.addWidget(field("Rechercher un client..."))

    th = QWidget(); th.setFixedHeight(36)
    th.setStyleSheet(f"background: {C_BORDER}; border-radius: 3px;")
    thl = QHBoxLayout(th); thl.setContentsMargins(16, 0, 16, 0)
    for col_name in ["NOM", "PRENOM", "AGE", "NB CARTES", ""]:
        thl.addWidget(lbl(col_name, size=10, color=C_ACCENT, bold=True, spacing=2))
    lay.addWidget(th)

    clients = [
        ("Tremblay", "Marie",   "34", "2"),
        ("Gagnon",   "Jean",    "52", "1"),
        ("Lavoie",   "Sophie",  "28", "3"),
        ("Beaulieu", "Marc",    "45", "1"),
        ("Roy",      "Isabelle","31", "2"),
    ]
    for nom, prenom, age, cartes in clients:
        rw = QWidget(); rw.setFixedHeight(48)
        rw.setStyleSheet(f"background: {C_CARD}; border: 1px solid {C_BORDER}; border-radius: 3px;")
        rl = QHBoxLayout(rw); rl.setContentsMargins(16, 0, 16, 0); rl.setSpacing(0)
        for val in [nom, prenom, age, cartes]:
            rl.addWidget(lbl(val, size=12))
        rl.addStretch()
        b1 = btn("MODIFIER", C_ACCENT, w=110, h=32)
        b2 = btn("RETIRER",  C_RED,    w=100, h=32)
        rl.addWidget(b1); rl.addSpacing(8); rl.addWidget(b2)
        lay.addWidget(rw)

    lay.addStretch()
    return scroll_wrap(outer)


# ── Cartes ─────────────────────────────────────────────────────────────────
def page_cartes():
    outer = QWidget(); outer.setStyleSheet("background: transparent;")
    lay = QVBoxLayout(outer); lay.setContentsMargins(36, 28, 36, 28); lay.setSpacing(18)

    hdr = QHBoxLayout()
    col = QVBoxLayout(); col.setSpacing(4)
    col.addWidget(lbl_sub("GESTION"))
    col.addWidget(lbl_title("Cartes"))
    hdr.addLayout(col); hdr.addStretch()
    hdr.addWidget(btn("NOUVELLE CARTE", C_GREEN))
    lay.addLayout(hdr)
    lay.addWidget(h_sep())

    cartes = [
        ("**** **** **** 4521", "Marie Tremblay",  "12/26", "4 200 $",  C_ACCENT),
        ("**** **** **** 8830", "Jean Gagnon",     "08/25", "1 100 $",  C_GREEN),
        ("**** **** **** 3317", "Sophie Lavoie",   "03/27", "7 850 $",  C_YELLOW),
        ("**** **** **** 9902", "Marc Beaulieu",   "11/24", "320 $",    C_RED),
        ("**** **** **** 1155", "Marie Tremblay",  "06/28", "12 400 $", C_ACCENT2),
    ]
    for numero, client, exp, solde, color in cartes:
        cw = QWidget(); cw.setFixedHeight(72)
        cw.setStyleSheet(f"""
            background: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 {C_CARD2}, stop:1 {C_CARD});
            border: 1px solid {color}44;
            border-radius: 6px;
        """)
        cl = QHBoxLayout(cw); cl.setContentsMargins(20, 0, 20, 0); cl.setSpacing(24)
        cl.addWidget(lbl(numero,       size=13, color=color, bold=True))
        cl.addWidget(lbl(client,       size=12))
        cl.addWidget(lbl(f"EXP: {exp}", size=11, color=C_DIM))
        cl.addStretch()
        cl.addWidget(lbl(solde, size=15, color=color, bold=True))
        cl.addSpacing(16)
        cl.addWidget(btn("SUPPRIMER", C_RED, h=32))
        lay.addWidget(cw)

    lay.addStretch()
    return scroll_wrap(outer)


# ── Transactions ───────────────────────────────────────────────────────────
def page_transactions():
    outer = QWidget(); outer.setStyleSheet("background: transparent;")
    lay = QVBoxLayout(outer); lay.setContentsMargins(36, 28, 36, 28); lay.setSpacing(18)

    hdr = QVBoxLayout(); hdr.setSpacing(4)
    hdr.addWidget(lbl_sub("VIREMENTS"))
    hdr.addWidget(lbl_title("Transactions"))
    lay.addLayout(hdr)
    lay.addWidget(h_sep())

    fw = QWidget()
    fw.setStyleSheet(f"background: {C_CARD}; border: 1px solid {C_BORDER}; border-radius: 6px;")
    fl = QVBoxLayout(fw); fl.setContentsMargins(24, 18, 24, 18); fl.setSpacing(12)
    fl.addWidget(lbl_field("NOUVEAU VIREMENT"))

    r1 = QHBoxLayout(); r1.setSpacing(12)
    r1.addWidget(field("Carte source  (ex: **** 4521)"))
    r1.addWidget(field("Carte destinataire"))
    fl.addLayout(r1)

    r2 = QHBoxLayout(); r2.setSpacing(12)
    r2.addWidget(field("Montant ($)"))
    r2.addWidget(field("Description (optionnel)"))
    fl.addLayout(r2)

    brow = QHBoxLayout()
    brow.addWidget(btn("EFFECTUER LE VIREMENT", C_ACCENT, h=42))
    brow.addStretch()
    fl.addLayout(brow)
    lay.addWidget(fw)

    lay.addWidget(lbl_field("HISTORIQUE"))
    history = [
        ("2025-04-15", "Depot",    "Marie Tremblay",  "Jean Gagnon",   "+2 500 $",  C_GREEN),
        ("2025-04-14", "Retrait",  "Jean Gagnon",     "—",             "-800 $",    C_RED),
        ("2025-04-13", "Virement", "Sophie Lavoie",   "Marc Beaulieu", "-1 200 $",  C_YELLOW),
        ("2025-04-12", "Depot",    "Marc Beaulieu",   "—",             "+5 000 $",  C_GREEN),
    ]
    for date, typ, src, dst, amount, color in history:
        rw = QWidget(); rw.setFixedHeight(44)
        rw.setStyleSheet(f"background: {C_CARD}; border: 1px solid {C_BORDER}; border-radius: 3px;")
        rl = QHBoxLayout(rw); rl.setContentsMargins(16, 0, 16, 0); rl.setSpacing(0)
        for txt, clr, w in [(date, C_DIM, 95), (typ, C_ACCENT, 85), (src, C_TEXT, 155), (dst, C_DIM, 155)]:
            l2 = lbl(txt, size=11, color=clr); l2.setFixedWidth(w)
            rl.addWidget(l2)
        rl.addStretch()
        rl.addWidget(lbl(amount, size=12, color=color, bold=True))
        lay.addWidget(rw)

    lay.addStretch()
    return scroll_wrap(outer)


# ── Investissements ────────────────────────────────────────────────────────
def page_investissements():
    outer = QWidget(); outer.setStyleSheet("background: transparent;")
    lay = QVBoxLayout(outer); lay.setContentsMargins(36, 28, 36, 28); lay.setSpacing(18)

    hdr = QVBoxLayout(); hdr.setSpacing(4)
    hdr.addWidget(lbl_sub("GESTION"))
    hdr.addWidget(lbl_title("Investissements"))
    lay.addLayout(hdr)
    lay.addWidget(h_sep())

    sl = QHBoxLayout(); sl.setSpacing(12)
    for t, v, c in [("Montant Net", "124 580 $", C_ACCENT), ("Montant Investi", "38 200 $", C_GREEN), ("Rendement", "+6.2 %", C_YELLOW)]:
        sl.addWidget(StatCard(t, v, c))
    lay.addLayout(sl)

    fw = QWidget()
    fw.setStyleSheet(f"background: {C_CARD}; border: 1px solid {C_BORDER}; border-radius: 6px;")
    fl = QVBoxLayout(fw); fl.setContentsMargins(24, 18, 24, 18); fl.setSpacing(12)
    fl.addWidget(lbl_field("NOUVELLE OPERATION"))

    r = QHBoxLayout(); r.setSpacing(12)
    r.addWidget(field("Montant ($)"))
    r.addWidget(field("Description"))
    fl.addLayout(r)

    br = QHBoxLayout(); br.setSpacing(12)
    br.addWidget(btn("INVESTIR",               C_GREEN, h=42))
    br.addWidget(btn("RETIRER INVESTISSEMENT", C_RED,   h=42))
    br.addStretch()
    fl.addLayout(br)
    lay.addWidget(fw)
    lay.addStretch()
    return scroll_wrap(outer)


# ── Parametres ─────────────────────────────────────────────────────────────
def page_parametres(username):
    outer = QWidget(); outer.setStyleSheet("background: transparent;")
    lay = QVBoxLayout(outer); lay.setContentsMargins(36, 28, 36, 28); lay.setSpacing(18)

    hdr = QVBoxLayout(); hdr.setSpacing(4)
    hdr.addWidget(lbl_sub("CONFIGURATION"))
    hdr.addWidget(lbl_title("Parametres"))
    lay.addLayout(hdr)
    lay.addWidget(h_sep())

    # Profil
    pw = QWidget()
    pw.setStyleSheet(f"background: {C_CARD}; border: 1px solid {C_BORDER}; border-radius: 6px;")
    pl = QHBoxLayout(pw); pl.setContentsMargins(24, 16, 24, 16); pl.setSpacing(16)

    av = QLabel(username[0].upper())
    av.setFixedSize(52, 52)
    av.setAlignment(Qt.AlignmentFlag.AlignCenter)
    av.setStyleSheet(f"""
        background: {C_ACCENT}22;
        border: 1px solid {C_ACCENT}55;
        border-radius: 26px;
        color: {C_ACCENT};
        font-family: '{FONT}';
        font-size: 22px;
        font-weight: bold;
    """)

    info = QVBoxLayout(); info.setSpacing(4)
    info.addWidget(lbl(username.upper(), size=16, bold=True))
    info.addWidget(lbl("SUPER ADMIN  ·  BEATS BANK", size=10, color=C_ACCENT, bold=True, spacing=2))

    pl.addWidget(av)
    pl.addLayout(info)
    pl.addStretch()
    pl.addWidget(btn("MODIFIER PROFIL", C_ACCENT))
    lay.addWidget(pw)

    lay.addWidget(lbl_field("ADMINISTRATEURS"))

    admins = [("admin", "Super Admin"), ("gestionnaire01", "Admin"), ("gestionnaire02", "Admin")]
    for uname, role in admins:
        rw = QWidget(); rw.setFixedHeight(48)
        rw.setStyleSheet(f"background: {C_CARD}; border: 1px solid {C_BORDER}; border-radius: 3px;")
        rl = QHBoxLayout(rw); rl.setContentsMargins(20, 0, 16, 0); rl.setSpacing(16)
        rl.addWidget(lbl(uname, size=12))
        rl.addWidget(lbl(role, size=10, color=C_ACCENT, bold=True, spacing=1))
        rl.addStretch()
        if uname != "admin":
            rl.addWidget(btn("RETIRER", C_RED, h=32))
        lay.addWidget(rw)

    lay.addWidget(btn("AJOUTER UN ADMIN", C_GREEN, h=42))
    lay.addStretch()
    return scroll_wrap(outer)


# ══════════════════════════════════════════════════════════════════════════════
#  Fenêtre Dashboard
# ══════════════════════════════════════════════════════════════════════════════
class DashboardWindow(QWidget):
    def __init__(self, username="admin", login_window=None):
        super().__init__()
        self.username = username
        self.login_window = login_window
        self.setWindowTitle("BEATS BANK — Dashboard")
        self.setFixedSize(1200, 720)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self._drag_pos = None
        self._build_ui()

    def _build_ui(self):
        self.bg = MatrixBackground(self)
        self.bg.setGeometry(0, 0, 1200, 720)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # ── Barre de titre ────────────────────────────────────────────────
        title_bar = QWidget()
        title_bar.setFixedHeight(34)
        title_bar.setStyleSheet("background: rgba(6,8,10,200);")
        tb = QHBoxLayout(title_bar)
        tb.setContentsMargins(14, 0, 10, 0)
        tb.setSpacing(6)

        tb.addWidget(lbl("BEATS BANK  //  TABLEAU DE BORD ADMIN", size=10, color=C_DIM, spacing=2))
        tb.addStretch()

        for symbol, action, hover_color in [("─", self.showMinimized, C_ACCENT), ("✕", self.close, C_RED)]:
            b = QPushButton(symbol)
            b.setFixedSize(28, 22)
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            b.setStyleSheet(f"""
                QPushButton {{ background: transparent; color: {C_DIM}; border: 1px solid #1a3040; border-radius: 3px; font-size: 11px; {'padding-bottom: 3px;' if symbol == '─' else ''} }}
                QPushButton:hover {{ color: #ffffff; border-color: {hover_color}; background: {hover_color}22; }}
            """)
            b.clicked.connect(action)
            tb.addWidget(b)

        outer.addWidget(title_bar)

        # ── Corps principal ───────────────────────────────────────────────
        body = QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)
        outer.addLayout(body)

        # ── Sidebar ───────────────────────────────────────────────────────
        sidebar = QWidget()
        sidebar.setFixedWidth(210)
        sidebar.setStyleSheet(f"background: rgba(8,13,18,215); border-right: 1px solid {C_BORDER};")
        sb = QVBoxLayout(sidebar)
        sb.setContentsMargins(0, 0, 0, 0)
        sb.setSpacing(0)

        # Logo sidebar
        logo_w = QWidget(); logo_w.setFixedHeight(82)
        logo_w.setStyleSheet("background: transparent;")
        logo_l = QHBoxLayout(logo_w)
        logo_l.setContentsMargins(16, 10, 16, 10)
        logo_l.setSpacing(12)

        lbl_logo = QLabel()
        px = QPixmap(os.path.join(BASE_DIR, "logo.png"))
        lbl_logo.setPixmap(px.scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        lbl_logo.setStyleSheet("background: transparent;")

        lbl_bank = QLabel("BEATS\nBANK")
        lbl_bank.setStyleSheet(f"color: {C_TEXT}; font-family: '{FONT}'; font-size: 14px; font-weight: bold; letter-spacing: 3px; background: transparent;")

        logo_l.addWidget(lbl_logo)
        logo_l.addWidget(lbl_bank)
        logo_l.addStretch()
        sb.addWidget(logo_w)
        sb.addWidget(h_sep())
        sb.addSpacing(6)

        # Navigation
        nav_items = [
            "Tableau de bord",
            "Clients",
            "Cartes",
            "Transactions",
            "Investissements",
            "Parametres",
        ]
        self._nav_btns = []
        self._stack = QStackedWidget()
        self._stack.setStyleSheet("background: transparent;")

        for label in nav_items:
            b = SidebarBtn(label)
            b.clicked.connect(lambda checked, nb=b: self._navigate(nb))
            sb.addWidget(b)
            self._nav_btns.append(b)

        sb.addStretch()
        sb.addWidget(h_sep())

        # Bouton déconnexion
        btn_out = SidebarBtn("Deconnexion")
        btn_out.clicked.connect(self._logout)
        sb.addWidget(btn_out)
        sb.addSpacing(6)

        # ── Stack de contenu ──────────────────────────────────────────────
        self._stack.addWidget(page_dashboard(self.username))
        self._stack.addWidget(page_clients())
        self._stack.addWidget(page_cartes())
        self._stack.addWidget(page_transactions())
        self._stack.addWidget(page_investissements())
        self._stack.addWidget(page_parametres(self.username))

        body.addWidget(sidebar)
        body.addWidget(self._stack)

        # Activer le tableau de bord par défaut
        self._nav_btns[0].setChecked(True)

    def _navigate(self, clicked):
        for i, b in enumerate(self._nav_btns):
            if b is clicked:
                b.setChecked(True)
                self._stack.setCurrentIndex(i)
            else:
                b.setChecked(False)

    def _logout(self):
        if self.login_window:
            self.login_window.input_username.clear()
            self.login_window.input_password.clear()
            self.login_window.show()
        self.close()

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = e.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, e):
        if self._drag_pos and e.buttons() == Qt.MouseButton.LeftButton:
            self.move(e.globalPosition().toPoint() - self._drag_pos)

    def mouseReleaseEvent(self, e):
        self._drag_pos = None


# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    w = DashboardWindow("admin")
    w.show()
    sys.exit(app.exec())