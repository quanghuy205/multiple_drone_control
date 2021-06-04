#!/usr/bin/python

import sys

from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import *
import os
import sys

class Interceptor(QWebEngineUrlRequestInterceptor):
    def interceptRequest(self, info):
        info.setHttpHeader(b"Accept-Language", b"en-US,en;q=0.9,es;q=0.8,de;q=0.7")

def main():
    app = QApplication(sys.argv)

    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'map.html'))

    local_url = QUrl.fromLocalFile(file_path)
    web = QWebEngineView()

    interceptor = Interceptor()
    web.page().profile().setUrlRequestInterceptor(interceptor)
    p = QWebEnginePage()
    web.setPage(p)
    web.load(QUrl(local_url))
    web.show()

    sys.exit(app.exec_())
if __name__ == '__main__':
    main()