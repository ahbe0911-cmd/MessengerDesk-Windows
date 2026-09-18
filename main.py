import os, sys
from pathlib import Path

# Chromium flags aimed at desktop stability and lower background work.
os.environ.setdefault("QTWEBENGINE_CHROMIUM_FLAGS", "--disable-background-networking --disable-component-update --disable-features=Translate,MediaRouter")

from PySide6.QtCore import Qt, QUrl, QTimer
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QScrollArea
from PySide6.QtWebEngineCore import QWebEngineProfile, QWebEnginePage, QWebEngineSettings
from PySide6.QtWebEngineWidgets import QWebEngineView

APP_DIR = Path(os.getenv("LOCALAPPDATA", Path.home())) / "MessengerDesk"
APP_DIR.mkdir(parents=True, exist_ok=True)

MESSENGERS=[
 ("بله","https://web.bale.ai/","#16a7b7"),
 ("ایتا","https://web.eitaa.com/","#f28b20"),
 ("شاد","https://web.shad.ir/","#13ad69"),
 ("روبیکا","https://web.rubika.ir/","#7257e8"),
]

class MessengerCard(QFrame):
    def __init__(self,name,url,accent,delay=0,parent=None):
        super().__init__(parent); self.name=name; self.url=url; self.loaded=False
        self.setObjectName("card"); self.setMinimumWidth(330)
        root=QVBoxLayout(self); root.setContentsMargins(0,0,0,0); root.setSpacing(0)
        head=QFrame(); head.setObjectName("cardHead"); h=QHBoxLayout(head)
        dot=QLabel("●"); dot.setStyleSheet(f"color:{accent};font-size:24px")
        title=QLabel(name); title.setObjectName("cardTitle")
        self.status=QLabel("در حال آماده‌سازی…"); self.status.setObjectName("status")
        reload_btn=QPushButton("↻"); reload_btn.setObjectName("iconBtn")
        h.addWidget(dot); h.addWidget(title); h.addWidget(self.status); h.addStretch(); h.addWidget(reload_btn)
        root.addWidget(head)

        # Each service gets a persistent profile. Login/cookies survive app restarts.
        storage=APP_DIR/"profiles"/name; storage.mkdir(parents=True,exist_ok=True)
        self.profile=QWebEngineProfile(f"MessengerDesk-{name}",self)
        self.profile.setPersistentStoragePath(str(storage/"storage"))
        self.profile.setCachePath(str(storage/"cache"))
        self.profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies)
        self.profile.setHttpCacheType(QWebEngineProfile.HttpCacheType.DiskHttpCache)
        self.profile.setHttpCacheMaximumSize(96*1024*1024)

        self.page=QWebEnginePage(self.profile,self)
        s=self.page.settings()
        s.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled,True)
        s.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled,True)
        s.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled,False)

        self.web=QWebEngineView(); self.web.setPage(self.page)
        root.addWidget(self.web,1)
        foot=QFrame(); f=QHBoxLayout(foot); f.setContentsMargins(8,5,8,5)
        for txt,fn in [("⌂",self.home),("←",self.web.back),("→",self.web.forward)]:
            b=QPushButton(txt); b.setObjectName("navBtn"); b.clicked.connect(fn); f.addWidget(b)
        root.addWidget(foot)
        reload_btn.clicked.connect(self.web.reload)
        self.web.loadStarted.connect(lambda:self.status.setText("در حال بارگذاری…"))
        self.web.loadFinished.connect(self._loaded)
        QTimer.singleShot(delay,self.load)

    def load(self):
        if not self.loaded:
            self.loaded=True; self.web.setUrl(QUrl(self.url))
    def home(self): self.web.setUrl(QUrl(self.url))
    def _loaded(self,ok): self.status.setText("" if ok else "خطای اتصال")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__(); self.setWindowTitle("میزکار پیام‌رسان‌ها"); self.resize(1500,860)
        root=QWidget(); self.setCentralWidget(root)
        outer=QVBoxLayout(root); outer.setContentsMargins(12,10,12,10); outer.setSpacing(9)
        top=QFrame(); top.setObjectName("topbar"); tl=QHBoxLayout(top)
        search=QLineEdit(); search.setPlaceholderText("جستجو…"); search.setObjectName("search")
        brand=QVBoxLayout(); title=QLabel("میزکار پیام‌رسان‌ها"); title.setObjectName("title")
        sub=QLabel("بله • ایتا • شاد • روبیکا"); sub.setObjectName("subtitle")
        brand.addWidget(title,0,Qt.AlignRight); brand.addWidget(sub,0,Qt.AlignRight)
        tl.addWidget(search,1); tl.addLayout(brand); outer.addWidget(top)
        scroll=QScrollArea(); scroll.setWidgetResizable(True); scroll.setFrameShape(QFrame.NoFrame)
        content=QWidget(); row=QHBoxLayout(content); row.setContentsMargins(0,0,0,0); row.setSpacing(9)
        # Stagger Chromium page loading: avoids four heavy logins starting at the same instant.
        for i,data in enumerate(MESSENGERS): row.addWidget(MessengerCard(*data,delay=i*900),1)
        scroll.setWidget(content); outer.addWidget(scroll,1); self.setStyleSheet(STYLE)

STYLE="""
QWidget{font-family:'Vazirmatn','Segoe UI';font-size:13px;color:#172235}
QMainWindow,QWidget{background:#dce8ef}
#topbar{background:#244760;border-radius:16px} #title{color:white;font-size:22px;font-weight:800}
#subtitle{color:#d8e6ee} #search{background:white;border:0;border-radius:14px;padding:9px 14px;min-width:280px}
#card{background:#f8fbfd;border:1px solid #d8e2e8;border-radius:18px}
#cardHead{background:#f4f8fa;border-top-left-radius:18px;border-top-right-radius:18px}
#cardTitle{font-size:18px;font-weight:800} #status{color:#71808b;font-size:11px}
#iconBtn,#navBtn{border:0;border-radius:9px;background:#e9f0f4;padding:6px 10px}
#iconBtn:hover,#navBtn:hover{background:white} QScrollArea{background:transparent}
"""

if __name__=="__main__":
    app=QApplication(sys.argv); app.setApplicationName("MessengerDesk"); app.setOrganizationName("MessengerDesk")
    app.setLayoutDirection(Qt.RightToLeft)
    w=MainWindow(); w.show(); sys.exit(app.exec())
