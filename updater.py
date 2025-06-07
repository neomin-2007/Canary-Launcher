import os
import requests
import zipfile
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
                            QProgressBar, QMessageBox)
from PyQt6.QtCore import Qt

class DownloadThread(QThread):
    progress_signal = pyqtSignal(int, str)
    finished_signal = pyqtSignal(bool, str)
    
    def __init__(self, url, save_path):
        super().__init__()
        self.url = url
        self.save_path = save_path
    
    def run(self):
        try:
            os.makedirs(os.path.dirname(self.save_path), exist_ok=True)
            
            with requests.get(self.url, stream=True) as r:
                r.raise_for_status()
                total_size = int(r.headers.get('content-length', 0))
                downloaded_size = 0
                
                self.progress_signal.emit(0, f"Tamanho total: {total_size/1024/1024:.2f} MB")
                
                with open(self.save_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded_size += len(chunk)
                            progress = int((downloaded_size / total_size) * 100) if total_size > 0 else 0
                            self.progress_signal.emit(
                                progress, 
                                f"Baixando: {downloaded_size/1024/1024:.2f} MB de {total_size/1024/1024:.2f} MB"
                            )
            
            self.progress_signal.emit(100, "Descompactando arquivo...")
            extract_to = os.path.join(os.path.dirname(self.save_path))
            with zipfile.ZipFile(self.save_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
            
            os.remove(self.save_path)
            
            self.finished_signal.emit(True, "Download e extração concluídos")
        except Exception as e:
            self.finished_signal.emit(False, str(e))

class Updater:
    def __init__(self, main_window):
        self.main_window = main_window
        self.download_thread = None
    
    def downloading(self):
        self.options_window = QWidget()
        self.options_window.setWindowTitle("Instalação")
        self.options_window.setFixedSize(400, 150)
        
        # Centralizar a janela
        main_window_rect = self.main_window.frameGeometry()
        self.options_window.move(main_window_rect.center() - self.options_window.rect().center())
        
        layout = QVBoxLayout(self.options_window)
        
        # Título
        title_label = QLabel("Baixando arquivos...")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 18px; 
            font-weight: bold; 
            margin-bottom: 15px;
            color: #333;
        """)
        layout.addWidget(title_label)
        
        # Barra de progresso
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                height: 25px;
                text-align: center;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
            QProgressBar::chunk {
                background-color: #3c8527;
                width: 10px;
            }
        """)
        layout.addWidget(self.progress_bar)
        
        # Label de status
        self.status_label = QLabel("Preparando download...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #666; margin-top: 10px;")
        layout.addWidget(self.status_label)
        
        self.options_window.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.options_window.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.options_window.show()
        
        # Iniciar o download
        self.start_download()

    def start_download(self):
        # URL do arquivo para download
        download_url = "https://download1500.mediafire.com/leqbr20lqjmgNG_GbCwjy5_FVazpg1cnAEcpceixU9kJwAxVm6gozaOFfvfYy4xHHKdo0W3XfEOA9iwCe0NHRLgJgCvcXxDOtCve97OQzg6c29eM4uQvBHyVXWmKk5jfOZ19u2KtRh3-iNGLeXk029MGj_qBd8uDt6FxEsH9pbLiuA/howqy5jssbfh4t7/canaryClient.zip"
        # Caminho local para salvar o arquivo
        save_path = os.path.join(os.getenv('HOME'), '.canaryClient', 'CanaryClient.zip')
        
        # Criar thread para o download
        self.download_thread = DownloadThread(download_url, save_path)
        self.download_thread.progress_signal.connect(self.update_progress)
        self.download_thread.finished_signal.connect(self.download_finished)
        self.download_thread.start()

    def update_progress(self, progress, status):
        self.progress_bar.setValue(progress)
        self.status_label.setText(status)

    def download_finished(self, success, message):
        if success:
            self.status_label.setText("Download e extração concluídos!")
            self.progress_bar.setValue(100)
            # Fechar a janela após 2 segundos
            self.options_window.close()
            QMessageBox.information(self.main_window, "Sucesso", "Instalação concluída com sucesso!")
        else:
            self.status_label.setText(f"Erro: {message}")
            self.progress_bar.setStyleSheet("QProgressBar::chunk { background-color: #d9534f; }")
            QMessageBox.critical(self.main_window, "Erro", f"Ocorreu um erro: {message}")