import time
from PyQt5 import QtCore, QtGui, QtWidgets
import os
import subprocess
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

DOWNLOADS_FOLDER = os.path.join(os.path.expanduser('~'), 'Downloads')
DOWNLOAD_MEDIA_PLAY_FOLDER = os.path.join(DOWNLOADS_FOLDER, 'Músicas')

if not os.path.exists(DOWNLOAD_MEDIA_PLAY_FOLDER):
    os.makedirs(DOWNLOAD_MEDIA_PLAY_FOLDER)

class DownloadThread(QtCore.QThread):
    progress_updated = QtCore.pyqtSignal(str, int, QtGui.QPixmap)
    download_finished = QtCore.pyqtSignal()

    def __init__(self, playlist_id, output_directory):
        super().__init__()
        self.playlist_id = playlist_id
        self.output_directory = output_directory
        self.failed_tracks = []  

    def run(self):
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id='f164aa7c07fd4eff94be21e9c270b4a0', client_secret='80a776ef99bf453cbd103f1e3ccafec0'))
        playlist = sp.playlist_tracks(self.playlist_id)
        total_tracks = len(playlist['items'])

        for i, track in enumerate(playlist['items']):
            track_name = track['track']['name']
            artist_name = track['track']['artists'][0]['name']
            track_url = track['track']['external_urls']['spotify']
            album_cover_url = track['track']['album']['images'][0]['url']
            album_cover_pixmap = QtGui.QPixmap()
            album_cover_pixmap.loadFromData(sp._get(album_cover_url))

            print(f"Baixando: {track_name} - {artist_name}")
            try:
                subprocess.run(["spotdl", track_url, "--output", self.output_directory], check=True)
            except subprocess.CalledProcessError:
                self.failed_tracks.append(f"{track_name} - {artist_name}")
                print(f"Erro ao baixar: {track_name} - {artist_name}")

            progress_percentage = int(((i + 1) / total_tracks) * 100)
            self.progress_updated.emit(f"✔ {track_name} - {artist_name}", progress_percentage, album_cover_pixmap)
        
        if self.failed_tracks:
            failed_tracks_file = os.path.join(self.output_directory, 'failed_tracks.txt')
            with open(failed_tracks_file, 'w') as file:
                file.write("Músicas que não foram baixadas:\n")
                for track in self.failed_tracks:
                    file.write(f"{track}\n")

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
        self.lineEdit.setMaxLength(100)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setPlaceholderText('https://open.spotify.com/playlist/3DrQOdOEaGrh1iYJKQZ52T')
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

        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(138, 260, 507, 23))
        self.progressBar.setStyleSheet("QProgressBar {\n"
                                       "    border: 0px solid grey;\n"
                                       "    border-radius: 10px;\n"
                                       "    background: #404040;\n"
                                       "    color: #404040;"
                                       "    text-align: center;"
                                       "}\n"
                                       "QProgressBar::chunk {\n"
                                       "    background: #1FDF64;\n"
                                       "    width: 20px;\n"
                                       "    border-radius: 5px;"
                                       "}")
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")

        self.statusLabel = QtWidgets.QLabel(self.centralwidget)
        self.statusLabel.setGeometry(QtCore.QRect(138, 290, 507, 23))
        self.statusLabel.setFont(font)
        self.statusLabel.setStyleSheet("color: white;")
        self.statusLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.statusLabel.setObjectName("statusLabel")

        self.albumCoverLabel = QtWidgets.QLabel(self.centralwidget)
        self.albumCoverLabel.setGeometry(QtCore.QRect(322, 320, 140, 140))
        self.albumCoverLabel.setStyleSheet("background: transparent")
        self.albumCoverLabel.setScaledContents(True)
        self.albumCoverLabel.setObjectName("albumCoverLabel")

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
        input_text = self.ui.lineEdit.text()
        self.playlist_id = extract_playlist_id(input_text)
        self.download_thread = DownloadThread(self.playlist_id, self.output_directory)
        self.download_thread.progress_updated.connect(self.update_progress)
        self.download_thread.download_finished.connect(self.download_finished)
        self.download_thread.start()

    def update_progress(self, status, progress, album_cover_pixmap):
        self.ui.statusLabel.setText(status)
        self.ui.progressBar.setValue(progress)
        self.ui.albumCoverLabel.setPixmap(album_cover_pixmap)

    def download_finished(self):
        self.ui.statusLabel.setText("Download concluído.")
        self.ui.progressBar.setValue(100)

#Extraindo ID da URL da Playlist do Spotify

def extract_playlist_id(url_or_id):
    if "spotify.com/playlist/" in url_or_id:
        return url_or_id.split("spotify.com/playlist/")[1].split("?")[0]
    return url_or_id

def download_spotify_playlist_tracks(playlist_id, output_directory):
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id='f164aa7c07fd4eff94be21e9c270b4a0', client_secret='80a776ef99bf453cbd103f1e3ccafec0'))
        playlist = sp.playlist_tracks(playlist_id)
        total_tracks = len(playlist['items'])
        failed_tracks = []

        for i, track in enumerate(playlist['items']):
            track_name = track['track']['name']
            artist_name = track['track']['artists'][0]['name']
            track_url = track['track']['external_urls']['spotify']

            print(f"Baixando: {track_name} - {artist_name}")
            try:
                subprocess.run(["spotdl", track_url, "--output", output_directory], check=True)
            except subprocess.CalledProcessError:
                failed_tracks.append(f"{track_name} - {artist_name}")
                print(f"Erro ao baixar: {track_name} - {artist_name}")

            progress_percentage = int(((i + 1) / total_tracks) * 100)
            time.sleep(1)
            DownloadThread.progress_updated.emit(f"✔ {track_name} - {artist_name}", progress_percentage)
        
        if failed_tracks:
            failed_tracks_file = os.path.join(output_directory, 'failed_tracks.txt')
            with open(failed_tracks_file, 'w') as file:
                file.write("Músicas que não foram baixadas:\n")
                for track in failed_tracks:
                    file.write(f"{track}\n")

        DownloadThread.download_finished.emit()

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
