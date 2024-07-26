from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTextEdit, QPushButton, QMessageBox, QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt
from gtts import gTTS
from src.translator import translate_maya_to_spanish, translate_spanish_to_maya
from src.feedback import store_feedback  
import pyttsx3
import pygame
import tempfile

class MayaToSpanishTranslator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Traductor Maya-Español / tuk'ulka'an Maayá-Español")
        self.setFixedSize(1000, 430)
        
        ## Configuración del fondo de la ventana principal
        self.background_label = QLabel(self)
        pixmap = QPixmap('img/background.jpg')
        self.background_label.setPixmap(pixmap)
        self.background_label.setScaledContents(True)
        self.background_label.setGeometry(0, 0, 1000, 430)

        ## Inicialización del motor de texto a voz con pyttsx3
        self.engine = pyttsx3.init()
        self.initialize_pygame()  ## Inicialización de pygame para la reproducción de audio
        self.load_icon()  ## Carga del icono personalizado para la ventana

        ## Configuración inicial de la interfaz de traducción
        self.create_translation_interface()

        # Configurar pyttsx3 para utilizar voz en español si está disponible
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if "spanish" in voice.id.lower():
                self.engine.setProperty('voice', voice.id)
                break
        self.engine.setProperty('rate', 150)  # Puedes ajustar la velocidad de la voz aquí

    def translate_text(self):
        input_text = self.text_input.toPlainText().strip()
        
        if not input_text:
            QMessageBox.warning(self, "Texto Vacío", "Por favor ingrese texto para traducir.")
            return
        
        if self.direction_var == "maya_to_spanish":
            translated_text = translate_maya_to_spanish(input_text)
        else:
            translated_text = translate_spanish_to_maya(input_text)
        
        self.text_output.setPlainText(translated_text)

    def initialize_pygame(self):
        pygame.mixer.init()  ## Inicialización de pygame para la mezcla de audio

    def load_icon(self):
        icon_path = 'img/icono.ico'
        self.setWindowIcon(QIcon(icon_path))  ## Carga del icono para la ventana principal

    def clear_interface(self):
        ## Limpiar y reconfigurar la interfaz principal
        if hasattr(self, 'central_widget'):
            self.central_widget.deleteLater()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

    def create_translation_interface(self):
        ## Crear la interfaz de traducción con todos sus componentes
        self.clear_interface()

        main_layout = QVBoxLayout()
        h_layout = QHBoxLayout()

        left_layout = QVBoxLayout()

        self.input_label = QLabel("Ingrese texto (Maya) / Ōt'el Maayá")
        self.input_label.setFixedHeight(30)
        self.input_label.setFixedWidth(290)
        self.input_label.setStyleSheet("color: white;")
        font = QFont()
        font.setPointSize(12)
        self.input_label.setFont(font)
        left_layout.addWidget(self.input_label)

        self.text_input = QTextEdit()
        self.text_input.setStyleSheet("""
            QTextEdit {
                background-color: #FFFFFF;
                border: 1px solid #000000;
                border-radius: 10px;
                padding: 6px;
                font-size: 15px;
            }
        """)
        self.text_input.setFixedHeight(40)
        self.text_input.setFixedWidth(360)
        left_layout.addWidget(self.text_input)

        h_layout.addLayout(left_layout)

        ## Botón para cambiar la dirección de traducción
        self.reverse_button = QPushButton()
        self.reverse_button.setIcon(QIcon('img/reverse.png'))
        self.reverse_button.setIconSize(self.reverse_button.sizeHint())
        self.reverse_button.setFixedSize(40, 40)
        self.reverse_button.setStyleSheet("background-color: white;")
        self.reverse_button.clicked.connect(self.reverse_translation)
        self.reverse_button.setStyleSheet("""
            QPushButton:hover {
                border: 1px solid #000000;
                background-color: rgba(255, 255, 255, 150);
            }
        """)
        h_layout.addWidget(self.reverse_button)

        right_layout = QVBoxLayout()

        self.output_label = QLabel("Traducción (Español) / tuk'ulka'an Español")
        self.output_label.setFont(font)
        self.output_label.setFixedHeight(30)
        self.output_label.setFixedWidth(300)
        self.output_label.setStyleSheet("color: white;")
        right_layout.addWidget(self.output_label)

        output_layout = QHBoxLayout()

        self.text_output = QTextEdit()
        self.text_output.setStyleSheet("""
            QTextEdit {
                background-color: #FFFFFF;
                border: 1px solid #000000;
                border-radius: 10px;
                padding: 6px;
                font-size: 15px;
            }
        """)
        self.text_output.setReadOnly(True)
        self.text_output.setFixedHeight(40)
        self.text_output.setFixedWidth(360)
        output_layout.addWidget(self.text_output)

        ## Botón para reproducir la traducción en audio
        self.speaker_button = QPushButton("🔊")
        self.speaker_button.setFixedSize(40, 40)
        self.speaker_button.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF;
                border: 1px solid #000000;
                color: black;
                font-size: 20px;
                border-radius: 20px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 150);
            }
        """)
        self.speaker_button.clicked.connect(self.speak_translation)
        output_layout.addWidget(self.speaker_button)

        right_layout.addLayout(output_layout)

        h_layout.addLayout(right_layout)

        main_layout.addLayout(h_layout)

        ## Layout horizontal para los botones de acción
        button_layout = QHBoxLayout()

        ## Espaciador flexible a la izquierda
        button_layout.addStretch()

        ## Botón para iniciar la traducción
        self.translate_button = QPushButton("Traducir / tuk'ulka'an")
        self.translate_button.clicked.connect(self.translate_text)
        self.translate_button.setFixedSize(170, 40)
        self.translate_button.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF;
                border: 1px solid #000000;
                color: black;
                font-size: 12px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #E4E4E4;
            }
        """)
        button_layout.addWidget(self.translate_button)

        ## Espacio entre botones
        button_layout.addSpacing(30)

        ## Botón para enviar retroalimentación
        self.feedback_button = QPushButton("Enviar Retroalimentación")
        self.feedback_button.clicked.connect(self.show_feedback_interface)
        self.feedback_button.setFixedSize(200, 40)
        self.feedback_button.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF;
                border: 1px solid #000000;
                color: black;
                font-size: 12px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #E4E4E4;
            }
        """)
        button_layout.addWidget(self.feedback_button)

        ## Espaciador flexible a la derecha
        button_layout.addStretch()

        ## Añadir el layout de botones al layout principal
        main_layout.addLayout(button_layout)

        self.central_widget.setLayout(main_layout)

        self.direction_var = "maya_to_spanish"

    def reverse_translation(self):
        ## Cambiar la dirección de traducción entre Maya y Español
        current_direction = self.direction_var

        if current_direction == "maya_to_spanish":
            self.direction_var = "spanish_to_maya"
            self.input_label.setText("Ingrese texto en Español/ Ōt'el Español")
            self.output_label.setText("Traducción en Maya / tuk'ulka'an Maayá")
            QMessageBox.information(self, "Cambio de Dirección", "Ahora traducirá de Español a Maya.")
        else:
            self.direction_var = "maya_to_spanish"
            self.input_label.setText("Ingrese texto (Maya) / Ōt'el Maayá")
            self.output_label.setText("Traducción en Español / tuk'ulka'an Español")
            QMessageBox.information(self, "Cambio de Dirección", "Ahora traducirá de Maya a Español.")

        self.text_input.clear()
        self.text_output.clear()

    def show_feedback_interface(self):
        ## Mostrar la interfaz para ingresar retroalimentación
        self.clear_interface()

        self.layout = QVBoxLayout()

        feedback_label = QLabel("Ingrese su retroalimentación:")
        feedback_label.setStyleSheet("color:white;")
        font = QFont()
        font.setPointSize(13)
        feedback_label.setFont(font)
        self.layout.addWidget(feedback_label)

        self.feedback_text = QTextEdit()
        self.feedback_text.setStyleSheet("""
            QTextEdit {
                background-color: rgba(255, 255, 255, 150);
                border: 1px solid #000000;
                border-radius: 10px;
                padding: 6px;
                font-size: 15px;
            }
        """)
        self.layout.addWidget(self.feedback_text)

        button_layout = QHBoxLayout()

        ## Botón para regresar a la interfaz de traducción
        back_button = QPushButton("Regresar")
        back_button.clicked.connect(self.create_translation_interface)
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF;
                border: 1px solid #000000;
                color: black;
                font-size: 20px;
                border-radius: 20px;
            }
            QPushButton:hover {
                background-color: #E4E4E4;
            }
        """)
        button_layout.addWidget(back_button)
        
        ## Botón para enviar la retroalimentación
        send_feedback_button = QPushButton("Enviar")
        send_feedback_button.clicked.connect(self.send_feedback)
        send_feedback_button.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF;
                border: 1px solid #000000;
                color: black;
                font-size: 20px;
                border-radius: 20px;
            }
            QPushButton:hover {
                background-color: #E4E4E4;
            }
        """)
        button_layout.addWidget(send_feedback_button)

        self.layout.addLayout(button_layout)

        self.central_widget.setLayout(self.layout)

    def send_feedback(self):
        ## Enviar la retroalimentación ingresada por el usuario
        feedback = self.feedback_text.toPlainText().strip()
        if not feedback:
            QMessageBox.warning(self, "Espacio vacío", "No puedes dejar el espacio vacío.")
            return
        else:
            store_feedback(feedback)  ## Llamar a la función para almacenar la retroalimentación
        QMessageBox.information(self, "Retroalimentación", "Gracias por su retroalimentación.")
        self.create_translation_interface()  ## Regresar a la interfaz de traducción después de enviar

    def speak_translation(self):
        ## Reproducir la traducción en audio utilizando gTTS o pyttsx3 según la dirección de traducción
        translation = self.text_output.toPlainText().strip()
        if translation:
            if self.direction_var == "maya_to_spanish":
                tts = gTTS(text=translation, lang='es')
                with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_mp3:
                    temp_mp3.close()
                    tts.save(temp_mp3.name)
                    pygame.mixer.music.load(temp_mp3.name)
                    pygame.mixer.music.play()
            else:
                ## Reproducción de voz en Maya utilizando pyttsx3
                self.engine.say(translation)
                self.engine.runAndWait()
        else:
            QMessageBox.warning(self, "Sin texto", "No hay texto para reproducir.")
