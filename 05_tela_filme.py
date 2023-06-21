from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QGuiApplication
import sys
import subprocess
import webview

# pip install PyQt6-WebEngine
# pip install PyQt6    

tmdb = sys.argv[1]
arquivo = sys.argv[2]
trailer = sys.argv[3]

def abrir_trailer(url):#abrir o trailer pelo link
    
    webview.create_window("Trailer:", url=url, width=700, height=400,on_top=True)
    webview.start()

class MainWindow(QMainWindow):
        
    def __init__(self, tmdb,arquivo, trailer):
        super().__init__()

        self.setWindowTitle("Informações do Filme")
        self.resize(1300, 720)

        self.webview = QWebEngineView()
        self.webview.load(QUrl(tmdb))

        button_trailer = QPushButton("Trailer")
        button_Assistir = QPushButton("Assistir")
        button_copiar_link = QPushButton("Copiar Link")

        button_style = "QPushButton { \
                                font-size: 18px; \
                                padding: 8px 16px; \
                                border: none; \
                                border-radius: 3px; \
                                background-color: #132335; \
                                color: white; \
                            }"

        button_trailer.setStyleSheet(button_style)
        button_Assistir.setStyleSheet(button_style)
        button_copiar_link.setStyleSheet(button_style)

        layout_buttons = QHBoxLayout()
        layout_buttons.addWidget(button_trailer)
        layout_buttons.addWidget(button_Assistir)
        layout_buttons.addWidget(button_copiar_link)

        layout_main = QVBoxLayout()
        layout_main.addWidget(self.webview)
        layout_main.addLayout(layout_buttons)

        central_widget = QWidget()
        central_widget.setLayout(layout_main)
        self.setCentralWidget(central_widget)

        button_copiar_link.clicked.connect(self.copiar_link)
        button_Assistir.clicked.connect(lambda: subprocess.run(["python", "07_vlc.py",str(arquivo)]))
        button_trailer.clicked.connect(lambda: abrir_trailer(trailer))
        

    def closeEvent(self, event):
        self.close()

    def copiar_link(self):
        clipboard = QGuiApplication.clipboard()
        clipboard.setText(arquivo)
        QMessageBox.information(
            self, "Link Copiado", "O link foi copiado para a área de transferência.")

def tela_filme(tmdb,arquivo,trailer):
    app = QApplication(sys.argv)
    mainWindow = MainWindow(tmdb, arquivo, trailer)
    mainWindow.show()
    app.exec_()

if __name__ == "__main__":
    tela_filme(tmdb, arquivo, trailer)
