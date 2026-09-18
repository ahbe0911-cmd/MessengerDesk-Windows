import sys
from pathlib import Path
from PySide6.QtCore import Qt, QUrl, QSize
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QScrollArea
from PySide6.QtWebEngineCore import QWebEngineProfile, QWebEnginePage
from PySide6.QtWebEngineWidgets import QWebEngineView

APP_DIR = Path.home() / ".messengerdesk"
APP_DIR.mkdir(exist_ok=True)

MESSENGERS = [
    ("بله", "https://web.bale.ai/", "#16a7b7"),
    ("ایتا", "https://web.eitaa.com/", "#f28b20"),
    ("شاد", "https://web.shad.ir/", "#13ad69"),
    ("روبیکا", "https://web.rubika.ir/", "#7257e8"),
]

class MessengerCard(QFrame):
    def __init__(self, name, url, accent, parent=None):
        super().__init__(parent)
        self.name, self.url, self.accent = name, url, accent
        self.setObjectName("card")
        self.setMinimumWidth(340)
        layout=QVBoxLayout(self); layout.setContentsMargins(0,0,0,0); layout.setSpacing(0)
        head=QFrame(); head.setObjectName("cardHead")
        hl=QHBoxLayout(head); hl.setContentsMargins(14,10,14,10)
        dot=QLabel("●"); dot.setStyleSheet(f"color:{accent};font-size:25px")
        title=QLabel(name); title.setObjectName("cardTitle")
        more=QPushButton("⋮"); more.setObjectName("iconBtn"); more.setFixedSize(34,34)
        hl.addWidget(dot); hl.addWidget(title); hl.addStretch(); hl.addWidget(more)
        layout.addWidget(head)
        profile=QWebEngineProfile(f"profile-{name}", self)
        storage=APP_DIR / "profiles" / name
        storage.mkdir(parents=True, exist_ok=True)
        profile.setPersistentStoragePath(str(storage))
        profile.setCachePath(str(storage/"cache"))
        profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies)
        page=QWebEnginePage(profile, self)
        self.web=QWebEngineView(); self.web.setPage(page); self.web.setUrl(QUrl(url))
        layout.addWidget(self.web,1)
        foot=QFrame(); fl=QHBoxLayout(foot); fl.setContentsMargins(8,5,8,5)
        for text, fn in [("⌂",lambda:self.web.setUrl(QUrl(self.url))),("↻",self.web.reload),("←",self.web.back),("→",self.web.forward)]:
            b=QPushButton(text); b.setObjectName("navBtn"); b.clicked.connect(fn); fl.addWidget(b)
        layout.addWidget(foot)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("میزکار پیام‌رسان‌ها")
        self.resize(1540,900)
        root=QWidget(); self.setCentralWidget(root)
        outer=QVBoxLayout(root); outer.setContentsMargins(14,12,14,12); outer.setSpacing(10)
        top=QFrame(); top.setObjectName("topbar"); tl=QHBoxLayout(top)
        settings=QPushButton("⚙"); settings.setObjectName("topBtn")
        search=QLineEdit(); search.setPlaceholderText("جستجو در میزکار…"); search.setObjectName("search")
        subtitle=QLabel("همه پیام‌های شما، در یک نگاه"); subtitle.setObjectName("subtitle")
        title=QLabel("میزکار پیام‌رسان‌ها"); title.setObjectName("title")
        brand=QVBoxLayout(); brand.addWidget(title,0,Qt.AlignRight); brand.addWidget(subtitle,0,Qt.AlignRight)
        tl.addWidget(settings); tl.addWidget(search,1); tl.addLayout(brand)
        outer.addWidget(top)
        scroll=QScrollArea(); scroll.setWidgetResizable(True); scroll.setFrameShape(QFrame.NoFrame)
        content=QWidget(); row=QHBoxLayout(content); row.setContentsMargins(0,0,0,0); row.setSpacing(10)
        # RTL order visually: Rubika, Shad, Eitaa, Bale from left to right; Bale starts at right.
        for data in MESSENGERS:
            row.addWidget(MessengerCard(*data),1)
        scroll.setWidget(content); outer.addWidget(scroll,1)
        self.setStyleSheet(STYLE)

STYLE="""
QWidget{font-family:'Vazirmatn','Segoe UI';font-size:13px;color:#152238}
QMainWindow,QWidget{background:#dbe9f2}
#topbar{background:rgba(25,63,94,220);border-radius:18px}
#title{color:white;font-size:24px;font-weight:800}
#subtitle{color:#d7e5ef;font-size:12px}
#search{background:rgba(255,255,255,230);border:0;border-radius:16px;padding:10px 15px;min-width:320px}
#topBtn,#iconBtn,#navBtn{border:0;border-radius:10px;background:rgba(255,255,255,180);padding:7px}
#topBtn{font-size:20px;color:white;background:transparent}
#card{background:#f8fbfd;border:1px solid rgba(255,255,255,180);border-radius:22px}
#cardHead{background:rgba(255,255,255,210);border-top-left-radius:22px;border-top-right-radius:22px}
#cardTitle{font-size:20px;font-weight:800}
#navBtn:hover,#iconBtn:hover{background:white}
QScrollArea{background:transparent}
"""

if __name__=="__main__":
    app=QApplication(sys.argv)
    app.setLayoutDirection(Qt.RightToLeft)
    w=MainWindow(); w.show()
    sys.exit(app.exec())
