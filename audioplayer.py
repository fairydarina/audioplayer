import sys
import random
from PyQt5 import uic, QtMultimedia, QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QFileDialog, QListView, QLabel, QSlider
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *

class MyAudioPlayer(QMainWindow):
    # Интерфейс был создан в designer
    # Затем он был сконвертирован в код 
    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(403, 380)
        
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        
        # Кнопка при нажатии которой начинает играть музыка
        self.pushButtonPlay = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonPlay.setGeometry(QtCore.QRect(100, 270, 75, 23))
        self.pushButtonPlay.setObjectName("pushButtonPlay")
        
        # Кнопка при нажатии которой музыка перестает играть
        self.pushButtonPause = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonPause.setGeometry(QtCore.QRect(180, 270, 75, 23))
        self.pushButtonPause.setObjectName("pushButtonPause")
        
        # label с помощью которого выводится трек, играющий в данный момент
        self.labelCurrentTrack = QtWidgets.QLabel(self.centralwidget)
        self.labelCurrentTrack.setGeometry(QtCore.QRect(40, 210, 281, 16))
        self.labelCurrentTrack.setObjectName("labelCurrentTrack")
        
        # Кнопка при нажатии которой играет следущая песня
        self.pushButtonNextSong = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonNextSong.setGeometry(QtCore.QRect(260, 270, 75, 23))
        self.pushButtonNextSong.setObjectName("pushButtonNextSong")
        
        # Кнопка при нажатии которой играет предыдущая песня
        self.pushButtonPrevSong = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonPrevSong.setGeometry(QtCore.QRect(20, 270, 75, 23))
        self.pushButtonPrevSong.setObjectName("pushButtonPrevSong")
        
        # Кнопка при нажатии которой добавляется выбраная вами песня/песни
        self.pushButtonAddSong = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonAddSong.setGeometry(QtCore.QRect(360, 30, 31, 23))
        self.pushButtonAddSong.setObjectName("pushButtonAddSong")
        
        # Кнопка при нажатии которой удаляется выбраная вами песня
        self.pushButtonDelSong = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonDelSong.setGeometry(QtCore.QRect(360, 60, 31, 23))
        self.pushButtonDelSong.setObjectName("pushButtonDelSong")
        
        # Перемещивание песен
        self.pushButtonRandom = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonRandom.setGeometry(QtCore.QRect(360, 90, 31, 23))
        self.pushButtonRandom.setObjectName("pushButtonRandom")
        
        # Экран на котором выводится список песен
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(10, 10, 341, 192))
        self.listWidget.setObjectName("listWidget")
        
        # Слайдер на котором отображается где играет песня 
        self.hSliderPos = QtWidgets.QSlider(self.centralwidget)
        self.hSliderPos.setGeometry(QtCore.QRect(10, 230, 331, 22))
        self.hSliderPos.setOrientation(QtCore.Qt.Horizontal)
        self.hSliderPos.setObjectName("hSliderPos")
        
        # Слайдер громкости
        self.hSliderVolume = QtWidgets.QSlider(self.centralwidget)
        self.hSliderVolume.setGeometry(QtCore.QRect(100, 310, 160, 22))
        self.hSliderVolume.setProperty("value", 50)
        self.hSliderVolume.setOrientation(QtCore.Qt.Horizontal)
        self.hSliderVolume.setObjectName("hSliderVolume")
        
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 310, 71, 21))
        self.label.setObjectName("label")
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 403, 21))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButtonPlay.setText(_translate("MainWindow", ">"))
        self.pushButtonPause.setText(_translate("MainWindow", "||"))
        self.labelCurrentTrack.setText(_translate("MainWindow", "TextLabel"))
        self.pushButtonNextSong.setText(_translate("MainWindow", ">>"))
        self.pushButtonPrevSong.setText(_translate("MainWindow", "<<"))
        self.pushButtonAddSong.setText(_translate("MainWindow", "+"))
        self.pushButtonDelSong.setText(_translate("MainWindow", "-"))
        self.pushButtonRandom.setText(_translate("MainWindow", "Rnd"))
        self.label.setText(_translate("MainWindow", "Громкость"))
    
    
    def __init__(self):
        super().__init__()
        self.setupUi()
        self.initUI()
        
        # При нажатии кнопок срабатывают функции
        # Функции находятся ниже
        self.pushButtonAddSong.clicked.connect(self.addSong)
        self.pushButtonDelSong.clicked.connect(self.delSong)
        self.pushButtonRandom.clicked.connect(self.rndSongs)
        self.pushButtonPlay.clicked.connect(self.playSong)
        self.pushButtonPause.clicked.connect(self.pauseSong)
        self.pushButtonPrevSong.clicked.connect(self.prevBtn)
        self.pushButtonNextSong.clicked.connect(self.nextBtn)        
        self.hSliderVolume.valueChanged[int].connect(self.changeValue)
        self.hSliderPos.valueChanged.connect(self.mpPlayer.setPosition)
        self.mpPlayer.positionChanged.connect(self.hSliderPos.setValue)
        self.listWidget.itemClicked.connect(self.listWidgetClicked)        
        self.labelCurrentTrack.setText('')
        
    def initUI(self):
        self.setWindowTitle('audioplayer')
        
        self.mpPlayer = QtMultimedia.QMediaPlayer()
        self.mpPlayer.setVolume(50)
        
        self.show()
    
    # Функция которая перемешивает песни
    def rndSongs(self):
        lst = []
        # Выгрузка песен в список
        for i in range(self.listWidget.count()):
            lst.append(self.listWidget.item(i).text())
        
        self.listWidget.clear()
        
        # Рандомное перемешивание треков
        while len(lst) > 0:
            p = lst.pop(random.randint(0, len(lst) - 1))
            self.listWidget.addItem(p)
            
        self.setCurrentTrack()

    # Получение текущего трека
    def setCurrentTrack(self):
        if self.listWidget.count() > 0:
            it = self.listWidget.item(0)
            self.listWidget.setCurrentItem(it)
            self.sound = QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(it.text()))
            self.mpPlayer.setMedia(self.sound)
            self.labelCurrentTrack.setText(it.text())

    # При щелчке мышью на трек он начинает играть
    def listWidgetClicked(self, q):
        self.labelCurrentTrack.setText(q.text())
        self.sound = QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(q.text()))
        self.mpPlayer.setMedia(self.sound)
        self.hSliderPos.valueChanged.connect(self.mpPlayer.setPosition)
        self.playSong()
        
    
    # Добавление в плейлист песни/песен
    def addSong(self):
        # Проверка, что файлы в mp3 формате
        fname = QFileDialog.getOpenFileNames(self, 'Open file', '', "MP3 (*.mp3)")
        for i in fname[0]:
            # Проверка, что песня/песни раньше не добавлялись 
            if self.findTrackIndex(i) == None:
                self.listWidget.addItem(i)
        self.setCurrentTrack()
    
    # Удаление выбранной песни           
    def delSong(self):
        # Останавливаем песню
        self.mpPlayer.stop()
        listItems = self.listWidget.selectedItems()
        if not listItems: return        
        for item in listItems:
            # Удаление
            self.listWidget.takeItem(self.listWidget.row(item))
            
        self.setCurrentTrack()
      
    # Функция для прогрывания песни  
    def playSong(self):
        self.mpPlayer.play()
        # методы для получения места для слайдера 
        self.hSliderPos.setMinimum(0)
        self.hSliderPos.setMaximum(self.mpPlayer.duration())
    
    # Функция для остановки песни  
    def pauseSong(self):
        self.mpPlayer.pause()
    
    # Громкость    
    def changeValue(self, value):
        self.mpPlayer.setVolume(value)
     
    # Кнопка которая ставит предыдущий трек   
    def prevBtn(self):
        # Текущая песня
        currentTrack = self.labelCurrentTrack.text()
        currentTrackIndex = self.findTrackIndex(currentTrack)
        # Если трек стоит первым, то ничего не делаем
        if currentTrackIndex == 0:
            return
        currentTrackIndex = currentTrackIndex - 1
        # Получение индекса песни
        currentTrack = self.getTrackFromIndex(currentTrackIndex)
        self.labelCurrentTrack.setText(currentTrack)
        it = self.listWidget.item(currentTrackIndex)
        self.listWidget.setCurrentItem(it)
        self.listWidgetClicked(it)
    
    # Кнопка которая ставит следующий трек 
    def nextBtn(self):
        # Текущая песня
        currentTrack = self.labelCurrentTrack.text()
        currentTrackIndex = self.findTrackIndex(currentTrack)
        # Если трек стоит последним, то ничего не делаем
        if currentTrackIndex == self.getTrackCount() - 1:
            return
        # Прибавляем к индексу текущей песни 1
        currentTrackIndex = currentTrackIndex + 1
        currentTrack = self.getTrackFromIndex(currentTrackIndex)
        self.labelCurrentTrack.setText(currentTrack)
        it = self.listWidget.item(currentTrackIndex)
        self.listWidget.setCurrentItem(it)
        self.listWidgetClicked(it)
    
    # Получение трека через индекс    
    def getTrackFromIndex(self, index):
        return self.listWidget.item(index).text()
     
    # Поиск трека   
    def findTrackIndex(self, trackName):
        for i in range(self.getTrackCount()):
            if self.listWidget.item(i).text() == trackName:
                return i
        # Если не находим возращаем None
        return None
    
    # Полученик кол-ва треков
    def getTrackCount(self):
        return self.listWidget.count()
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyAudioPlayer()
    sys.exit(app.exec_())