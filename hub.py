import os
import requests
import downloader
from PyQt6.QtWidgets import (QMainWindow, QScrollArea, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLineEdit, QPushButton, QLabel, 
                            QFrame, QSizePolicy, QGridLayout)
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QFont

class GitHubFolderViewer(QMainWindow):
    item_clicked = pyqtSignal(str)  # Sinal emitido quando um item é clicado

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Modificações")
        self.setMinimumSize(600, 400)
        
        # Widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Layout principal
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # Barra de busca
        self.setup_search_bar()
        
        # Botões de categorias
        self.setup_category_buttons()
        
        # Área de rolagem para os itens
        self.setup_scroll_area()
        
        # Estilização
        self.setStyleSheet("""
            QFrame {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 10px;
                background-color: #f9f9f9;
            }
            QFrame:hover {
                background-color: #eef;
                border: 1px solid #aaa;
            }
            QPushButton {
                padding: 8px 15px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            .category-button {
                background-color: #2196F3;
            }
            .category-button:hover {
                background-color: #0b7dda;
            }
            QLineEdit {
                padding: 5px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
        """)

    def setup_search_bar(self):
        """Configura a barra de busca"""
        search_layout = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar itens...")
        self.search_input.textChanged.connect(self.filter_items)
        
        search_layout.addWidget(QLabel("Buscar:"))
        search_layout.addWidget(self.search_input)
        self.main_layout.addLayout(search_layout)

    def setup_category_buttons(self):
        """Configura os botões de categorias pré-definidas"""
        self.categories = [
            ("Mods", "mods", "https://github.com/neomin-2007/Canary-Launcher-Repository/tree/main/mods"),
            ("Resource Packs", "resourcepacks", "https://github.com/neomin-2007/Canary-Launcher-Repository/tree/main/resourcespack"),
            ("Shaders", "shaderpacks", "https://github.com/neomin-2007/Canary-Launcher-Repository/tree/main/shaders")
        ]
        
        button_layout = QHBoxLayout()
        
        for name, folder, url in self.categories:
            button = QPushButton(name)
            button.setProperty('class', 'category-button')
            button.clicked.connect(lambda checked, u=url, f=folder: self.load_github_folder(u, f))
            button_layout.addWidget(button)
        
        self.main_layout.addLayout(button_layout)

    def setup_scroll_area(self):
        """Configura a área de rolagem para os itens"""
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        
        self.items_container = QWidget()
        self.items_layout = QVBoxLayout(self.items_container)
        self.items_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.items_layout.setSpacing(10)
        
        self.scroll_area.setWidget(self.items_container)
        self.main_layout.addWidget(self.scroll_area)

    def load_github_folder(self, folder_url, folder_name):
        """Carrega os itens de uma pasta do GitHub"""
        try:
            # Limpa os itens atuais
            for i in reversed(range(self.items_layout.count())): 
                self.items_layout.itemAt(i).widget().setParent(None)
            
            # Obtém a lista de arquivos da API do GitHub
            api_url = self.convert_to_api_url(folder_url)
            response = requests.get(api_url)
            response.raise_for_status()
            items = response.json()
            
            # Adiciona cada item à lista
            for item in items:
                if item['type'] == 'file':  # Pode ajustar para incluir pastas também
                    self.add_item(item['name'], item['download_url'], folder_name)
            
        except Exception as e:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Erro", f"Falha ao carregar a pasta: {str(e)}")

    def convert_to_api_url(self, github_url):
        """Converte uma URL normal do GitHub para a URL da API"""
        parts = github_url.replace("https://github.com/", "").split("/")
        user, repo = parts[0], parts[1]
        path = "/".join(parts[4:]) if "tree" in parts else "/".join(parts[2:])
        return f"https://api.github.com/repos/{user}/{repo}/contents/{path}"

    def add_item(self, name, download_url, folder):
        """Adiciona um item à lista"""
        item_frame = QFrame()
        item_frame.setCursor(Qt.CursorShape.PointingHandCursor)
        
        layout = QHBoxLayout(item_frame)
        layout.setContentsMargins(10, 5, 10, 5)
        
        # Nome do item
        name_label = QLabel(name)
        name_label.setFont(QFont("Arial", 10))
        name_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        
        self.download = downloader.Downloader(self)

        # Botão de ação
        action_button = QPushButton("Baixar")
        action_button.setFixedSize(80, 40)
        action_button.clicked.connect(lambda: self.download.downloading(download_url, folder))
        
        layout.addWidget(name_label)
        layout.addWidget(action_button)
        
        self.items_layout.addWidget(item_frame)

    def filter_items(self, text):
        """Filtra os itens com base no texto da busca"""
        for i in range(self.items_layout.count()):
            item = self.items_layout.itemAt(i).widget()
            label = item.findChild(QLabel)
            if label:
                item.setVisible(text.lower() in label.text().lower())