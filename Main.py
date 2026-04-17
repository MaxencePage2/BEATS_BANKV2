import sys
import os
import math
import random
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QHBoxLayout, QFrame,
    QGraphicsDropShadowEffect, QMessageBox
)
from PyQt6.QtGui import (
    QPixmap, QFont, QColor, QPainter, QPen, QBrush,
    QLinearGradient, QRadialGradient
)
from PyQt6.QtCore import Qt, QTimer, QRectF


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# ══════════════════════════════════════════════════════════════════════════════
#  Background avec pluie de code Matrix
# ══════════════════════════════════════════════════════════════════════════════
class MatrixBackground(QWidget):
    CHARS = "01アイウエオカキクケコサシスセソタチツテトナニヌネノ"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.columns = []
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(60)

    def _init_columns(self):
        cols = max(1, self.width() // 20)
        self.columns = []
        for i in range(cols):
            self.columns.append({
                "x": i * 20 + random.randint(0, 8),
                "y": random.randint(-600, 0),
                "speed": random.uniform(1.5, 4.0),
                "length": random.randint(6, 18),
                "chars": [random.choice(self.CHARS) for _ in range(22)],
                "alpha": random.uniform(0.04, 0.12),
            })

    def resizeEvent(self, event):
        self._init_columns()
        super().resizeEvent(event)

    def showEvent(self, event):
        self._init_columns()
        super().showEvent(event)

    def _tick(self):
        for col in self.columns:
            col["y"] += col["speed"]
            if col["y"] > self.height() + col["length"] * 18:
                col["y"] = random.randint(-200, -20)
                col["speed"] = random.uniform(1.5, 4.0)
                col["alpha"] = random.uniform(0.04, 0.12)
            if random.random() < 0.08:
                idx = random.randint(0, len(col["chars"]) - 1)
                col["chars"][idx] = random.choice(self.CHARS)
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        grad = QLinearGradient(0, 0, 0, self.height())
        grad.setColorAt(0.0, QColor("#060809"))
        grad.setColorAt(1.0, QColor("#0a0e12"))
        p.fillRect(self.rect(), grad)

        font = QFont("Courier New", 9)
        p.setFont(font)

        for col in self.columns:
            for i in range(col["length"]):
                y = col["y"] - i * 17
                if y < -17 or y > self.height():
                    continue
                brightness = 1.0 if i == 0 else max(0.1, 1.0 - i / col["length"])
                alpha = int(col["alpha"] * brightness * 255 * 2.8)
                alpha = min(255, alpha)
                if i == 0:
                    char_color = QColor(180, 230, 255, min(255, alpha * 3))
                else:
                    char_color = QColor(42, 159, 214, alpha)
                p.setPen(QPen(char_color))
                char = col["chars"][i % len(col["chars"])]
                p.drawText(int(col["x"]), int(y), char)
        p.end()


# ══════════════════════════════════════════════════════════════════════════════
#  Carte de login avec bordure lumineuse tournante
# ══════════════════════════════════════════════════════════════════════════════
class LoginCard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(400, 500)
        self._glow_angle = 0.0
        self._anim = QTimer(self)
        self._anim.timeout.connect(self._rotate_glow)
        self._anim.start(30)

    def _rotate_glow(self):
        self._glow_angle = (self._glow_angle + 1.2) % 360
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        r = QRectF(1, 1, self.width() - 2, self.height() - 2)
        radius = 6.0

        # Fond de la carte
        p.setPen(Qt.PenStyle.NoPen)
        card_grad = QLinearGradient(0, 0, 0, self.height())
        card_grad.setColorAt(0.0, QColor("#0e1620"))
        card_grad.setColorAt(1.0, QColor("#080d14"))
        p.setBrush(QBrush(card_grad))
        p.drawRoundedRect(r, radius, radius)

        # Bordure animée
        angle_rad = math.radians(self._glow_angle)
        cx = self.width() / 2 + math.cos(angle_rad) * self.width() * 0.7
        cy = self.height() / 2 + math.sin(angle_rad) * self.height() * 0.7
        glow = QRadialGradient(cx, cy, self.width())
        glow.setColorAt(0.0, QColor(42, 159, 214, 110))
        glow.setColorAt(0.5, QColor(42, 159, 214, 30))
        glow.setColorAt(1.0, QColor(42, 159, 214, 0))
        p.setPen(QPen(QBrush(glow), 1.5))
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawRoundedRect(r, radius, radius)

        # Bordure fixe intérieure
        p.setPen(QPen(QColor("#162030"), 1))
        p.drawRoundedRect(r.adjusted(1, 1, -1, -1), radius - 0.5, radius - 0.5)
        p.end()


# ══════════════════════════════════════════════════════════════════════════════
#  Styles
# ══════════════════════════════════════════════════════════════════════════════
FIELD_STYLE = """
QLineEdit {
    background-color: #07111a;
    border: 1px solid #152535;
    border-radius: 4px;
    color: #b8d8f0;
    padding: 0 14px;
    font-family: 'Courier New';
    font-size: 12px;
    selection-background-color: #2a9fd6;
}
QLineEdit:focus {
    border: 1px solid #2a9fd6;
    background-color: #091520;
    color: #e8f4ff;
}
"""

BTN_STYLE = """
QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #38b8e8, stop:1 #1878a8);
    color: #001018;
    border: none;
    border-radius: 4px;
    font-family: 'Courier New';
    font-size: 11px;
    font-weight: bold;
    letter-spacing: 4px;
}
QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #60d8ff, stop:1 #2a9fd6);
}
QPushButton:pressed {
    background: #125878;
}
"""


# ══════════════════════════════════════════════════════════════════════════════
#  Fenêtre principale
# ══════════════════════════════════════════════════════════════════════════════
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BEATS BANK — Connexion")
        self.setFixedSize(980, 610)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self._drag_pos = None
        self._build_ui()

    def _build_ui(self):
        # Background animé pleine fenêtre
        self.bg = MatrixBackground(self)
        self.bg.setGeometry(0, 0, 980, 610)

        # Layout racine VERTICAL : barre de titre + contenu
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # ── Barre de titre intégrée ───────────────────────────────────────
        title_bar = QWidget()
        title_bar.setFixedHeight(34)
        title_bar.setStyleSheet("background: rgba(6,8,10,180);")
        tb = QHBoxLayout(title_bar)
        tb.setContentsMargins(14, 0, 10, 0)
        tb.setSpacing(6)

        lbl_tb = QLabel("BEATS BANK  //  CONNEXION SÉCURISÉE")
        lbl_tb.setStyleSheet("""
            color: #2a5570;
            font-family: 'Courier New';
            font-size: 9px;
            letter-spacing: 2px;
        """)

        # Bouton minimiser
        btn_min = QPushButton("─")
        btn_min.setFixedSize(28, 22)
        btn_min.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_min.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #2a5570;
                border: 1px solid #1a3040;
                border-radius: 3px;
                font-size: 11px;
                padding-bottom: 3px;
            }
            QPushButton:hover { color: #e8f4ff; border-color: #2a9fd6; background: #0d1f2d; }
        """)
        btn_min.clicked.connect(self.showMinimized)

        # Bouton fermer
        btn_close = QPushButton("✕")
        btn_close.setFixedSize(28, 22)
        btn_close.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_close.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #2a5570;
                border: 1px solid #1a3040;
                border-radius: 3px;
                font-size: 11px;
            }
            QPushButton:hover { color: #ffffff; border-color: #cc3333; background: #3a0808; }
        """)
        btn_close.clicked.connect(self.close)

        tb.addWidget(lbl_tb)
        tb.addStretch()
        tb.addWidget(btn_min)
        tb.addWidget(btn_close)

        outer.addWidget(title_bar)

        # Layout principal horizontal
        root = QHBoxLayout()
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)
        outer.addLayout(root)

        # ── Panneau gauche — Logo centré ──────────────────────────────────
        left = QWidget()
        left.setFixedWidth(460)
        left.setStyleSheet("background: transparent;")
        left_layout = QVBoxLayout(left)
        left_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.setContentsMargins(40, 0, 40, 0)

        logo_label = QLabel()
        logo_path = os.path.join(BASE_DIR, "logo.png")
        pixmap = QPixmap(logo_path)
        logo_label.setPixmap(
            pixmap.scaled(300, 300,
                          Qt.AspectRatioMode.KeepAspectRatio,
                          Qt.TransformationMode.SmoothTransformation)
        )
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setStyleSheet("background: transparent;")

        logo_shadow = QGraphicsDropShadowEffect()
        logo_shadow.setBlurRadius(70)
        logo_shadow.setColor(QColor(42, 159, 214, 130))
        logo_shadow.setOffset(0, 0)
        logo_label.setGraphicsEffect(logo_shadow)

        lbl_name = QLabel("BEATS BANK")
        lbl_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_name.setStyleSheet("""
            color: #c8e0f0;
            font-family: 'Courier New';
            font-size: 24px;
            font-weight: bold;
            letter-spacing: 8px;
            background: transparent;
        """)

        lbl_tag = QLabel("SÉCURISÉ  ·  FIABLE   ·  RAPIDE ")
        lbl_tag.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_tag.setStyleSheet("""
            color: #2a9fd6;
            font-family: 'Courier New';
            font-size: 12px;
            letter-spacing: 5px;
            background: transparent;
        """)

        left_layout.addStretch()
        left_layout.addWidget(logo_label)
        left_layout.addSpacing(22)
        left_layout.addWidget(lbl_name)
        left_layout.addSpacing(8)
        left_layout.addWidget(lbl_tag)
        left_layout.addStretch()

        # Séparateur vertical
        v_sep = QFrame()
        v_sep.setFrameShape(QFrame.Shape.VLine)
        v_sep.setStyleSheet("color: #0f2030; max-width: 1px;")

        # ── Panneau droit — Carte login ───────────────────────────────────
        right = QWidget()
        right.setStyleSheet("background: transparent;")
        right_layout = QVBoxLayout(right)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_layout.setContentsMargins(20, 0, 20, 0)

        card = LoginCard(right)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(38, 32, 38, 32)
        card_layout.setSpacing(0)

        lbl_access = QLabel("ACCÈS SÉCURISÉ")
        lbl_access.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_access.setStyleSheet("""
            color: #2a9fd6;
            font-family: 'Courier New';
            font-size: 11px;
            font-weight: bold;
            letter-spacing: 5px;
            background: transparent;
        """)

        lbl_conn = QLabel("Connexion")
        lbl_conn.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_conn.setStyleSheet("""
            color: #ddeeff;
            font-family: 'Courier New';
            font-size: 20px;
            font-weight: bold;
            letter-spacing: 2px;
            background: transparent;
        """)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color: #152535;")

        def make_label(text):
            l = QLabel(text)
            l.setStyleSheet("""
                color: #2a9fd6;
                font-family: 'Courier New';
                font-size: 11px;
                font-weight: bold;
                letter-spacing: 3px;
                background: transparent;
            """)
            return l

        self.input_username = QLineEdit()
        self.input_username.setPlaceholderText("Entrez votre identifiant")
        self.input_username.setFixedHeight(42)
        self.input_username.setStyleSheet(FIELD_STYLE)

        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Entrez votre mot de passe")
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_password.setFixedHeight(42)
        self.input_password.setStyleSheet(FIELD_STYLE)
        self.input_password.returnPressed.connect(self._handle_login)

        self.btn_login = QPushButton("SE CONNECTER")
        self.btn_login.setFixedHeight(46)
        self.btn_login.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_login.setStyleSheet(BTN_STYLE)
        self.btn_login.clicked.connect(self._handle_login)

        btn_glow = QGraphicsDropShadowEffect()
        btn_glow.setBlurRadius(22)
        btn_glow.setColor(QColor(42, 159, 214, 120))
        btn_glow.setOffset(0, 4)
        self.btn_login.setGraphicsEffect(btn_glow)

        lbl_forgot = QLabel("Mot de passe oublié ?")
        lbl_forgot.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_forgot.setCursor(Qt.CursorShape.PointingHandCursor)
        lbl_forgot.setStyleSheet("""
            color: #2a9fd6;
            font-family: 'Courier New';
            font-size: 11px;
            text-decoration: underline;
            background: transparent;
        """)

        lbl_ver = QLabel("v2.0.0  ·  © 2025 BEATS BANK")
        lbl_ver.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_ver.setStyleSheet("""
            color: #2a9fd6;
            font-family: 'Courier New';
            font-size: 10px;
            letter-spacing: 2px;
            background: transparent;
        """)

        card_layout.addWidget(lbl_access)
        card_layout.addSpacing(4)
        card_layout.addWidget(lbl_conn)
        card_layout.addSpacing(18)
        card_layout.addWidget(sep)
        card_layout.addSpacing(22)
        card_layout.addWidget(make_label("NOM D'UTILISATEUR"))
        card_layout.addSpacing(6)
        card_layout.addWidget(self.input_username)
        card_layout.addSpacing(16)
        card_layout.addWidget(make_label("MOT DE PASSE"))
        card_layout.addSpacing(6)
        card_layout.addWidget(self.input_password)
        card_layout.addSpacing(28)
        card_layout.addWidget(self.btn_login)
        card_layout.addSpacing(14)
        card_layout.addWidget(lbl_forgot)
        card_layout.addStretch()
        card_layout.addWidget(lbl_ver)

        right_layout.addWidget(card)

        root.addWidget(left)
        root.addWidget(v_sep)
        root.addWidget(right)

    # ── Login ─────────────────────────────────────────────────────────────────
    def _handle_login(self):
        username = self.input_username.text().strip()
        password = self.input_password.text()
        if not username or not password:
            self._show_error("Veuillez remplir tous les champs.")
            return
        if username == "admin" and password == "1234":
            from dashboard import DashboardWindow
            self.hide()
            self._dashboard = DashboardWindow(username=username, login_window=self)
            self._dashboard.show()
        else:
            self._show_error("Identifiant ou mot de passe incorrect.")
            self.input_password.clear()
            self.input_password.setFocus()

    def _show_error(self, msg):
        box = QMessageBox(self)
        box.setWindowTitle("Erreur")
        box.setText(msg)
        box.setIcon(QMessageBox.Icon.Warning)
        box.setStyleSheet("""
            QMessageBox { background: #0c1219; color: #c8e0f0; font-family: 'Courier New'; }
            QPushButton { background: #1a3040; color: #c8e0f0; border: 1px solid #2a9fd6;
                          padding: 4px 16px; font-family: 'Courier New'; }
            QPushButton:hover { background: #2a9fd6; color: #000; }
        """)
        box.exec()

    # ── Drag ──────────────────────────────────────────────────────────────────
    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = e.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, e):
        if self._drag_pos and e.buttons() == Qt.MouseButton.LeftButton:
            self.move(e.globalPosition().toPoint() - self._drag_pos)

    def mouseReleaseEvent(self, e):
        self._drag_pos = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    w = LoginWindow()
    w.show()
    sys.exit(app.exec())