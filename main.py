from PyQt6.QtWidgets import QMainWindow, QSlider, QBoxLayout, QHBoxLayout, QLineEdit, QApplication, QPushButton, QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QPixmap, QIcon, QFont
from PyQt6.QtCore import Qt, QSize
import launcher
import updater
import downloader
import hub
import os
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Canary Client")
        self.setFixedSize(1040, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        self.setup_title()
        self.setup_background(main_layout)
        self.setup_nickname_input(main_layout)
        self.setup_buttons()
        self.set_window_icon()
        
        self.nickname_input.setFocus()
        self.show()

        if not os.path.isdir(os.path.join(os.getenv('HOME'), '.canaryClient')):
            self.updater = updater.Updater(self)
            self.updater.downloading()
    
    def setup_title(self):

        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))

        banner_path = os.path.join(base_path, "assets/banner.png")
        
        banner_button = QPushButton(self)
        banner_button.setIcon(QIcon(banner_path))
        banner_button.setIconSize(QSize(200, 200))
        banner_button.setFixedSize(245, 245) 
        banner_button.setStyleSheet("QPushButton { border: none; }")
        banner_button.setGeometry((self.width() - 200) // 2, self.height() - 700, 40, 40)

    def setup_background(self, layout):

        layout.addSpacing(40)

        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
            
        image_path = os.path.join(base_path, "assets/background.png")
        pixmap = QPixmap(image_path)

        image_label = QLabel()
        image_label.setPixmap(pixmap)
        image_label.setMaximumSize(1040, 500)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label.setScaledContents(False)
        
        layout.addWidget(image_label)
        layout.addStretch()
    
    def setup_nickname_input(self, layout):
        nickname_layout = QVBoxLayout()
        
        nickname_label = QLabel("Nickname:")
        self.nickname_input = QLineEdit()
        self.nickname_input.setPlaceholderText("Digite seu nickname")
        self.nickname_input.setMaximumWidth(300)
        
        nickname_layout.addWidget(nickname_label)
        nickname_layout.addWidget(self.nickname_input)
        
        layout.addLayout(nickname_layout)
        layout.addStretch()
    
    def set_window_icon(self):
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
            
        icon_path = os.path.join(base_path, "assets/icon.png")
        
        if not os.path.exists(icon_path):
            icon_path = os.path.join(base_path, "assets/icon.ico")
        
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            print(f"Aviso: Arquivo de ícone não encontrado em {icon_path}")

    def setup_buttons(self):
        
        start_font = QFont()
        start_font.setBold(True)
        start_font.setPixelSize(24)
        
        start_button = QPushButton("INICIAR JOGO", self)
        start_button.setFont(start_font)
        start_button.pressed.connect(self.execute_launcher)
        start_button.setGeometry((self.width() - 250) // 2, self.height() - 80, 300, 55)
        
        start_button.setStyleSheet("""
    QPushButton {
        background-color: #3c8527;
        color: white;
        border-style: outset;
        border-width: 2px;
        border-radius: 10px;
        border-color: #6a6a6a;
        font-family: 'Minecraft', 'Arial', sans-serif;
        font-size: 20px;
        padding: 8px 16px;
        min-width: 200px;
        text-align: center;
    }
    QPushButton:hover {
        background-color: #4a9e2d;
        border-color: #7a7a7a;
    }
    QPushButton:pressed {
        background-color: #2a6a1a;
        border-style: inset;
        padding-top: 9px;
        padding-bottom: 7px;
    }
""")
        
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
            
        options_path = os.path.join(base_path, "assets/settings_icon.png")
        
        options_button = QPushButton(self)
        options_button.setIcon(QIcon(options_path))
        options_button.setIconSize(QSize(32, 32))
        options_button.setFixedSize(40, 40) 
        options_button.setStyleSheet("QPushButton { border: none; }")
        options_button.pressed.connect(self.execute_options)
        options_button.setGeometry((self.width() + 900) // 2, self.height() - 60, 40, 40)

        modification_path = os.path.join(base_path, "assets/modification_icon.png")
        
        modification_button = QPushButton(self)
        modification_button.setIcon(QIcon(modification_path))
        modification_button.setIconSize(QSize(32, 32))
        modification_button.setFixedSize(40, 40) 
        modification_button.setStyleSheet("QPushButton { border: none; }")
        modification_button.pressed.connect(self.execute_hub)
        modification_button.setGeometry((self.width() + 800) // 2, self.height() - 60, 40, 40)

        discord_path = os.path.join(base_path, "assets/discord_icon.png")
        
        discord_button = QPushButton(self)
        discord_button.setIcon(QIcon(discord_path))
        discord_button.setIconSize(QSize(128, 128))
        discord_button.setFixedSize(64, 64) 
        discord_button.setStyleSheet("QPushButton { border: none; }")
        discord_button.pressed.connect(self.execute_options)
        discord_button.setGeometry((self.width() + 875) // 2, self.height() - 550, 40, 40)
    
    def execute_launcher(self):
        nickname = self.nickname_input.text()
        
        if len(nickname) < 3:
            self.nickname_input.setText("")
            self.nickname_input.setPlaceholderText("O nickname deve ter ao menos 3 letras")
            return
        
        if len(nickname) > 16:
            self.nickname_input.setText("")
            self.nickname_input.setPlaceholderText("O nickname deve ter apenas 16 letras")
            return

        self.close()
        ram_value = self.ram_slider.value() if hasattr(self, 'ram_slider') else None
        launcher.execute(nickname, ram_value)

    def execute_hub(self):
        self.viewer = hub.GitHubFolderViewer()
        self.viewer.show()
        
        #self.viewer.item_clicked.connect(self.handle_item_clicked)
        
        #self.hub = downloader.Downloader(self)
        #self.hub.downloading("https://github.com/neomin-2007/Canary-Launcher-Repository/blob/main/mods/OptiFine-1.8.9_HD_U_M5.jar")
    
    def execute_options(self):

        self.options_window = QWidget()
        self.options_window.setWindowTitle("Opções")
        self.options_window.setFixedSize(400, 150)
        
        main_window_rect = self.frameGeometry()
        self.options_window.move(main_window_rect.center() - self.options_window.rect().center())
        
        layout = QVBoxLayout(self.options_window)
        
        title_label = QLabel("Configurações de RAM")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 18px; 
            font-weight: bold; 
            margin-bottom: 15px;
            color: #333;
        """)
        layout.addWidget(title_label)
        
        ram_layout = QVBoxLayout()
        
        value_layout = QHBoxLayout()
        self.ram_value_label = QLabel("1024 MB")
        self.ram_value_label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #3c8527;
            margin-bottom: 10px;
        """)
        value_layout.addStretch()
        value_layout.addWidget(self.ram_value_label)
        value_layout.addStretch()
        ram_layout.addLayout(value_layout)
        
        self.ram_slider = QSlider(Qt.Orientation.Horizontal)
        self.ram_slider.setRange(512, 4096)
        self.ram_slider.setValue(1024)
        self.ram_slider.setTickInterval(512)
        self.ram_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.ram_slider.setStyleSheet("""
            QSlider {
                height: 30px;
            }
            QSlider::groove:horizontal {
                height: 8px;
                background: #ddd;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                width: 20px;
                height: 20px;
                background: #3c8527;
                margin: -6px 0;
                border-radius: 10px;
            }
        """)
        
        self.ram_slider.valueChanged.connect(
            lambda value: self.ram_value_label.setText(f"{value} MB")
        )
        ram_layout.addWidget(self.ram_slider)
        
        min_max_layout = QHBoxLayout()
        min_label = QLabel("512 MB")
        min_label.setStyleSheet("color: #666;")
        max_label = QLabel("4096 MB")
        max_label.setStyleSheet("color: #666;")
        
        min_max_layout.addWidget(min_label)
        min_max_layout.addStretch()
        min_max_layout.addWidget(max_label)
        ram_layout.addLayout(min_max_layout)
        
        layout.addLayout(ram_layout)
        
        self.options_window.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.options_window.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        
        self.options_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
        
    icon_path = os.path.join(base_path, "icon.ico")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    window = MainWindow()
    app.exec()