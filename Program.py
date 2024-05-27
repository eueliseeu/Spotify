from PyQt5 import QtCore, QtGui, QtWidgets
import os
import subprocess
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

DOWNLOADS_FOLDER = os.path.join(os.path.expanduser('~'), 'Downloads')
DOWNLOAD_MEDIA_PLAY_FOLDER = os.path.join(DOWNLOADS_FOLDER, 'Rádio indoor')

if not os.path.exists(DOWNLOAD_MEDIA_PLAY_FOLDER):
    os.makedirs(DOWNLOAD_MEDIA_PLAY_FOLDER)

class DownloadThread(QtCore.QThread):
    download_finished = QtCore.pyqtSignal()

    def __init__(self, playlist_id, output_directory):
        super().__init__()
        self.playlist_id = playlist_id
        self.output_directory = output_directory

    def run(self):
        download_spotify_playlist_tracks(self.playlist_id, self.output_directory)
        self.download_finished.emit()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(784, 465)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet("background: #171717")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(138, 216, 507, 33))
        self.lineEdit.setStyleSheet("border:none;\n"
"border-radius: 15px;\n"
"background: #404040;\n"
"padding: 36px;\n"
"font-size: 13px;\n"
"color: white;\n"
"")
        self.lineEdit.setMaxLength(30)
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(150, 222, 21, 20))
        self.label.setStyleSheet("background: transparent")
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("./Public/2.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(610, 216, 34, 33))
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton.setStyleSheet("background: transparent")
        self.pushButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./Public/x.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QtCore.QSize(34, 33))
        self.pushButton.setObjectName("pushButton")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(322, 40, 140, 93))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("./Public/1.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(200, 130, 401, 54))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(36)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: #1FDF64")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(351, 423, 101, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: white;")
        self.label_4.setObjectName("label_4")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Spotify Download"))
        self.label_3.setText(_translate("MainWindow", "Spotify Download"))
        self.label_4.setText(_translate("MainWindow", "Versão Beta"))

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.playlist_id = ""
        self.output_directory = DOWNLOAD_MEDIA_PLAY_FOLDER

        self.ui.pushButton.clicked.connect(self.start_download)

    def start_download(self):
        self.playlist_id = self.ui.lineEdit.text()
        self.download_thread = DownloadThread(self.playlist_id, self.output_directory)
        self.download_thread.download_finished.connect(self.download_finished)
        self.download_thread.start()

    def download_finished(self):
        print("Download concluído.")

def download_spotify_playlist_tracks(playlist_id, output_directory):
    try:
        # Autenticar a aplicação com as credenciais do cliente do Spotify
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id='f164aa7c07fd4eff94be21e9c270b4a0', client_secret='80a776ef99bf453cbd103f1e3ccafec0'))

        # Buscar as faixas na playlist do Spotify
        playlist = sp.playlist_tracks(playlist_id)

        # Iterar sobre as faixas e obter informações
        for track in playlist['items']:
            track_name = track['track']['name']
            artist_name = track['track']['artists'][0]['name']
            track_url = track['track']['external_urls']['spotify']
            
            # Baixar a faixa usando SpotDL
            print(f"Baixando: {track_name} - {artist_name}")
            subprocess.run(["spotdl", track_url, "--output", output_directory])
            
    except Exception as e:
        print(f"Erro ao baixar a playlist do Spotify: {e}")

def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
