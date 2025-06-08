import os
import requests
from urllib.parse import unquote
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
            
            self.finished_signal.emit(True, "Download concluído com sucesso")
        except Exception as e:
            self.finished_signal.emit(False, str(e))

class Downloader:
    def __init__(self, main_window):
        self.main_window = main_window
        self.download_thread = None
    
    def downloading(self, download_url, folder):
        self.options_window = QWidget()
        self.options_window.setWindowTitle("Download de Arquivo")
        self.options_window.setFixedSize(400, 150)
        
        main_window_rect = self.main_window.frameGeometry()
        self.options_window.move(main_window_rect.center() - self.options_window.rect().center())
        
        layout = QVBoxLayout(self.options_window)
        
        title_label = QLabel("Baixando arquivo...")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 18px; 
            font-weight: bold; 
            margin-bottom: 15px;
            color: #333;
        """)
        layout.addWidget(title_label)
        
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
        
        self.status_label = QLabel("Preparando download...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #666; margin-top: 10px;")
        layout.addWidget(self.status_label)
        
        self.options_window.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.options_window.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.options_window.show()
        
        self.start_download(download_url, folder)

    def start_download(self, download_url, folder):
        # Extrai o nome do arquivo da URL
        filename = unquote(download_url.split('/')[-1])
        save_path = os.path.join(os.path.expanduser('~'), '.canaryClient', folder, filename)
        
        self.download_thread = DownloadThread(download_url, save_path)
        self.download_thread.progress_signal.connect(self.update_progress)
        self.download_thread.finished_signal.connect(self.download_finished)
        self.download_thread.start()

    def update_progress(self, progress, status):
        self.progress_bar.setValue(progress)
        self.status_label.setText(status)

    def download_finished(self, success, message):
        if success:
            self.status_label.setText("Download concluído!")
            self.progress_bar.setValue(100)
            QMessageBox.information(self.main_window, "Sucesso", "Arquivo baixado com sucesso!")
        else:
            self.status_label.setText(f"Erro: {message}")
            self.progress_bar.setStyleSheet("QProgressBar::chunk { background-color: #d9534f; }")
            QMessageBox.critical(self.main_window, "Erro", f"Ocorreu um erro: {message}")
        self.options_window.close()