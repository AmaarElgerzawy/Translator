import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from threading import Thread
import os
from random import random
import re
from shutil import move, rmtree
from googletrans import Translator, constants

TheRand = round((random()*10000))


class TranslatorClass(QDialog):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("Translator")
    self.setWindowIcon(QIcon("C:\Windows\System32\@language_notification_icon.png"))
    self.setWindowIconText("Translator")

    self.MainLayout = QVBoxLayout()

    #region MainLayout ThePath

    self.H_Path = QHBoxLayout()

    self.pathLabel = QLabel("Prime Path : ")
    self.pathlineEdit = QLineEdit()

    self.H_Path.addWidget(self.pathLabel)
    self.H_Path.addWidget(self.pathlineEdit)

    #endregion

    #region MainLayout TheBackUp
    self.H_BacKUp = QHBoxLayout()

    self.backUplabel = QLabel("BackUp Path : ")
    self.backUplineEdit = QLineEdit()

    self.H_BacKUp.addWidget(self.backUplabel)
    self.H_BacKUp.addWidget(self.backUplineEdit)
    #endregion

    #region MainLayout radioBuutons
    self.H_radio = QHBoxLayout()

    self.oneFile = QRadioButton("One File")
    self.onlyPath = QRadioButton("Only Path")
    self.fullPath = QRadioButton("Full Path")

    self.H_radio.addWidget(self.oneFile)
    self.H_radio.addWidget(self.onlyPath)
    self.H_radio.addWidget(self.fullPath)
    #endregion

    #region MainLayout comboBoxs
    self.H_ComboBox = QHBoxLayout()

    self.FromLabel = QLabel("From:")
    self.FromCompo = QComboBox()
    self.FromCompo.addItems(constants.LANGUAGES.keys())
    self.FromCompo.setCurrentText("en")

    self.ToLabel = QLabel("To:")
    self.ToCompo = QComboBox()
    self.ToCompo.addItems(constants.LANGUAGES.keys())
    self.ToCompo.setCurrentText("ar")

    self.H_ComboBox.addWidget(self.FromLabel)
    self.H_ComboBox.addWidget(self.FromCompo)
    self.H_ComboBox.addWidget(self.ToLabel)
    self.H_ComboBox.addWidget(self.ToCompo)
    #endregion

    #region MainLayout Button
    self.H_btns = QHBoxLayout()

    self.startBtn = QPushButton("Start")

    self.t = Thread(target=self.startConnection)
    self.startBtn.clicked.connect(self.t.start)

    self.H_btns.addWidget(self.startBtn)
    #endregion

    #region MainLayout Adding
    self.MainLayout.addLayout(self.H_Path)
    self.MainLayout.addLayout(self.H_BacKUp)
    self.MainLayout.addLayout(self.H_radio)
    self.MainLayout.addLayout(self.H_ComboBox)
    self.MainLayout.addLayout(self.H_btns)
    #endregion

    self.setLayout(self.MainLayout)

  def startConnection(self):
    widget.setCurrentIndex(widget.currentIndex()+1)

    path = self.pathlineEdit.text()
    dest = self.FromCompo.currentText()
    src = self.ToCompo.currentText()
    type = ""
    if self.oneFile.isChecked():
      type = "file"
    elif self.onlyPath.isChecked():
      type = "path"
    elif self.fullPath.isChecked():
      type = "full"
    else:
      HandlingErrors()

    Connection(path, type, src, dest)

class Loading(QDialog):
  def __init__(self) -> None:
    super().__init__()
    self.setGeometry(super().geometry())

    self.LoadingLayout = QVBoxLayout()

    self.total = QLabel("Their is 0 Files Left...")
    self.total.setStyleSheet('''
    font-family: sans-serif;
    font-size:18px;
    color: green;
    ''')

    self.currentFile = QLabel("Translate...")
    self.currentFile.setMaximumWidth(50)
    self.currentFile.setStyleSheet('''
    font-family: sans-serif;
    font-size:10px;
    color: green;
    ''')

    self.CopyRight = QLabel("Made By @Ammar_Elgerzawy")
    self.CopyRight.setStyleSheet('''
    font-family: sans-serif;
    font-size:10px;
    color: red;
    font-weight : Bold;
    margin : 0px auto;
    ''')

    self.prog_bar = QProgressBar()
    self.prog_bar.setValue(0)

    self.prog_bar_det = QProgressBar()
    self.prog_bar_det.setValue(0)
    
    self.LoadingLayout.addWidget(self.total)
    self.LoadingLayout.addWidget(self.prog_bar)
    self.LoadingLayout.addWidget(self.currentFile)
    self.LoadingLayout.addWidget(self.prog_bar_det)
    self.LoadingLayout.addWidget(self.CopyRight)

    self.setLayout(self.LoadingLayout)

  def ControllLepal(self, name, total):
    self.total.setText(f"There is {total} Files Left")
    self.currentFile.setText(f"Translate...{name}")

  def ControllBar(self, progress):
    self.prog_bar.setValue(self.prog_bar.value() + round(progress))
    self.prog_bar.setValue(0)

  def ControllDetBar(self , prog):
    self.prog_bar.setValue(self.prog_bar.value() + round(prog))

