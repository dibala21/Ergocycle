"""
Created on Wed Feb 23 17:20:00 2022

@author: Frédérique Leclerc
"""
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import QTimer, QTime
from PIL import Image
#from Stimulator import Stimulator
import time
import numpy
from numpy import *
#from Parameters import Parameters
#import sys

SCREEN_WIDTH = 1920
SCREEN_HEIGTH = 1080
MAX_AMPLITUDE = 130
MIN_AMPLITUDE = 0
MAX_FREQ = 50
MIN_FREQ = 0
MAX_IMP = 500
MIN_IMP = 0

class StimulationWindow(QWidget):
    def __init__(self, init_parameters):
        super(StimulationWindow, self).__init__()
        ### 1.1. Instaurer la taille, la couleur de fond et le titre du de la fenêtre des instructions ###
        self.setGeometry(100, 50, SCREEN_WIDTH/1.2, SCREEN_HEIGTH/1.15)
        self.setWindowTitle("Menu des stimulations")
        self.setStyleSheet("background-color: white;")
        current_parameters = init_parameters
        self.initUI(current_parameters)
    def initUI(self, current_parameters):  
        ### 1.3. Mettre le logo du laboratoire dans le coin gauche de la fenêtre ###
        self.imageS2M = Image.open("img_S2M_JPG.jpg")
        self.petite_imageS2M = self.imageS2M.resize((200, 150))
        self.petite_imageS2M.save('image_400.jpg')
        self.logo_label = QtWidgets.QLabel(self)
        self.logo_jpg = QPixmap('image_400.jpg') # Modifier la taille de l'image au besoin
        self.logo_label.setPixmap(self.logo_jpg)
        self.logo_label.resize(self.logo_jpg.width(), self.logo_jpg.height())
        ### 1.4. Titre menu des instructions ###
        self.menu_label = QtWidgets.QLabel(self)
        self.menu_label.setText("Stimulations en cours...")
        self.menu_label.move(650,100)
        self.menu_label.setFont(QFont('Arial', 20, weight = QFont.Bold))
        self.menu_label.adjustSize()
        ### 1.5. Bouton d'arrêt ##
        self.stop_button = QtWidgets.QPushButton(self)
        self.stop_button.setText("  Arrêter  ")
        self.stop_button.setStyleSheet("background-color: red; border: 2 solid;")
        self.stop_button.move(1300, 50)
        self.stop_button.setFont(QFont('Arial', 20, weight = QFont.Bold))
        self.stop_button.adjustSize()
        self.stop_button.clicked.connect(lambda:self.clicked_stop()) 
        ### 1.6. ###
        #self.end_of_stim = False
        ### 1.7. Nouvelle méthode pour le timer ###
        self.counter = 0
        self.minute = '00'
        self.second = '00'
        self.count = '00'
        self.MAX_TIME = int(current_parameters.get_stim_training_length())
        self.time_label = QLabel(self)
        self.time_label.setGeometry(750, 175, 150, 70)
        self.startWatch = True
        # Bouton pause du timer 
        self.pauseWatch = QPushButton("Pause", self)
        self.pauseWatch.setGeometry(900, 187, 100, 40)
        self.pauseWatch.setStyleSheet("background-color: palegreen; border: 2 solid;")
        self.pauseWatch.setFont(QFont('Arial', 12))
        self.pauseWatch.pressed.connect(self.pause)
        # objet timer
        timer = QTimer(self)
        timer.timeout.connect(self.showCounter)
        timer.start(100)
        ### 1.8. Layout des labels de la fenêtre de stimulation ###
        self.amplitude_label = QtWidgets.QLabel(self)
        self.amplitude_label.setText("Amplitude (mA):")
        self.amplitude_label.move(400,300)
        self.amplitude_label.setFont(QFont('Arial', 12))
        self.amplitude_label.adjustSize()

        self.frequency_label = QtWidgets.QLabel(self)
        self.frequency_label.setText("Fréquence (Hz):")
        self.frequency_label.move(800,300)
        self.frequency_label.setFont(QFont('Arial', 12))
        self.frequency_label.adjustSize()

        self.length_imp_label = QtWidgets.QLabel(self)
        self.length_imp_label.setText("Durée d'impulsion (μs):")
        self.length_imp_label.move(1200,(300))
        self.length_imp_label.setFont(QFont('Arial', 12))
        self.length_imp_label.adjustSize()
        ### 1.7. Label d'électrode ##
        self.electrode1_label = QtWidgets.QLabel(self)
        self.electrode1_label.setText("Électrode 1 (droite):")
        self.electrode1_label.move(75,375)
        self.electrode1_label.setFont(QFont('Arial', 12))
        self.electrode1_label.adjustSize()

        self.electrode2_label = QtWidgets.QLabel(self)
        self.electrode2_label.setText("Électrode 2 (droite):")
        self.electrode2_label.move(75,450)
        self.electrode2_label.setFont(QFont('Arial', 12))
        self.electrode2_label.adjustSize()

        self.electrode3_label = QtWidgets.QLabel(self)
        self.electrode3_label.setText("Électrode 3 (droite):")
        self.electrode3_label.move(75,525)
        self.electrode3_label.setFont(QFont('Arial', 12))
        self.electrode3_label.adjustSize()

        self.electrode4_label = QtWidgets.QLabel(self)
        self.electrode4_label.setText("Électrode 4 (droite):")
        self.electrode4_label.move(75,600)
        self.electrode4_label.setFont(QFont('Arial', 12))
        self.electrode4_label.adjustSize()

        self.electrode5_label = QtWidgets.QLabel(self)
        self.electrode5_label.setText("Électrode 5 (gauche):")
        self.electrode5_label.move(75,675)
        self.electrode5_label.setFont(QFont('Arial', 12))
        self.electrode5_label.adjustSize()

        self.electrode6_label = QtWidgets.QLabel(self)
        self.electrode6_label.setText("Électrode 6 (gauche):")
        self.electrode6_label.move(75,750)
        self.electrode6_label.setFont(QFont('Arial', 12))
        self.electrode6_label.adjustSize()

        self.electrode7_label = QtWidgets.QLabel(self)
        self.electrode7_label.setText("Électrode 7 (gauche):")
        self.electrode7_label.move(75,825)
        self.electrode7_label.setFont(QFont('Arial', 12))
        self.electrode7_label.adjustSize()

        self.electrode8_label = QtWidgets.QLabel(self)
        self.electrode8_label.setText("Électrode 8 (gauche):")
        self.electrode8_label.move(75,900)
        self.electrode8_label.setFont(QFont('Arial', 12))
        self.electrode8_label.adjustSize()
        #print("Amplitudes enregistrées: ", current_parameters.get_electrode1_amplitude(),  current_parameters.get_electrode2_amplitude(),  current_parameters.get_electrode3_amplitude(),  current_parameters.get_electrode4_amplitude(),  current_parameters.get_electrode5_amplitude(), current_parameters.get_electrode6_amplitude(),  current_parameters.get_electrode7_amplitude(),  current_parameters.get_electrode8_amplitude())
        #print("Fréquences enregistrées: ", init_parameters.get_electrode1_frequency(),  init_parameters.get_electrode2_frequency(),  init_parameters.get_electrode3_frequency(),  init_parameters.get_electrode4_frequency(),  init_parameters.get_electrode5_frequency(), init_parameters.get_electrode6_frequency(),  init_parameters.get_electrode7_frequency(),  init_parameters.get_electrode8_frequency())
        #print("Durées d'imp enregistrées: ", init_parameters.get_electrode1_length_imp(),  init_parameters.get_electrode2_length_imp(),  init_parameters.get_electrode3_length_imp(),  init_parameters.get_electrode4_length_imp(),  init_parameters.get_electrode5_length_imp(), init_parameters.get_electrode6_length_imp(),  init_parameters.get_electrode7_length_imp(),  init_parameters.get_electrode8_length_imp())
        
        ### 1.8. Placer toutes les amplitudes selon l'électrode ###
        self.current_amplitude1_label = QtWidgets.QLabel(self)
        self.current_amplitude1_label.setText(str(current_parameters.get_electrode1_amplitude()))
        self.current_amplitude1_label.move(450,375)
        self.current_amplitude1_label.setFont(QFont('Arial', 12))
        self.current_amplitude1_label.adjustSize()

        self.current_amplitude2_label = QtWidgets.QLabel(self)
        self.current_amplitude2_label.setText(str(current_parameters.get_electrode2_amplitude()))
        self.current_amplitude2_label.move(450,450)
        self.current_amplitude2_label.setFont(QFont('Arial', 12))
        self.current_amplitude2_label.adjustSize()

        self.current_amplitude3_label = QtWidgets.QLabel(self)
        self.current_amplitude3_label.setText(str(current_parameters.get_electrode3_amplitude()))
        self.current_amplitude3_label.move(450,525)
        self.current_amplitude3_label.setFont(QFont('Arial', 12))
        self.current_amplitude3_label.adjustSize()

        self.current_amplitude4_label = QtWidgets.QLabel(self)
        self.current_amplitude4_label.setText(str(current_parameters.get_electrode4_amplitude()))
        self.current_amplitude4_label.move(450,600)
        self.current_amplitude4_label.setFont(QFont('Arial', 12))
        self.current_amplitude4_label.adjustSize()

        self.current_amplitude5_label = QtWidgets.QLabel(self)
        self.current_amplitude5_label.setText(str(current_parameters.get_electrode5_amplitude()))
        self.current_amplitude5_label.move(450,675)
        self.current_amplitude5_label.setFont(QFont('Arial', 12))
        self.current_amplitude5_label.adjustSize()

        self.current_amplitude6_label = QtWidgets.QLabel(self)
        self.current_amplitude6_label.setText(str(current_parameters.get_electrode6_amplitude()))
        self.current_amplitude6_label.move(450,750)
        self.current_amplitude6_label.setFont(QFont('Arial', 12))
        self.current_amplitude6_label.adjustSize()

        self.current_amplitude7_label = QtWidgets.QLabel(self)
        self.current_amplitude7_label.setText(str(current_parameters.get_electrode7_amplitude()))
        self.current_amplitude7_label.move(450,825)
        self.current_amplitude7_label.setFont(QFont('Arial', 12))
        self.current_amplitude7_label.adjustSize()

        self.current_amplitude8_label = QtWidgets.QLabel(self)
        self.current_amplitude8_label.setText(str(current_parameters.get_electrode8_amplitude()))
        self.current_amplitude8_label.move(450,900)
        self.current_amplitude8_label.setFont(QFont('Arial', 12))
        self.current_amplitude8_label.adjustSize()

        ### 1.9. Placer toutes les fréquences selon l'électrode ###
        self.current_frequency1_label = QtWidgets.QLabel(self)
        self.current_frequency1_label.setText(str(current_parameters.get_electrode1_frequency()))
        self.current_frequency1_label.move(850,375)
        self.current_frequency1_label.setFont(QFont('Arial', 12))
        self.current_frequency1_label.adjustSize()

        self.current_frequency2_label = QtWidgets.QLabel(self)
        self.current_frequency2_label.setText(str(current_parameters.get_electrode2_frequency()))
        self.current_frequency2_label.move(850,450)
        self.current_frequency2_label.setFont(QFont('Arial', 12))
        self.current_frequency2_label.adjustSize()

        self.current_frequency3_label = QtWidgets.QLabel(self)
        self.current_frequency3_label.setText(str(current_parameters.get_electrode3_frequency()))
        self.current_frequency3_label.move(850,525)
        self.current_frequency3_label.setFont(QFont('Arial', 12))
        self.current_frequency3_label.adjustSize()

        self.current_frequency4_label = QtWidgets.QLabel(self)
        self.current_frequency4_label.setText(str(current_parameters.get_electrode4_frequency()))
        self.current_frequency4_label.move(850,600)
        self.current_frequency4_label.setFont(QFont('Arial', 12))
        self.current_frequency4_label.adjustSize()

        self.current_frequency5_label = QtWidgets.QLabel(self)
        self.current_frequency5_label.setText(str(current_parameters.get_electrode5_frequency()))
        self.current_frequency5_label.move(850,675)
        self.current_frequency5_label.setFont(QFont('Arial', 12))
        self.current_frequency5_label.adjustSize()

        self.current_frequency6_label = QtWidgets.QLabel(self)
        self.current_frequency6_label.setText(str(current_parameters.get_electrode6_frequency()))
        self.current_frequency6_label.move(850,750)
        self.current_frequency6_label.setFont(QFont('Arial', 12))
        self.current_frequency6_label.adjustSize()

        self.current_frequency7_label = QtWidgets.QLabel(self)
        self.current_frequency7_label.setText(str(current_parameters.get_electrode7_frequency()))
        self.current_frequency7_label.move(850,825)
        self.current_frequency7_label.setFont(QFont('Arial', 12))
        self.current_frequency7_label.adjustSize()

        self.current_frequency8_label = QtWidgets.QLabel(self)
        self.current_frequency8_label.setText(str(current_parameters.get_electrode8_frequency()))
        self.current_frequency8_label.move(850,900)
        self.current_frequency8_label.setFont(QFont('Arial', 12))
        self.current_frequency8_label.adjustSize()

        ### 1.10. Placer toutes les durée impulsion selon l'électrode ###
        self.current_imp_label1_label = QtWidgets.QLabel(self)
        self.current_imp_label1_label.setText(str(current_parameters.get_electrode1_length_imp()))
        self.current_imp_label1_label.move(1275,375)
        self.current_imp_label1_label.setFont(QFont('Arial', 12))
        self.current_imp_label1_label.adjustSize()

        self.current_imp_label2_label = QtWidgets.QLabel(self)
        self.current_imp_label2_label.setText(str(current_parameters.get_electrode2_length_imp()))
        self.current_imp_label2_label.move(1275,450)
        self.current_imp_label2_label.setFont(QFont('Arial', 12))
        self.current_imp_label2_label.adjustSize()

        self.current_imp_label3_label = QtWidgets.QLabel(self)
        self.current_imp_label3_label.setText(str(current_parameters.get_electrode3_length_imp()))
        self.current_imp_label3_label.move(1275,525)
        self.current_imp_label3_label.setFont(QFont('Arial', 12))
        self.current_imp_label3_label.adjustSize()

        self.current_imp_label4_label = QtWidgets.QLabel(self)
        self.current_imp_label4_label.setText(str(current_parameters.get_electrode4_length_imp()))
        self.current_imp_label4_label.move(1275,600)
        self.current_imp_label4_label.setFont(QFont('Arial', 12))
        self.current_imp_label4_label.adjustSize()

        self.current_imp_label5_label = QtWidgets.QLabel(self)
        self.current_imp_label5_label.setText(str(current_parameters.get_electrode5_length_imp()))
        self.current_imp_label5_label.move(1275,675)
        self.current_imp_label5_label.setFont(QFont('Arial', 12))
        self.current_imp_label5_label.adjustSize()

        self.current_imp_label6_label = QtWidgets.QLabel(self)
        self.current_imp_label6_label.setText(str(current_parameters.get_electrode6_length_imp()))
        self.current_imp_label6_label.move(1275,750)
        self.current_imp_label6_label.setFont(QFont('Arial', 12))
        self.current_imp_label6_label.adjustSize()

        self.current_imp_label7_label = QtWidgets.QLabel(self)
        self.current_imp_label7_label.setText(str(current_parameters.get_electrode7_length_imp()))
        self.current_imp_label7_label.move(1275,825)
        self.current_imp_label7_label.setFont(QFont('Arial', 12))
        self.current_imp_label7_label.adjustSize()

        self.current_imp_label8_label = QtWidgets.QLabel(self)
        self.current_imp_label8_label.setText(str(current_parameters.get_electrode8_length_imp()))
        self.current_imp_label8_label.move(1275,900)
        self.current_imp_label8_label.setFont(QFont('Arial', 12))
        self.current_imp_label8_label.adjustSize()

        ### 1.11 - Mettre les boutons "+" et "-" pour l'amplitude ###
        ### 1.11.1 - "+" pour l'amplitude ###
        self.increase_amplitude1_button = QtWidgets.QPushButton(self)
        self.increase_amplitude2_button = QtWidgets.QPushButton(self)
        self.increase_amplitude3_button = QtWidgets.QPushButton(self)
        self.increase_amplitude4_button = QtWidgets.QPushButton(self)
        self.increase_amplitude5_button = QtWidgets.QPushButton(self)
        self.increase_amplitude6_button = QtWidgets.QPushButton(self)
        self.increase_amplitude7_button = QtWidgets.QPushButton(self)
        self.increase_amplitude8_button = QtWidgets.QPushButton(self)
        self.increase_amplitude1_button.setText(" + ")
        self.increase_amplitude2_button.setText(" + ")
        self.increase_amplitude3_button.setText(" + ")
        self.increase_amplitude4_button.setText(" + ")
        self.increase_amplitude5_button.setText(" + ")
        self.increase_amplitude6_button.setText(" + ")
        self.increase_amplitude7_button.setText(" + ")
        self.increase_amplitude8_button.setText(" + ")
        self.increase_amplitude1_button.move(500, 375)
        self.increase_amplitude2_button.move(500, 450)
        self.increase_amplitude3_button.move(500, 525)
        self.increase_amplitude4_button.move(500, 600)
        self.increase_amplitude5_button.move(500, 675)
        self.increase_amplitude6_button.move(500, 750)
        self.increase_amplitude7_button.move(500, 825)
        self.increase_amplitude8_button.move(500, 900)
        self.increase_amplitude1_button.setFont(QFont('Arial', 14))
        self.increase_amplitude2_button.setFont(QFont('Arial', 14))
        self.increase_amplitude3_button.setFont(QFont('Arial', 14))
        self.increase_amplitude4_button.setFont(QFont('Arial', 14))
        self.increase_amplitude5_button.setFont(QFont('Arial', 14))
        self.increase_amplitude6_button.setFont(QFont('Arial', 14))
        self.increase_amplitude7_button.setFont(QFont('Arial', 14))
        self.increase_amplitude8_button.setFont(QFont('Arial', 14))
        self.increase_amplitude1_button.setStyleSheet("background-color: palegreen; border: 2 solid; border-radius: 1")
        self.increase_amplitude2_button.setStyleSheet("background-color: palegreen; border: 2 solid; border-radius: 1")
        self.increase_amplitude3_button.setStyleSheet("background-color: palegreen; border: 2 solid; border-radius: 1")
        self.increase_amplitude4_button.setStyleSheet("background-color: palegreen; border: 2 solid; border-radius: 1")
        self.increase_amplitude5_button.setStyleSheet("background-color: palegreen; border: 2 solid; border-radius: 1")
        self.increase_amplitude6_button.setStyleSheet("background-color: palegreen; border: 2 solid; border-radius: 1")
        self.increase_amplitude7_button.setStyleSheet("background-color: palegreen; border: 2 solid; border-radius: 1")
        self.increase_amplitude8_button.setStyleSheet("background-color: palegreen; border: 2 solid; border-radius: 1")
        self.increase_amplitude1_button.adjustSize()
        self.increase_amplitude2_button.adjustSize()
        self.increase_amplitude3_button.adjustSize()
        self.increase_amplitude4_button.adjustSize()
        self.increase_amplitude5_button.adjustSize()
        self.increase_amplitude6_button.adjustSize()
        self.increase_amplitude7_button.adjustSize()
        self.increase_amplitude8_button.adjustSize()
        self.increase_amplitude1_button.clicked.connect(lambda:self.increase_amplitude1(current_parameters)) 
        self.increase_amplitude2_button.clicked.connect(lambda:self.increase_amplitude2(current_parameters)) 
        self.increase_amplitude3_button.clicked.connect(lambda:self.increase_amplitude3(current_parameters))
        self.increase_amplitude4_button.clicked.connect(lambda:self.increase_amplitude4(current_parameters))
        self.increase_amplitude5_button.clicked.connect(lambda:self.increase_amplitude5(current_parameters))
        self.increase_amplitude6_button.clicked.connect(lambda:self.increase_amplitude6(current_parameters)) 
        self.increase_amplitude7_button.clicked.connect(lambda:self.increase_amplitude7(current_parameters))
        self.increase_amplitude8_button.clicked.connect(lambda:self.increase_amplitude8(current_parameters))
        ### 1.11.2 - "-" pour l'amplitude ###
        self.decrease_amplitude1_button = QtWidgets.QPushButton(self)
        self.decrease_amplitude2_button = QtWidgets.QPushButton(self)
        self.decrease_amplitude3_button = QtWidgets.QPushButton(self)
        self.decrease_amplitude4_button = QtWidgets.QPushButton(self)
        self.decrease_amplitude5_button = QtWidgets.QPushButton(self)
        self.decrease_amplitude6_button = QtWidgets.QPushButton(self)
        self.decrease_amplitude7_button = QtWidgets.QPushButton(self)
        self.decrease_amplitude8_button = QtWidgets.QPushButton(self)
        self.decrease_amplitude1_button.setText("  - ")
        self.decrease_amplitude2_button.setText("  - ")
        self.decrease_amplitude3_button.setText("  - ")
        self.decrease_amplitude4_button.setText("  - ")
        self.decrease_amplitude5_button.setText("  - ")
        self.decrease_amplitude6_button.setText("  - ")
        self.decrease_amplitude7_button.setText("  - ")
        self.decrease_amplitude8_button.setText("  - ")
        self.decrease_amplitude1_button.move(400, 375)
        self.decrease_amplitude2_button.move(400, 450)
        self.decrease_amplitude3_button.move(400, 525)
        self.decrease_amplitude4_button.move(400, 600)
        self.decrease_amplitude5_button.move(400, 675)
        self.decrease_amplitude6_button.move(400, 750)
        self.decrease_amplitude7_button.move(400, 825)
        self.decrease_amplitude8_button.move(400, 900)
        self.decrease_amplitude1_button.setFont(QFont('Arial', 14))
        self.decrease_amplitude2_button.setFont(QFont('Arial', 14))
        self.decrease_amplitude3_button.setFont(QFont('Arial', 14))
        self.decrease_amplitude4_button.setFont(QFont('Arial', 14))
        self.decrease_amplitude5_button.setFont(QFont('Arial', 14))
        self.decrease_amplitude6_button.setFont(QFont('Arial', 14))
        self.decrease_amplitude7_button.setFont(QFont('Arial', 14))
        self.decrease_amplitude8_button.setFont(QFont('Arial', 14))
        self.decrease_amplitude1_button.setStyleSheet("background-color: palegreen; border: 2 solid; border-radius: 1")
        self.decrease_amplitude2_button.setStyleSheet("background-color: palegreen; border: 2 solid; border-radius: 1")
        self.decrease_amplitude3_button.setStyleSheet("background-color: palegreen; border: 2 solid; border-radius: 1")
        self.decrease_amplitude4_button.setStyleSheet("background-color: palegreen; border: 2 solid; border-radius: 1")
        self.decrease_amplitude5_button.setStyleSheet("background-color: palegreen; border: 2 solid; border-radius: 1")
        self.decrease_amplitude6_button.setStyleSheet("background-color: palegreen; border: 2 solid; border-radius: 1")
        self.decrease_amplitude7_button.setStyleSheet("background-color: palegreen; border: 2 solid; border-radius: 1")
        self.decrease_amplitude8_button.setStyleSheet("background-color: palegreen; border: 2 solid; border-radius: 1")
        self.decrease_amplitude1_button.adjustSize()
        self.decrease_amplitude2_button.adjustSize()
        self.decrease_amplitude3_button.adjustSize()
        self.decrease_amplitude4_button.adjustSize()
        self.decrease_amplitude5_button.adjustSize()
        self.decrease_amplitude6_button.adjustSize()
        self.decrease_amplitude7_button.adjustSize()
        self.decrease_amplitude8_button.adjustSize()
        self.decrease_amplitude1_button.clicked.connect(lambda:self.decrease_amplitude1(current_parameters)) 
        self.decrease_amplitude2_button.clicked.connect(lambda:self.decrease_amplitude2(current_parameters)) 
        self.decrease_amplitude3_button.clicked.connect(lambda:self.decrease_amplitude3(current_parameters))
        self.decrease_amplitude4_button.clicked.connect(lambda:self.decrease_amplitude4(current_parameters))
        self.decrease_amplitude5_button.clicked.connect(lambda:self.decrease_amplitude5(current_parameters))
        self.decrease_amplitude6_button.clicked.connect(lambda:self.decrease_amplitude6(current_parameters)) 
        self.decrease_amplitude7_button.clicked.connect(lambda:self.decrease_amplitude7(current_parameters)) 
        self.decrease_amplitude8_button.clicked.connect(lambda:self.decrease_amplitude8(current_parameters))
        ### 1.12 - Mettre les boutons "+" et "-" pour la fréquence###
        ### 1.12.1 - "+" pour la fréquence ###
        self.increase_frequency1_button = QtWidgets.QPushButton(self)
        self.increase_frequency2_button = QtWidgets.QPushButton(self)
        self.increase_frequency3_button = QtWidgets.QPushButton(self)
        self.increase_frequency4_button = QtWidgets.QPushButton(self)
        self.increase_frequency5_button = QtWidgets.QPushButton(self)
        self.increase_frequency6_button = QtWidgets.QPushButton(self)
        self.increase_frequency7_button = QtWidgets.QPushButton(self)
        self.increase_frequency8_button = QtWidgets.QPushButton(self)
        self.increase_frequency1_button.setText(" + ")
        self.increase_frequency2_button.setText(" + ")
        self.increase_frequency3_button.setText(" + ")
        self.increase_frequency4_button.setText(" + ")
        self.increase_frequency5_button.setText(" + ")
        self.increase_frequency6_button.setText(" + ")
        self.increase_frequency7_button.setText(" + ")
        self.increase_frequency8_button.setText(" + ")
        self.increase_frequency1_button.move(900, 375)
        self.increase_frequency2_button.move(900, 450)
        self.increase_frequency3_button.move(900, 525)
        self.increase_frequency4_button.move(900, 600)
        self.increase_frequency5_button.move(900, 675)
        self.increase_frequency6_button.move(900, 750)
        self.increase_frequency7_button.move(900, 825)
        self.increase_frequency8_button.move(900, 900)
        self.increase_frequency1_button.setFont(QFont('Arial', 14))
        self.increase_frequency2_button.setFont(QFont('Arial', 14))
        self.increase_frequency3_button.setFont(QFont('Arial', 14))
        self.increase_frequency4_button.setFont(QFont('Arial', 14))
        self.increase_frequency5_button.setFont(QFont('Arial', 14))
        self.increase_frequency6_button.setFont(QFont('Arial', 14))
        self.increase_frequency7_button.setFont(QFont('Arial', 14))
        self.increase_frequency8_button.setFont(QFont('Arial', 14))
        self.increase_frequency1_button.setStyleSheet("background-color: palegreen; border: 2 solid; border-radius: 1")
        self.increase_frequency2_button.setStyleSheet("background-color: palegreen; border: 2 solid; border-radius: 1")
        self.increase_frequency3_button.setStyleSheet("background-color: palegreen; border: 2 solid; border-radius: 1")
        self.increase_frequency4_button.setStyleSheet("background-color: palegreen; border: 2 solid; border-radius: 1")
        self.increase_frequency5_button.setStyleSheet("background-color: palegreen; border: 2 solid; border-radius: 1")
        self.increase_frequency6_button.setStyleSheet("background-color: palegreen; border: 2 solid; border-radius: 1")
        self.increase_frequency7_button.setStyleSheet("background-color: palegreen; border: 2 solid; border-radius: 1")
        self.increase_frequency8_button.setStyleSheet("background-color: palegreen; border: 2 solid; border-radius: 1")
        self.increase_frequency1_button.adjustSize()
        self.increase_frequency2_button.adjustSize()
        self.increase_frequency3_button.adjustSize()
        self.increase_frequency4_button.adjustSize()
        self.increase_frequency5_button.adjustSize()
        self.increase_frequency6_button.adjustSize()
        self.increase_frequency7_button.adjustSize()
        self.increase_frequency8_button.adjustSize()
        self.increase_frequency1_button.clicked.connect(lambda:self.increase_frequency1(current_parameters))
        self.increase_frequency2_button.clicked.connect(lambda:self.increase_frequency2(current_parameters))
        self.increase_frequency3_button.clicked.connect(lambda:self.increase_frequency3(current_parameters))
        self.increase_frequency4_button.clicked.connect(lambda:self.increase_frequency4(current_parameters))
        self.increase_frequency5_button.clicked.connect(lambda:self.increase_frequency5(current_parameters)) 
        self.increase_frequency6_button.clicked.connect(lambda:self.increase_frequency6(current_parameters))
        self.increase_frequency7_button.clicked.connect(lambda:self.increase_frequency7(current_parameters))
        self.increase_frequency8_button.clicked.connect(lambda:self.increase_frequency8(current_parameters))
        ### 1.12.2 - "-" pour la fréquence ###
        self.decrease_frequency1_button = QtWidgets.QPushButton(self)
        self.decrease_frequency2_button = QtWidgets.QPushButton(self)
        self.decrease_frequency3_button = QtWidgets.QPushButton(self)
        self.decrease_frequency4_button = QtWidgets.QPushButton(self)
        self.decrease_frequency5_button = QtWidgets.QPushButton(self)
        self.decrease_frequency6_button = QtWidgets.QPushButton(self)
        self.decrease_frequency7_button = QtWidgets.QPushButton(self)
        self.decrease_frequency8_button = QtWidgets.QPushButton(self)
        self.decrease_frequency1_button.setText("  - ")
        self.decrease_frequency2_button.setText("  - ")
        self.decrease_frequency3_button.setText("  - ")
        self.decrease_frequency4_button.setText("  - ")
        self.decrease_frequency5_button.setText("  - ")
        self.decrease_frequency6_button.setText("  - ")
        self.decrease_frequency7_button.setText("  - ")
        self.decrease_frequency8_button.setText("  - ")
        self.decrease_frequency1_button.move(800, 375)
        self.decrease_frequency2_button.move(800, 450)
        self.decrease_frequency3_button.move(800, 525)
        self.decrease_frequency4_button.move(800, 600)
        self.decrease_frequency5_button.move(800, 675)
        self.decrease_frequency6_button.move(800, 750)
        self.decrease_frequency7_button.move(800, 825)
        self.decrease_frequency8_button.move(800, 900)
        self.decrease_frequency1_button.setFont(QFont('Arial', 14))
        self.decrease_frequency2_button.setFont(QFont('Arial', 14))
        self.decrease_frequency3_button.setFont(QFont('Arial', 14))
        self.decrease_frequency4_button.setFont(QFont('Arial', 14))
        self.decrease_frequency5_button.setFont(QFont('Arial', 14))
        self.decrease_frequency6_button.setFont(QFont('Arial', 14))
        self.decrease_frequency7_button.setFont(QFont('Arial', 14))
        self.decrease_frequency8_button.setFont(QFont('Arial', 14))
        self.decrease_frequency1_button.setStyleSheet("background-color: palegreen; border: 2 solid; border-radius: 1")
        self.decrease_frequency2_button.setStyleSheet("background-color: palegreen; border: 2 solid; border-radius: 1")
        self.decrease_frequency3_button.setStyleSheet("background-color: palegreen; border: 2 solid; border-radius: 1")
        self.decrease_frequency4_button.setStyleSheet("background-color: palegreen; border: 2 solid; border-radius: 1")
        self.decrease_frequency5_button.setStyleSheet("background-color: palegreen; border: 2 solid; border-radius: 1")
        self.decrease_frequency6_button.setStyleSheet("background-color: palegreen; border: 2 solid; border-radius: 1")
        self.decrease_frequency7_button.setStyleSheet("background-color: palegreen; border: 2 solid; border-radius: 1")
        self.decrease_frequency8_button.setStyleSheet("background-color: palegreen; border: 2 solid; border-radius: 1")
        self.decrease_frequency1_button.adjustSize()
        self.decrease_frequency2_button.adjustSize()
        self.decrease_frequency3_button.adjustSize()
        self.decrease_frequency4_button.adjustSize()
        self.decrease_frequency5_button.adjustSize()
        self.decrease_frequency6_button.adjustSize()
        self.decrease_frequency7_button.adjustSize()
        self.decrease_frequency8_button.adjustSize()
        self.decrease_frequency1_button.clicked.connect(lambda:self.decrease_frequency1(current_parameters))
        self.decrease_frequency2_button.clicked.connect(lambda:self.decrease_frequency2(current_parameters))
        self.decrease_frequency3_button.clicked.connect(lambda:self.decrease_frequency3(current_parameters))
        self.decrease_frequency4_button.clicked.connect(lambda:self.decrease_frequency4(current_parameters))
        self.decrease_frequency5_button.clicked.connect(lambda:self.decrease_frequency5(current_parameters)) 
        self.decrease_frequency6_button.clicked.connect(lambda:self.decrease_frequency6(current_parameters)) 
        self.decrease_frequency7_button.clicked.connect(lambda:self.decrease_frequency7(current_parameters))
        self.decrease_frequency8_button.clicked.connect(lambda:self.decrease_frequency8(current_parameters))
        ### 1.13 - Mettre les boutons "+" et "-" pour la durée d'impulsion ###
        ### 1.13.1 - "+" pour durée d'impulsion
        self.increase_imp1_button = QtWidgets.QPushButton(self)
        self.increase_imp2_button = QtWidgets.QPushButton(self)
        self.increase_imp3_button = QtWidgets.QPushButton(self)
        self.increase_imp4_button = QtWidgets.QPushButton(self)
        self.increase_imp5_button = QtWidgets.QPushButton(self)
        self.increase_imp6_button = QtWidgets.QPushButton(self)
        self.increase_imp7_button = QtWidgets.QPushButton(self)
        self.increase_imp8_button = QtWidgets.QPushButton(self)
        self.increase_imp1_button.setText(" + ")
        self.increase_imp2_button.setText(" + ")
        self.increase_imp3_button.setText(" + ")
        self.increase_imp4_button.setText(" + ")
        self.increase_imp5_button.setText(" + ")
        self.increase_imp6_button.setText(" + ")
        self.increase_imp7_button.setText(" + ")
        self.increase_imp8_button.setText(" + ")
        self.increase_imp1_button.move(1325, 375)
        self.increase_imp2_button.move(1325, 450)
        self.increase_imp3_button.move(1325, 525)
        self.increase_imp4_button.move(1325, 600)
        self.increase_imp5_button.move(1325, 675)
        self.increase_imp6_button.move(1325, 750)
        self.increase_imp7_button.move(1325, 825)
        self.increase_imp8_button.move(1325, 900)
        self.increase_imp1_button.setFont(QFont('Arial', 14))
        self.increase_imp2_button.setFont(QFont('Arial', 14))
        self.increase_imp3_button.setFont(QFont('Arial', 14))
        self.increase_imp4_button.setFont(QFont('Arial', 14))
        self.increase_imp5_button.setFont(QFont('Arial', 14))
        self.increase_imp6_button.setFont(QFont('Arial', 14))
        self.increase_imp7_button.setFont(QFont('Arial', 14))
        self.increase_imp8_button.setFont(QFont('Arial', 14))
        self.increase_imp1_button.setStyleSheet("background-color: palegreen; border: 2 solid; border-radius: 1")
        self.increase_imp2_button.setStyleSheet("background-color: palegreen; border: 2 solid; border-radius: 1")
        self.increase_imp3_button.setStyleSheet("background-color: palegreen; border: 2 solid; border-radius: 1")
        self.increase_imp4_button.setStyleSheet("background-color: palegreen; border: 2 solid; border-radius: 1")
        self.increase_imp5_button.setStyleSheet("background-color: palegreen; border: 2 solid; border-radius: 1")
        self.increase_imp6_button.setStyleSheet("background-color: palegreen; border: 2 solid; border-radius: 1")
        self.increase_imp7_button.setStyleSheet("background-color: palegreen; border: 2 solid; border-radius: 1")
        self.increase_imp8_button.setStyleSheet("background-color: palegreen; border: 2 solid; border-radius: 1")
        self.increase_imp1_button.adjustSize()
        self.increase_imp2_button.adjustSize()
        self.increase_imp3_button.adjustSize()
        self.increase_imp4_button.adjustSize()
        self.increase_imp5_button.adjustSize()
        self.increase_imp6_button.adjustSize()
        self.increase_imp7_button.adjustSize()
        self.increase_imp8_button.adjustSize()
        self.increase_imp1_button.clicked.connect(lambda:self.increase_imp1(current_parameters)) 
        self.increase_imp2_button.clicked.connect(lambda:self.increase_imp2(current_parameters)) 
        self.increase_imp3_button.clicked.connect(lambda:self.increase_imp3(current_parameters)) 
        self.increase_imp4_button.clicked.connect(lambda:self.increase_imp4(current_parameters)) 
        self.increase_imp5_button.clicked.connect(lambda:self.increase_imp5(current_parameters)) 
        self.increase_imp6_button.clicked.connect(lambda:self.increase_imp6(current_parameters)) 
        self.increase_imp7_button.clicked.connect(lambda:self.increase_imp7(current_parameters)) 
        self.increase_imp8_button.clicked.connect(lambda:self.increase_imp8(current_parameters)) 
        ### 1.13.2 - "-" pour durée d'impulsion
        self.decrease_imp1_button = QtWidgets.QPushButton(self)
        self.decrease_imp2_button = QtWidgets.QPushButton(self)
        self.decrease_imp3_button = QtWidgets.QPushButton(self)
        self.decrease_imp4_button = QtWidgets.QPushButton(self)
        self.decrease_imp5_button = QtWidgets.QPushButton(self)
        self.decrease_imp6_button = QtWidgets.QPushButton(self)
        self.decrease_imp7_button = QtWidgets.QPushButton(self)
        self.decrease_imp8_button = QtWidgets.QPushButton(self)
        self.decrease_imp1_button.setText("  - ")
        self.decrease_imp2_button.setText("  - ")
        self.decrease_imp3_button.setText("  - ")
        self.decrease_imp4_button.setText("  - ")
        self.decrease_imp5_button.setText("  - ")
        self.decrease_imp6_button.setText("  - ")
        self.decrease_imp7_button.setText("  - ")
        self.decrease_imp8_button.setText("  - ")
        self.decrease_imp1_button.move(1225, 375)
        self.decrease_imp2_button.move(1225, 450)
        self.decrease_imp3_button.move(1225, 525)
        self.decrease_imp4_button.move(1225, 600)
        self.decrease_imp5_button.move(1225, 675)
        self.decrease_imp6_button.move(1225, 750)
        self.decrease_imp7_button.move(1225, 825)
        self.decrease_imp8_button.move(1225, 900)
        self.decrease_imp1_button.setFont(QFont('Arial', 14))
        self.decrease_imp2_button.setFont(QFont('Arial', 14))
        self.decrease_imp3_button.setFont(QFont('Arial', 14))
        self.decrease_imp4_button.setFont(QFont('Arial', 14))
        self.decrease_imp5_button.setFont(QFont('Arial', 14))
        self.decrease_imp6_button.setFont(QFont('Arial', 14))
        self.decrease_imp7_button.setFont(QFont('Arial', 14))
        self.decrease_imp8_button.setFont(QFont('Arial', 14))
        self.decrease_imp1_button.setStyleSheet("background-color: palegreen; border: 2 solid; border-radius: 1")
        self.decrease_imp2_button.setStyleSheet("background-color: palegreen; border: 2 solid; border-radius: 1")
        self.decrease_imp3_button.setStyleSheet("background-color: palegreen; border: 2 solid; border-radius: 1")
        self.decrease_imp4_button.setStyleSheet("background-color: palegreen; border: 2 solid; border-radius: 1")
        self.decrease_imp5_button.setStyleSheet("background-color: palegreen; border: 2 solid; border-radius: 1")
        self.decrease_imp6_button.setStyleSheet("background-color: palegreen; border: 2 solid; border-radius: 1")
        self.decrease_imp7_button.setStyleSheet("background-color: palegreen; border: 2 solid; border-radius: 1")
        self.decrease_imp8_button.setStyleSheet("background-color: palegreen; border: 2 solid; border-radius: 1")
        self.decrease_imp1_button.adjustSize()
        self.decrease_imp2_button.adjustSize()
        self.decrease_imp3_button.adjustSize()
        self.decrease_imp4_button.adjustSize()
        self.decrease_imp5_button.adjustSize()
        self.decrease_imp6_button.adjustSize()
        self.decrease_imp7_button.adjustSize()
        self.decrease_imp8_button.adjustSize()
        self.decrease_imp1_button.clicked.connect(lambda:self.decrease_imp1(current_parameters)) 
        self.decrease_imp2_button.clicked.connect(lambda:self.decrease_imp2(current_parameters))  
        self.decrease_imp3_button.clicked.connect(lambda:self.decrease_imp3(current_parameters)) 
        self.decrease_imp4_button.clicked.connect(lambda:self.decrease_imp4(current_parameters)) 
        self.decrease_imp5_button.clicked.connect(lambda:self.decrease_imp5(current_parameters)) 
        self.decrease_imp6_button.clicked.connect(lambda:self.decrease_imp6(current_parameters))  
        self.decrease_imp7_button.clicked.connect(lambda:self.decrease_imp7(current_parameters))  
        self.decrease_imp8_button.clicked.connect(lambda:self.decrease_imp8(current_parameters)) 
        self.check_if_off(current_parameters)
    def check_if_off(self, current_parameters):
         if (int(current_parameters.electrode1_amplitude)==0) and (int(current_parameters.electrode1_frequency)==0) and (int(current_parameters.electrode1_length_imp)==0):
             self.increase_amplitude1_button.setEnabled(False)
             self.decrease_amplitude1_button.setEnabled(False)
             self.increase_frequency1_button.setEnabled(False)
             self.decrease_frequency1_button.setEnabled(False)
             self.increase_imp1_button.setEnabled(False)
             self.decrease_imp1_button.setEnabled(False)
         if (int(current_parameters.electrode2_amplitude)==0) and (int(current_parameters.electrode2_frequency)==0) and (int(current_parameters.electrode2_length_imp)==0):
             self.increase_amplitude2_button.setEnabled(False)
             self.decrease_amplitude2_button.setEnabled(False)
             self.increase_frequency2_button.setEnabled(False)
             self.decrease_frequency2_button.setEnabled(False)
             self.increase_imp2_button.setEnabled(False)
             self.decrease_imp2_button.setEnabled(False)
         if (int(current_parameters.electrode3_amplitude)==0) and (int(current_parameters.electrode3_frequency)==0) and (int(current_parameters.electrode3_length_imp)==0):
             self.increase_amplitude3_button.setEnabled(False)
             self.decrease_amplitude3_button.setEnabled(False)
             self.increase_frequency3_button.setEnabled(False)
             self.decrease_frequency3_button.setEnabled(False)
             self.increase_imp3_button.setEnabled(False)
             self.decrease_imp3_button.setEnabled(False)
         if (int(current_parameters.electrode4_amplitude)==0) and (int(current_parameters.electrode4_frequency)==0) and (int(current_parameters.electrode4_length_imp)==0):
             self.increase_amplitude4_button.setEnabled(False)
             self.decrease_amplitude4_button.setEnabled(False)
             self.increase_frequency4_button.setEnabled(False)
             self.decrease_frequency4_button.setEnabled(False)
             self.increase_imp4_button.setEnabled(False)
             self.decrease_imp4_button.setEnabled(False)  
         if (int(current_parameters.electrode5_amplitude)==0) and (int(current_parameters.electrode5_frequency)==0) and (int(current_parameters.electrode5_length_imp)==0):
             self.increase_amplitude5_button.setEnabled(False)
             self.decrease_amplitude5_button.setEnabled(False)
             self.increase_frequency5_button.setEnabled(False)
             self.decrease_frequency5_button.setEnabled(False)
             self.increase_imp5_button.setEnabled(False)
             self.decrease_imp5_button.setEnabled(False)
         if (int(current_parameters.electrode6_amplitude)==0) and (int(current_parameters.electrode6_frequency)==0) and (int(current_parameters.electrode6_length_imp)==0):
             self.increase_amplitude6_button.setEnabled(False)
             self.decrease_amplitude6_button.setEnabled(False)
             self.increase_frequency6_button.setEnabled(False)
             self.decrease_frequency6_button.setEnabled(False)
             self.increase_imp6_button.setEnabled(False)
             self.decrease_imp6_button.setEnabled(False)
         if (int(current_parameters.electrode7_amplitude)==0) and (int(current_parameters.electrode7_frequency)==0) and (int(current_parameters.electrode7_length_imp)==0):
             self.increase_amplitude7_button.setEnabled(False)
             self.decrease_amplitude7_button.setEnabled(False)
             self.increase_frequency7_button.setEnabled(False)
             self.decrease_frequency7_button.setEnabled(False)
             self.increase_imp7_button.setEnabled(False)
             self.decrease_imp7_button.setEnabled(False)
         if (int(current_parameters.electrode8_amplitude)==0) and (int(current_parameters.electrode8_frequency)==0) and (int(current_parameters.electrode8_length_imp)==0):
             self.increase_amplitude8_button.setEnabled(False)
             self.decrease_amplitude8_button.setEnabled(False)
             self.increase_frequency8_button.setEnabled(False)
             self.decrease_frequency8_button.setEnabled(False)
             self.increase_imp8_button.setEnabled(False)
             self.decrease_imp8_button.setEnabled(False) 

    #def clocking(self):
        #current_time = QTime.elapsed()
        #display_time = current_time.toString("hh:mm:ss")
        #self.timer_label.setText(display_time)
        #print(display_time)
    def countdown_timer(self, current_parameters):
        self.stim_training_length_sec = 60*(current_parameters.get_stim_training_length())
        while self.stim_training_length_sec > 0:
            self.sec = self.stim_training_length_sec%60
            self.min = self.stim_training_length_sec//60
            time.sleep(1)
            self.stim_training_length_sec -=1
            print("temps restant: ", self.min, " min ", self.sec ," sec ")
            self.timer_label_min.setText(str(self.min))
            self.timer_label_min.adjustSize()
            self.timer_label_sec.setText(str(self.sec))
            self.timer_label_sec.adjustSize()
        self.end_of_stim = True
        self.close()
    

    def increase_amplitude1(self, current_parameters):
        if (int(current_parameters.electrode1_amplitude)) < MAX_AMPLITUDE:
            current_parameters.electrode1_amplitude = str(int(current_parameters.electrode1_amplitude)+ 2)
            self.update_labels(current_parameters)
    def increase_amplitude2(self, current_parameters):
        if (int(current_parameters.electrode2_amplitude)) < MAX_AMPLITUDE:
            current_parameters.electrode2_amplitude = str(int(current_parameters.electrode2_amplitude)+ 2)
            self.update_labels(current_parameters)
    def increase_amplitude3(self, current_parameters):
        if (int(current_parameters.electrode3_amplitude)) < MAX_AMPLITUDE:
            current_parameters.electrode3_amplitude = str(int(current_parameters.electrode3_amplitude)+ 2)
            self.update_labels(current_parameters)
    def increase_amplitude4(self, current_parameters):
        if (int(current_parameters.electrode4_amplitude)) < MAX_AMPLITUDE:
            current_parameters.electrode4_amplitude = str(int(current_parameters.electrode4_amplitude)+ 2)
            self.update_labels(current_parameters)
    def increase_amplitude5(self, current_parameters):
        if (int(current_parameters.electrode5_amplitude)) < MAX_AMPLITUDE:
            current_parameters.electrode5_amplitude = str(int(current_parameters.electrode5_amplitude)+ 2)
            self.update_labels(current_parameters)
    def increase_amplitude6(self, current_parameters):
        if (int(current_parameters.electrode6_amplitude)) < MAX_AMPLITUDE:
            current_parameters.electrode6_amplitude = str(int(current_parameters.electrode6_amplitude)+ 2)
            self.update_labels(current_parameters)
    def increase_amplitude7(self, current_parameters):
        if (int(current_parameters.electrode7_amplitude)) < MAX_AMPLITUDE:
            current_parameters.electrode7_amplitude = str(int(current_parameters.electrode7_amplitude)+ 2)
            self.update_labels(current_parameters)
    def increase_amplitude8(self, current_parameters):
        if (int(current_parameters.electrode8_amplitude)) < MAX_AMPLITUDE:
            current_parameters.electrode8_amplitude = str(int(current_parameters.electrode8_amplitude)+ 2)
            self.update_labels(current_parameters)

    def decrease_amplitude1(self, current_parameters):
        if (int(current_parameters.electrode1_amplitude)) > MIN_AMPLITUDE:
            current_parameters.electrode1_amplitude = str(int(current_parameters.electrode1_amplitude)- 2)
            self.update_labels(current_parameters)
    def decrease_amplitude2(self, current_parameters):
        if (int(current_parameters.electrode2_amplitude)) > MIN_AMPLITUDE:
            current_parameters.electrode2_amplitude = str(int(current_parameters.electrode2_amplitude)- 2)
            self.update_labels(current_parameters)
    def decrease_amplitude3(self, current_parameters):
        if (int(current_parameters.electrode3_amplitude)) > MIN_AMPLITUDE:
            current_parameters.electrode3_amplitude = str(int(current_parameters.electrode3_amplitude)- 2)
            self.update_labels(current_parameters)
    def decrease_amplitude4(self, current_parameters):
        if (int(current_parameters.electrode4_amplitude)) > MIN_AMPLITUDE:
            current_parameters.electrode4_amplitude = str(int(current_parameters.electrode4_amplitude)- 2)
            self.update_labels(current_parameters)
    def decrease_amplitude5(self, current_parameters):
        if (int(current_parameters.electrode5_amplitude)) > MIN_AMPLITUDE:
            current_parameters.electrode5_amplitude = str(int(current_parameters.electrode5_amplitude)- 2)
            self.update_labels(current_parameters)
    def decrease_amplitude6(self, current_parameters):
        if (int(current_parameters.electrode6_amplitude)) > MIN_AMPLITUDE:
            current_parameters.electrode6_amplitude = str(int(current_parameters.electrode6_amplitude)- 2)
            self.update_labels(current_parameters)
    def decrease_amplitude7(self, current_parameters):
        if (int(current_parameters.electrode7_amplitude)) > MIN_AMPLITUDE:
            current_parameters.electrode7_amplitude = str(int(current_parameters.electrode7_amplitude)- 2)
            self.update_labels(current_parameters)
    def decrease_amplitude8(self, current_parameters):
        if (int(current_parameters.electrode8_amplitude)) > MIN_AMPLITUDE:
            current_parameters.electrode8_amplitude = str(int(current_parameters.electrode8_amplitude)- 2)
            self.update_labels(current_parameters)

    def increase_frequency1(self, current_parameters):
        if (int(current_parameters.electrode1_frequency)) < MAX_FREQ:
            if (int(current_parameters.electrode1_frequency)) == 0:
                current_parameters.electrode1_frequency = str(10)
            else:
                current_parameters.electrode1_frequency = str(int(current_parameters.electrode1_frequency)+ 5)
            self.update_labels(current_parameters)
    def increase_frequency2(self, current_parameters):
        if (int(current_parameters.electrode2_frequency)) < MAX_FREQ:
            if (int(current_parameters.electrode2_frequency)) == 0:
                current_parameters.electrode2_frequency = str(10)
            else:
                current_parameters.electrode2_frequency = str(int(current_parameters.electrode2_frequency)+ 5)
            self.update_labels(current_parameters)
    def increase_frequency3(self, current_parameters):
        if (int(current_parameters.electrode3_frequency)) < MAX_FREQ:
            if (int(current_parameters.electrode3_frequency)) == 0:
                current_parameters.electrode3_frequency = str(10)
            else:
                current_parameters.electrode3_frequency = str(int(current_parameters.electrode3_frequency)+ 5)
            self.update_labels(current_parameters)
    def increase_frequency4(self, current_parameters):
        if (int(current_parameters.electrode4_frequency)) < MAX_FREQ:
            if (int(current_parameters.electrode4_frequency)) == 0:
                current_parameters.electrode4_frequency = str(10)
            else:
                current_parameters.electrode4_frequency = str(int(current_parameters.electrode4_frequency)+ 5)
            self.update_labels(current_parameters)
    def increase_frequency5(self, current_parameters):
        if (int(current_parameters.electrode5_frequency)) < MAX_FREQ:
            if (int(current_parameters.electrode5_frequency)) == 0:
                current_parameters.electrode5_frequency = str(10)
            else:
                current_parameters.electrode5_frequency = str(int(current_parameters.electrode5_frequency)+ 5)
            self.update_labels(current_parameters)
    def increase_frequency6(self, current_parameters):
        if (int(current_parameters.electrode6_frequency)) < MAX_FREQ:
            if (int(current_parameters.electrode6_frequency)) == 0:
                current_parameters.electrode6_frequency = str(10)
            else:
                current_parameters.electrode6_frequency = str(int(current_parameters.electrode6_frequency)+ 5)
            self.update_labels(current_parameters)
    def increase_frequency7(self, current_parameters):
        if (int(current_parameters.electrode7_frequency)) < MAX_FREQ:
            if (int(current_parameters.electrode7_frequency)) == 0:
                current_parameters.electrode7_frequency = str(10)
            else:
                current_parameters.electrode7_frequency = str(int(current_parameters.electrode7_frequency)+ 5)
            self.update_labels(current_parameters)
    def increase_frequency8(self, current_parameters):
        if (int(current_parameters.electrode8_frequency)) < MAX_FREQ:
            if (int(current_parameters.electrode8_frequency)) == 0:
                current_parameters.electrode8_frequency = str(10)
            else:
                current_parameters.electrode8_frequency = str(int(current_parameters.electrode8_frequency)+ 5)
            self.update_labels(current_parameters)

    def decrease_frequency1(self, current_parameters):
        if (int(current_parameters.electrode1_frequency)) > MIN_FREQ:
            if (int(current_parameters.electrode1_frequency)) == 10:
                current_parameters.electrode1_frequency = str(0)
            else: 
                current_parameters.electrode1_frequency = str(int(current_parameters.electrode1_frequency)- 5)
            self.update_labels(current_parameters)
    def decrease_frequency2(self, current_parameters):
        if (int(current_parameters.electrode2_frequency)) > MIN_FREQ:
            if (int(current_parameters.electrode2_frequency)) == 10:
                current_parameters.electrode2_frequency = str(0)
            else: 
                current_parameters.electrode2_frequency = str(int(current_parameters.electrode2_frequency)- 5)
            self.update_labels(current_parameters)
    def decrease_frequency3(self, current_parameters):
        if (int(current_parameters.electrode3_frequency)) > MIN_FREQ:
            if (int(current_parameters.electrode3_frequency))== 10:
                current_parameters.electrode3_frequency = str(0)
            else:
                current_parameters.electrode3_frequency = str(int(current_parameters.electrode3_frequency)- 5)
            self.update_labels(current_parameters)
    def decrease_frequency4(self, current_parameters):
        if (int(current_parameters.electrode4_frequency)) > MIN_FREQ:
            if (int(current_parameters.electrode4_frequency)) == 10:
                current_parameters.electrode4_frequency = str(0)
            else: 
                current_parameters.electrode4_frequency = str(int(current_parameters.electrode4_frequency)- 5)
            self.update_labels(current_parameters)
    def decrease_frequency5(self, current_parameters):
        if (int(current_parameters.electrode5_frequency)) > MIN_FREQ:
            if (int(current_parameters.electrode5_frequency)) == 10:
                current_parameters.electrode5_frequency = str(0)
            else: 
                current_parameters.electrode5_frequency = str(int(current_parameters.electrode5_frequency)- 5)
            self.update_labels(current_parameters)
    def decrease_frequency6(self, current_parameters):
        if (int(current_parameters.electrode6_frequency)) > MIN_FREQ:
            if (int(current_parameters.electrode6_frequency)) == 10:
                current_parameters.electrode6_frequency = str(0)
            else: 
                current_parameters.electrode6_frequency = str(int(current_parameters.electrode6_frequency)- 5)
            self.update_labels(current_parameters)
    def decrease_frequency7(self, current_parameters):
        if (int(current_parameters.electrode7_frequency)) > MIN_FREQ:
            if (int(current_parameters.electrode7_frequency)) == 10:
                current_parameters.electrode7_frequency = str(0)
            else: 
                current_parameters.electrode7_frequency = str(int(current_parameters.electrode7_frequency)- 5)
            self.update_labels(current_parameters)
    def decrease_frequency8(self, current_parameters):
        if (int(current_parameters.electrode8_frequency)) > MIN_FREQ:
            if (int(current_parameters.electrode8_frequency)) == 10:
                current_parameters.electrode8_frequency = str(0)
            else: 
                current_parameters.electrode8_frequency = str(int(current_parameters.electrode8_frequency)- 5)
            self.update_labels(current_parameters)
    ## Durée d'impulsion ##
    def increase_imp1(self, current_parameters):
        if (int(current_parameters.electrode1_length_imp)) < MAX_IMP:
            if (int(current_parameters.electrode1_length_imp)) == 0:
                current_parameters.electrode1_length_imp = str(20)
            else:
                current_parameters.electrode1_length_imp = str(int(current_parameters.electrode1_length_imp)+ 10)
            self.update_labels(current_parameters)
    def increase_imp2(self, current_parameters):
        if (int(current_parameters.electrode2_length_imp)) < MAX_IMP:
            if (int(current_parameters.electrode2_length_imp)) == 0:
                current_parameters.electrode2_length_imp = str(20)
            else:
                current_parameters.electrode2_length_imp = str(int(current_parameters.electrode2_length_imp)+ 10)
            self.update_labels(current_parameters)
    def increase_imp3(self, current_parameters):
        if (int(current_parameters.electrode3_length_imp)) < MAX_IMP:
            if (int(current_parameters.electrode3_length_imp)) == 0:
                current_parameters.electrode3_length_imp = str(20)
            else:
                current_parameters.electrode3_length_imp = str(int(current_parameters.electrode3_length_imp)+ 10)
            self.update_labels(current_parameters)
    def increase_imp4(self, current_parameters):
        if (int(current_parameters.electrode4_length_imp)) < MAX_IMP:
            if (int(current_parameters.electrode4_length_imp)) == 0:
                current_parameters.electrode4_length_imp = str(20)
            else:
                current_parameters.electrode4_length_imp = str(int(current_parameters.electrode4_length_imp)+ 10)
            self.update_labels(current_parameters)
    def increase_imp5(self, current_parameters):
        if (int(current_parameters.electrode5_length_imp)) < MAX_IMP:
            if (int(current_parameters.electrode5_length_imp)) == 0:
                current_parameters.electrode5_length_imp = str(20)
            else:
                current_parameters.electrode5_length_imp = str(int(current_parameters.electrode5_length_imp)+ 10)
            self.update_labels(current_parameters)
    def increase_imp6(self, current_parameters):
        if (int(current_parameters.electrode6_length_imp)) < MAX_FREQ:
            if (int(current_parameters.electrode6_length_imp)) == 0:
                current_parameters.electrode6_length_imp = str(20)
            else:
                current_parameters.electrode6_length_imp = str(int(current_parameters.electrode6_length_imp)+ 10)
            self.update_labels(current_parameters)
    def increase_imp7(self, current_parameters):
        if (int(current_parameters.electrode7_length_imp)) < MAX_IMP:
            if (int(current_parameters.electrode7_length_imp)) == 0:
                current_parameters.electrode7_length_imp = str(20)
            else:
                current_parameters.electrode7_length_imp = str(int(current_parameters.electrode7_length_imp)+ 10)
            self.update_labels(current_parameters)
    def increase_imp8(self, current_parameters):
        if (int(current_parameters.electrode8_length_imp)) < MAX_IMP:
            if (int(current_parameters.electrode8_length_imp)) == 0:
                current_parameters.electrode8_length_imp = str(20)
            else:
                current_parameters.electrode8_length_imp = str(int(current_parameters.electrode8_length_imp)+ 10)
            self.update_labels(current_parameters)
    def decrease_imp1(self, current_parameters):
        if (int(current_parameters.electrode1_length_imp)) > MIN_IMP:
            if (int(current_parameters.electrode1_length_imp)) == 20:
                current_parameters.electrode1_length_imp = str(0)
            else: 
                current_parameters.electrode1_length_imp = str(int(current_parameters.electrode1_length_imp)- 10)
            self.update_labels(current_parameters)
    def decrease_imp2(self, current_parameters):
        if (int(current_parameters.electrode2_length_imp)) > MIN_IMP:
            if (int(current_parameters.electrode2_length_imp)) == 20:
                current_parameters.electrode2_length_imp = str(0)
            else: 
                current_parameters.electrode2_length_imp = str(int(current_parameters.electrode2_length_imp)- 10)
            self.update_labels(current_parameters)
    def decrease_imp3(self, current_parameters):
        if (int(current_parameters.electrode3_length_imp)) > MIN_IMP:
            if (int(current_parameters.electrode3_length_imp)) == 20:
                current_parameters.electrode3_length_imp = str(0)
            else: 
                current_parameters.electrode3_length_imp = str(int(current_parameters.electrode3_length_imp)- 10)
            self.update_labels(current_parameters)
    def decrease_imp4(self, current_parameters):
        if (int(current_parameters.electrode4_length_imp)) > MIN_IMP:
            if (int(current_parameters.electrode4_length_imp)) == 20:
                current_parameters.electrode4_length_imp = str(0)
            else: 
                current_parameters.electrode4_length_imp = str(int(current_parameters.electrode4_length_imp)- 10)
            self.update_labels(current_parameters)
    def decrease_imp5(self, current_parameters):
        if (int(current_parameters.electrode5_length_imp)) > MIN_IMP:
            if (int(current_parameters.electrode5_length_imp)) == 20:
                current_parameters.electrode5_length_imp = str(0)
            else: 
                current_parameters.electrode5_length_imp = str(int(current_parameters.electrode5_length_imp)- 10)
            self.update_labels(current_parameters)
    def decrease_imp6(self, current_parameters):
        if (int(current_parameters.electrode6_length_imp)) > MIN_IMP:
            if (int(current_parameters.electrode6_length_imp)) == 20:
                current_parameters.electrode6_length_imp = str(0)
            else: 
                current_parameters.electrode6_length_imp = str(int(current_parameters.electrode6_length_imp)- 10)
            self.update_labels(current_parameters)
    def decrease_imp7(self, current_parameters):
        if (int(current_parameters.electrode7_length_imp)) > MIN_IMP:
            if (int(current_parameters.electrode7_length_imp)) == 20:
                current_parameters.electrode7_length_imp = str(0)
            else: 
                current_parameters.electrode7_length_imp = str(int(current_parameters.electrode7_length_imp)- 10)
            self.update_labels(current_parameters)
    def decrease_imp8(self, current_parameters):
        if (int(current_parameters.electrode8_length_imp)) > MIN_IMP:
            if (int(current_parameters.electrode8_length_imp)) == 20:
                current_parameters.electrode8_length_imp = str(0)
            else: 
                current_parameters.electrode8_length_imp = str(int(current_parameters.electrode8_length_imp)- 10)
            self.update_labels(current_parameters)
    def update_labels(self, current_parameters):
        self.current_amplitude1_label.setText(current_parameters.get_electrode1_amplitude())
        self.current_amplitude1_label.adjustSize()
        self.current_amplitude2_label.setText(current_parameters.get_electrode2_amplitude())
        self.current_amplitude2_label.adjustSize()
        self.current_amplitude3_label.setText(current_parameters.get_electrode3_amplitude())
        self.current_amplitude3_label.adjustSize()
        self.current_amplitude4_label.setText(current_parameters.get_electrode4_amplitude())
        self.current_amplitude4_label.adjustSize()
        self.current_amplitude5_label.setText(current_parameters.get_electrode5_amplitude())
        self.current_amplitude5_label.adjustSize()
        self.current_amplitude6_label.setText(current_parameters.get_electrode6_amplitude())
        self.current_amplitude6_label.adjustSize()
        self.current_amplitude7_label.setText(current_parameters.get_electrode7_amplitude())
        self.current_amplitude7_label.adjustSize()
        self.current_amplitude8_label.setText(current_parameters.get_electrode8_amplitude())
        self.current_amplitude8_label.adjustSize()
        self.current_frequency1_label.setText(current_parameters.get_electrode1_frequency())
        self.current_frequency1_label.adjustSize()
        self.current_frequency2_label.setText(current_parameters.get_electrode2_frequency())
        self.current_frequency2_label.adjustSize()
        self.current_frequency3_label.setText(current_parameters.get_electrode3_frequency())
        self.current_frequency3_label.adjustSize()
        self.current_frequency4_label.setText(current_parameters.get_electrode4_frequency())
        self.current_frequency4_label.adjustSize()
        self.current_frequency5_label.setText(current_parameters.get_electrode5_frequency())
        self.current_frequency5_label.adjustSize()
        self.current_frequency6_label.setText(current_parameters.get_electrode6_frequency())
        self.current_frequency6_label.adjustSize()
        self.current_frequency7_label.setText(current_parameters.get_electrode7_frequency())
        self.current_frequency7_label.adjustSize()
        self.current_frequency8_label.setText(current_parameters.get_electrode8_frequency())
        self.current_frequency8_label.adjustSize()
        self.current_imp_label1_label.setText(current_parameters.get_electrode1_length_imp())
        self.current_imp_label1_label.adjustSize()
        self.current_imp_label2_label.setText(current_parameters.get_electrode2_length_imp())
        self.current_imp_label2_label.adjustSize()
        self.current_imp_label3_label.setText(current_parameters.get_electrode3_length_imp())
        self.current_imp_label3_label.adjustSize()
        self.current_imp_label4_label.setText(current_parameters.get_electrode4_length_imp())
        self.current_imp_label4_label.adjustSize()
        self.current_imp_label5_label.setText(current_parameters.get_electrode5_length_imp())
        self.current_imp_label5_label.adjustSize()
        self.current_imp_label6_label.setText(current_parameters.get_electrode6_length_imp())
        self.current_imp_label6_label.adjustSize()
        self.current_imp_label7_label.setText(current_parameters.get_electrode7_length_imp())
        self.current_imp_label7_label.adjustSize()
        self.current_imp_label8_label.setText(current_parameters.get_electrode8_length_imp())
        self.current_imp_label8_label.adjustSize()
        self.update_parameters = numpy.empty([4,8],dtype=int)
        for i in range(len(self.update_parameters)):
            if i==0:
                self.update_parameters[i,:]=[current_parameters.get_electrode1_amplitude(), current_parameters.get_electrode2_amplitude(), current_parameters.get_electrode3_amplitude(),current_parameters.get_electrode4_amplitude(),current_parameters.get_electrode5_amplitude(),current_parameters.get_electrode6_amplitude(),current_parameters.get_electrode7_amplitude(),current_parameters.get_electrode8_amplitude()]
            if i==1:
                self.update_parameters[i,:]=[current_parameters.get_electrode1_frequency(), current_parameters.get_electrode2_frequency(), current_parameters.get_electrode3_frequency(),current_parameters.get_electrode4_frequency(),current_parameters.get_electrode5_frequency(),current_parameters.get_electrode6_frequency(),current_parameters.get_electrode7_frequency(),current_parameters.get_electrode8_frequency()]
            if i==2:
                self.update_parameters[i,:]=[current_parameters.get_electrode1_length_imp(),current_parameters.get_electrode2_length_imp(), current_parameters.get_electrode3_length_imp(), current_parameters.get_electrode4_length_imp(), current_parameters.get_electrode5_length_imp(), current_parameters.get_electrode6_length_imp(), current_parameters.get_electrode7_length_imp(),current_parameters.get_electrode8_length_imp()]
            if i==3:
                    self.update_parameters[i,:]=current_parameters.get_muscle_number()
        print("updated parameters: ", self.update_parameters)
    def showCounter(self):
        # Check the value of startWatch  variable to start or stop the Stop Watch
        if self.startWatch:
            # Increment counter by 1
            self.counter += 1

            # Count and set the time counter value
            cnt = int((self.counter/10 - int(self.counter/10))*10)
            self.count = '0' + str(cnt)

            # Set the second value
            if int(self.counter/10) < 10 :
                self.second = '0' + str(int(self.counter / 10))
            else:
                self.second = str(int(self.counter / 10))
                # Set the minute value
                if self.counter / 10 == 60.0 :
                    self.second == '00'
                    self.counter = 0
                    min = int(self.minute) + 1
                    if min == self.MAX_TIME:
                        self.close()
                    if min < 10 :
                        self.minute = '0' + str(min)
                    else:
                        self.minute = str(min)
        #if min == self.MAX_TIME:
            #print('hi')
            #self.close()

        # Merge the mintue, second and count values
        text = self.minute + ':' + self.second + ':' + self.count
        # Display the stop watch values in the label
        self.time_label.setText('<h1 style="color:black">' + text + '</h1>')

    def pause(self):
        if self.pauseWatch.text() == 'Pause':
            self.pauseWatch.setText('Reprendre')
            self.startWatch = False
            self.end_of_stim = True
        else:
            self.startWatch = True
            self.pauseWatch.setText('Pause')
            self.end_of_stim = False

    def clicked_stop(self):
        self.end_of_stim = True
        self.close()