class Core():
  def __init__(self) -> None:
      global TheRand
      self.random = TheRand

  def MainCore(self, translateThat, From, To, name, total, progrss):
    LoadWindow.ControllLepal(name, total)
    self.TheFile = open(translateThat, "r", encoding="utf8")
    self.file = self.TheFile.readlines()
    self.strings, self.timing = self.classification_filtring()
    self.translated = self.translate_strings(From, To)
    self.make_translated_file(name, progrss)

  def classification_filtring(self):
    strings, timing = [], []
    for i in self.file:
      if re.search("\d+", i) and len(i) < 5:
        continue
      elif re.search("\d\d:\d\d:\d\d", i):
        timing.append(i[:-1])
      else:
        if i != "\n":
          if i[-1] == "\n":
            strings.append(i[:-1])
          else:
            strings.append(i)
    return self.merging(strings, timing)

  def merging(self, strings, timing):
    pointer = len(strings) - 2
    while pointer >= 0:
      if not strings[pointer].endswith("."):
        strings[pointer] += strings[pointer+1]
        timing[pointer] = timing[pointer].split("-->")[0] + "-->" + timing[pointer-1].split("-->")[1]

        strings.remove(strings[pointer+1])
        timing.remove(timing[pointer+1])
      pointer -= 1
    return strings, timing

  def translate_strings(self, From, To):
    translator = Translator()
    translated = []
    p = 100 / len(self.strings)
    try:
      for string in self.strings:
        translated.append(translator.translate(string, src=From, dest=To).text)
        LoadWindow.ControllDetBar(p)
      return translated
    except:
      HandlingErrors()

  def make_translated_file(self, name, progrss):
    try:
      os.mkdir(f"C:/Translated{self.random}")
    except:
      ...
    finalFile = open(f"C:/Translated{self.random}/{name}.srt", "a", encoding="utf16")
    i = 0
    while i < len(self.strings):
      finalFile.write(f"{i+1}\n{self.timing[i]}\n{self.translated[i]}\n\n")
      i += 1
    return LoadWindow.ControllBar(progrss)


class Connection():
  def __init__(self, path, type, dest, src) -> None:
    global TheRand
    self.random = TheRand

    #region Variables
    self.path = path
    self.dest = dest
    self.src = src
    self.FilesWithPaths = []
    self.names = []
    self.foldersName = []
    #endregion

    if type == "file":
      self.oneFile()
    elif type == "path":
      self.onlyPath()
    elif type == "full":
      self.fullPath()
    else:
      HandlingErrors()

  def getSrt(self, path):
      """this function to get srt from given path
      use reguler exp to set none on un srt file then clear nons with filter then get the name with map"""
      return list(map(lambda b: b.string, filter(lambda a: a != None, [re.search(".+srt", string) for string in os.listdir(path)])))

  def fetching(self, primePath):
    i = 0
    for i in os.listdir(primePath):
      i += 1
      if os.path.isdir(f"{primePath}/{i}"):
        self.fetching(f"{primePath}/{i}")
      else:
        if i.endswith(".srt"):
          self.foldersName.append(primePath.removesuffix(self.path))
          self.FilesWithPaths.append(f"{primePath}/{i}")
          self.names.append(i)
    return i

  def oneFile(self):
    Core().MainCore(translateThat=self.path, From=self.src, To=self.dest, name=re.split(r"(/|\\)", self.path)[-1][:-4], total=1, progrss=100)
    self.moving(re.split(r"(/|\\)", self.path)[-1], 0)

  def onlyPath(self):
    theCore = Core()
    the_self_path = self.getSrt(self.path)
    l = len(the_self_path)
    p = 100/l
    for file in the_self_path:
      theCore.MainCore(f"{self.path}/{file}", From=self.src, To=self.dest, name=re.split(r"(/|\\)", file)[-1][:-4], total=l, progrss=p)
      self.moving(file, 1)
      l -= 1

  def fullPath(self):
    theCore = Core()
    l = self.fetching(self.path)
    p = 100/l
    for f, n, fn in zip(self.FilesWithPaths, self.names, self.foldersName):
      theCore.MainCore(f, From=self.src, To=self.dest, name=re.split(r"(/|\\)", n)[-1][:-4], total=l, progrss=p)
      self.moving([n, fn], 2)
      l -= 1

  def moving(self, name, funcFrom):
      TranslateFolder = f"C:/Translated{self.random}"
      if funcFrom == 0:
          try:
              os.mkdir(self.path[:-len(name)]+"/backUp")
          except:
            ...
          try:
              move(self.path, self.path[:-len(name)]+"/backUp/"+name)
          except:
            ...
          move(f"{TranslateFolder}/{name}", f"{self.path}")
      elif funcFrom == 1:
          try:
              os.mkdir(self.path+"/backUp")
          except:
            ...
          try:
              move(f"{self.path}/{name}", f"{self.path}/backUp/{name}")
          except:
            ...
          move(f"{TranslateFolder}/{name}", f"{self.path}/{name}")
      elif funcFrom == 2:
          try:
              os.makedirs(f"{self.path}/{name[1]}/backUp")
          except:
            ...
          try:
              move(f"{self.path}/{name[1]}/{name[0]}", f"{self.path}/{name[1]}/backUp/{name[0]}")
          except:
            ...
          move(f"{TranslateFolder}/{name[0]}", f"{name[1]}/{name[0]}")
      else:
        ...
      rmtree(TranslateFolder)


class HandlingErrors():
  def __init__(self) -> None:
    print("error")


app = QApplication([])

widget = QStackedWidget()

mainWindow = TranslatorClass()
LoadWindow = Loading()

widget.addWidget(mainWindow)
widget.addWidget(LoadWindow)

widget.show()

sys.exit(app.exec())
