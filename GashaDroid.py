import sys
import webbrowser
import subprocess
import frida
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
from termcolor import colored
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QLabel, QListWidget, QPushButton, QStackedWidget,
    QProgressBar, QHBoxLayout, QFrame, QTextEdit,
    QLineEdit, QComboBox, QFileDialog, QTableWidget, QTableWidgetItem,
    QMessageBox, QTabWidget, QStyle
)

from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap


            
APK_PATH = "/path/to/your/apk/file.apk"  
MOBS_F_SERVER_URL = "https://mobsf.live/"


class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(900, 950) 
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        self.image_label = QLabel(self)
        pixmap = QPixmap("SS.png").scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)
        layout.addWidget(self.image_label, alignment=Qt.AlignCenter)

        self.progress = QProgressBar(self)
        self.progress.setAlignment(Qt.AlignCenter)
        self.progress.setRange(0, 100)
        self.progress.setTextVisible(False)
        self.progress.setStyleSheet("""
            QProgressBar {
                background-color: #444; 
                border-radius: 10px; 
                height: 20px;
                margin-top: 20px;
            }
            QProgressBar::chunk {
                background-color: #1de0f2; 
                border-radius: 10px;
            }
        """)

       
        layout.addWidget(self.progress, alignment=Qt.AlignCenter)

        self.setLayout(layout)

      
        screen_geometry = QApplication.desktop().screenGeometry()
        self.move((screen_geometry.width() - self.width()) // 2, (screen_geometry.height() - self.height()) // 2)

        self.show()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_loading)
        self.timer.start(30)

        self.loading_value = 0
        QTimer.singleShot(3000, self.close)
        QTimer.singleShot(3000, self.show_main_window)

    def update_loading(self):
        self.loading_value += 1
        self.progress.setValue(self.loading_value)
        if self.loading_value >= 100:
            self.timer.stop()

    def show_main_window(self):
        self.main_window = MainWindow() 
        self.main_window.show()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GashaDroid")
        self.setGeometry(100, 100, 800, 600)
        self.showMaximized()

        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)

        
        self.sidebar = QFrame()
        self.sidebar.setStyleSheet("background-image: url('SBI.jpg');")
        self.sidebar.setFixedWidth(300)
        self.sidebar_layout = QVBoxLayout(self.sidebar)

        
        self.toggle_button = QPushButton("☰", self)
        self.toggle_button.setStyleSheet("border-radius: 15px; background-color: #4CAF50; color: white; font-size: 20px;")
        self.toggle_button.setFixedSize(30, 30)
        self.toggle_button.clicked.connect(self.toggle_sidebar)
        self.sidebar_layout.addWidget(self.toggle_button, alignment=Qt.AlignTop)

        
        self.logo_label = QLabel(self)
        self.logo_label.setPixmap(QPixmap("path/to/your/logo.png").scaled(200, 100, Qt.KeepAspectRatio))
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.sidebar_layout.addWidget(self.logo_label)

        
        self.options_list = QListWidget()
        self.options_list.setStyleSheet("font-size: 16px; color: white;")
        self.options_list.addItems([
            "Emulator Detection and Bypass",
            "Root Detection Bypass",
            "Developer Mode Detection Bypass",
            "Certificate Pinning Bypass",
            "Inject Code with Frida",
            "Reverse Engineer The Application",
            "Analyze APK with MobSF",
            "Report",
            "About GashaDroid",
            "Exit"
        ])
        self.options_list.setCurrentRow(0)
        self.options_list.currentItemChanged.connect(self.handle_selection)
        self.sidebar_layout.addWidget(self.options_list)

        self.main_layout.addWidget(self.sidebar)

        
        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)

        
        self.create_pages()

        self.setStyleSheet("background-color: #2E2E2E; color: white;")

    def toggle_sidebar(self):
        if self.sidebar.width() == 300:
            self.sidebar.setFixedWidth(150)
        else:
            self.sidebar.setFixedWidth(300)

    def handle_selection(self, current, previous):
        if current:
            index = self.options_list.row(current)
            self.stacked_widget.setCurrentIndex(index)
            if current.text() == "Exit":
                self.close()

    def create_pages(self):
        self.create_emulator_page()
        self.create_root_page()
        self.create_developer_mode_page()
        self.create_certificate_pinning_page()
        self.create_inject_code_page()
        self.create_reverse_engineer_page()
        self.create_analyze_apk_page()
        self.create_report_page()
        self.create_about_page()
    


    def create_emulator_page(self):
        page = QWidget()
        layout = QVBoxLayout()

     
        page.setStyleSheet("background-color: #2E2E2E;")

      
        header_label = QLabel("<h2>Emulator Detection and Bypass</h2>")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-family: Arial, sans-serif;
                font-weight: bold;
                color: #1de0f2;
            }
        """)

      
        description = QLabel(
            "<p><br>This feature detects if the app runs on an emulator or a real device. Emulators can be exploited, so "
            "detection helps secure real-world app scenarios.</p>"
            "<p>This tool works by bypassing emulator detection by modifying the build properties of the emulator <br>"
            "And utilizing a Frida script in the background to make the app believe it is running on a real device.</p>"
            "<p>Starting the <strong>emulator detection bypass</strong> initiates checks to verify the device's authenticity. "
            "This is key for a comprehensive <strong>security assessment</strong>.</p>"
        )
        description.setStyleSheet("""
            QLabel {
                font-size: 22px;
                font-family: Arial, sans-serif;
                font-weight: normal;
                color: white;
                line-height: 1.6;
                margin-bottom: 20px;
            }
            p {
                font-size: 16px;
                color: #CCCCCC;
                margin-bottom: 15px;
            }
            strong {
                font-weight: bold;
                color: #FF9F00;
            }
        """)

       
        emstart_button = QPushButton("Start Emulator Detection Bypass")
        emstart_button.setStyleSheet("""
            QPushButton {
                font-size: 0px;
                font-family: Arial, sans-serif;
                font-weight: bold;
                background-color: #25becc;
                color: white;
                border: 2px solid #25becc;
                border-radius: 5px;
                padding: 10px 20px;
                min-width: 250px;
            }
            QPushButton:hover {
                background-color: #1ab8d0;
            }
            QPushButton:pressed {
                background-color: #25becc;
                padding: 8px 18px;
            }
        """)
        emstart_button.setFixedSize(250, 40)

       
        self.input_field11 = QLineEdit()
        self.input_field11.setPlaceholderText("Enter Package Name...")
        self.input_field11.setStyleSheet("""
            QLineEdit {
                font-size: 16px;
                padding: 10px;
                border: 2px solid #25becc;
                border-radius: 5px;
                background-color: #3A3A3A;
                color: white;
            }
            QLineEdit:focus {
                border-color: #1ab8d0;
            }
        """)
        self.input_field11.setFixedSize(300, 40)

        self.progress_bar1 = QProgressBar()
        self.progress_bar1.setRange(0, 100)
        self.progress_bar1.setValue(0)  
        self.progress_bar1.setTextVisible(True)
        self.progress_bar1.setStyleSheet("""
            QProgressBar {
                color: white;
                background-color: #4A4A4A;
                border-radius: 5px;
            }
            QProgressBar::chunk {
                background-color: #FF9F00;
                border-radius: 5px;
            }
        """)

    
        layout.addWidget(header_label)  
        layout.addWidget(description)  
        layout.addWidget(self.input_field11)  
        layout.addWidget(emstart_button) 

        layout.addStretch()

        layout.addWidget(self.progress_bar1)  

      
        layout.setAlignment(Qt.AlignTop)

    
        layout.setAlignment(self.progress_bar1, Qt.AlignBottom)

        
        emstart_button.clicked.connect(self.start_emulator_detection_and_bypass)

        page.setLayout(layout)
        self.stacked_widget.addWidget(page)

    def emulator_detection_and_bypass(self, TARGET_PACKAGE):
        print(colored("Starting emulator detection and bypass attempt...", 'blue'))
        session = None 

        try:
            print(colored("Setting system properties to attempt emulator bypass...", 'blue'))
            result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
            if "device offline" in result.stdout:
                QMessageBox.warning(self, "Device Status", "ADB device is offline. Reconnect the device and try again.")
                return

            try:
                subprocess.run(["adb", "shell", "su", "-c", "chmod 644 /system/build.prop"], check=True)
                subprocess.run(["adb", "shell", "setprop", "ro.build.selinux", "1"], check=True)
                subprocess.run(["adb", "shell", "setprop", "ro.build.type", "user"], check=True)
                subprocess.run(["adb", "shell", "setprop", "ro.build.tags", "release-keys"], check=True)
                subprocess.run(["adb", "remount", "ro"], check=True)
                QMessageBox.information(self, "Success", "System properties set successfully.")
            except subprocess.CalledProcessError:
                QMessageBox.warning(self, "Warning", "Failed to modify system properties. Check if the device is rooted.")
                return

            print(colored("Attempting runtime bypass using Frida...", 'blue'))
            try:
                device = frida.get_usb_device()
                pid = device.spawn([TARGET_PACKAGE])
                session = device.attach(pid)

                script = session.create_script("""
                Java.perform(function () {
                    var target = Java.use("android.os.Build");
                    target.getProp.implementation = function (prop) {
                        if (prop.equals("ro.build.selinux") || prop.equals("ro.build.type") || prop.equals("ro.build.tags")) {
                            console.log("Bypassing emulator detection check for property: " + prop);
                            return "0";
                        }
                        return this.getProp(prop);
                    };
                });
                """)
                script.load()
                device.resume(pid)
                print(colored("Runtime emulator detection bypass completed successfully.", 'green'))
                QMessageBox.information(self, "Success", "Runtime emulator bypass applied successfully.")

            except frida.ServerNotRunningError:
                QMessageBox.warning(self, "Frida Error", "Frida server is not running on the device.")
            except frida.PermissionDeniedError:
                QMessageBox.warning(self, "Frida Error", "Permission denied when trying to attach to the app. Ensure you have the required permissions.")
            except Exception as e:
                print(colored(f"Unexpected error: {e}", 'red'))
                QMessageBox.warning(self, "Warning", "An unexpected error occurred during emulator bypass.")

        finally:
            if session:
                try:
                    session.detach()
                    print(colored("Frida session detached cleanly.", 'green'))
                except Exception as e:
                    print(colored(f"Error detaching Frida session: {e}", 'red'))

    def start_emulator_detection_and_bypass(self):
        TARGET_PACKAGE = self.input_field11.text().strip()
        if not TARGET_PACKAGE:
            QMessageBox.warning(self, "Input Error", "Please enter a package name.")
            return

        self.progress_bar1.setValue(10)
        for i in range(1, 101):
            QTimer.singleShot(i * 30, lambda val=i: self.progress_bar1.setValue(val))

        self.emulator_detection_and_bypass(TARGET_PACKAGE)

    def create_root_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        header_label = QLabel("<h2>Root Detection Bypass</h2>")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-family: Arial, sans-serif;
                font-weight: bold;
                color: #1de0f2;
                margin-bottom: 20px;
            }
        """)

        description = QLabel(
            "<p>This feature checks whether the device on which the application is running has been rooted.</p>"
            "<p>Rooting provides greater control over the device but also exposes it to significant security risks.</p>"
            "<p>Initiating root detection bypass performs checks to ensure app security by verifying device integrity.</p>"
        )
        description.setStyleSheet("""
            QLabel {
                font-size: 22px;
                font-family: Arial, sans-serif;
                font-weight: normal;
                color: white;
                line-height: 1.6;
                margin-bottom: 20px;
            }
            p {
                font-size: 16px;
                color: #CCCCCC;
                margin-bottom: 15px;
            }
        """)

        self.input_field222 = QLineEdit()
        self.input_field222.setPlaceholderText("Enter Package Name...")
        self.input_field222.setStyleSheet("""
            QLineEdit {
                font-size: 16px;
                padding: 10px;
                border: 2px solid #25becc;
                border-radius: 5px;
                background-color: #3A3A3A;
                color: white;
            }
            QLineEdit:focus {
                border-color: #1ab8d0;
            }
        """)
        self.input_field222.setFixedSize(300, 40)

        start_button = QPushButton("Start Root Detection Bypass")
        start_button.setStyleSheet("""
            QPushButton {
                font-size: 0px;
                font-family: Arial, sans-serif;
                font-weight: bold;
                background-color: #1de0f2;
                color: white;
                border: 2px solid #1de0f2;
                border-radius: 5px;
                padding: 10px 20px;
                min-width: 250px;
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: #17c8d1;
            }
            QPushButton:pressed {
                background-color: #1ab8d0;
                padding: 8px 18px;
            }
        """)
        start_button.setFixedSize(250, 60)

        self.progress_bar222 = QProgressBar()
        self.progress_bar222.setRange(0, 100)
        self.progress_bar222.setValue(0)  
        self.progress_bar222.setTextVisible(True)
        self.progress_bar222.setStyleSheet("""
            QProgressBar {
                color: white;
                background-color: #4A4A4A;
                border-radius: 5px;
                height: 26px;
                margin-top: 20px;
            }
            QProgressBar::chunk {
                background-color: #1de0f2;
                border-radius: 5px;
            }
        """)

        
        layout.addWidget(header_label)  
        layout.addWidget(description)    
        layout.addWidget(self.input_field222) 
        layout.addWidget(start_button)  

    
        layout.addStretch()

        layout.addWidget(self.progress_bar222)  

      
        layout.setAlignment(Qt.AlignTop)

      
        start_button.clicked.connect(self.start_root_detection)

        page.setLayout(layout)
        self.stacked_widget.addWidget(page)

    def start_root_detection(self):
        self.progress_bar222.setValue(0)
        TARGET_PACKAGE = self.input_field222.text().strip()
        
        if not TARGET_PACKAGE:
            QMessageBox.warning(self, "Input Error", "Please enter a package name.")
            return

        for i in range(1, 101):
            QTimer.singleShot(i * 30, lambda val=i: self.progress_bar22.setValue(val))
        
        
        self.root_detection_bypass(TARGET_PACKAGE)

    def root_detection_bypass(self, TARGET_PACKAGE):
        frida_commands = [
            f"frida --codeshare Q0120S/root-detection-bypass -f {TARGET_PACKAGE}",
            f"frida --codeshare KishorBal/multiple-root-detection-bypass -f {TARGET_PACKAGE}",
            f"frida --codeshare enovella/anti-frida-bypass -f {TARGET_PACKAGE}",
        ]

        print(colored("Attempting multiple root detection bypass methods...", 'blue'))

        for attempt, command in enumerate(frida_commands, start=1):
            print(colored(f"Executing Frida command attempt {attempt}...", 'blue'))
            
            try:
                result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
                print(colored(result.stdout, 'green'))
                print(colored(result.stderr, 'red'))
                QMessageBox.information(self, "Success", f"Frida command {attempt} executed successfully.")

            except subprocess.CalledProcessError as e:
                if "is not supported" in str(e) or "access denied" in str(e):
                    QMessageBox.warning(self, "Security Block", "Operation blocked due to strong security features.")
                    print(colored("Operation blocked due to strong security features.", 'red'))
                else:
                    QMessageBox.warning(self, "Execution Error", f"Error executing Frida command: {e}")
                    print(colored(f"Error executing Frida command: {e}", 'red'))

            except Exception as e:
                QMessageBox.warning(self, "Unexpected Error", f"Unexpected error occurred: {e}")
                print(colored(f"Unexpected error: {e}", 'red'))
  
    def create_developer_mode_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        header_label = QLabel("<h2>Developer Mode Detection Bypass</h2>")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-family: Arial, sans-serif;
                font-weight: bold;
                color: #1de0f2;
                margin-bottom: 20px;
            }
        """)

        description = QLabel(
            "<p>This feature checks if the device is operating in Developer Mode.<br><br>"
            "Developer Mode allows access to advanced features, useful for developers but potentially risky for security.<br><br>"
            "By initiating the <strong>developer mode detection bypass</strong>, the application performs checks to detect Developer Mode.<br><br>"
            "This helps ensure that the application remains secure.</p>"
        )
        description.setStyleSheet("""
            QLabel {
                font-size: 22px;
                font-family: Arial, sans-serif;
                font-weight: normal;
                color: white;
                line-height: 1.6;
                margin-bottom: 20px;
            }
            p {
                font-size: 16px;
                color: #CCCCCC;
                margin-bottom: 15px;
            }
            strong {
                font-weight: bold;
                color: #FF9F00;
            }
        """)

    
        self.input_field3 = QLineEdit()
        self.input_field3.setPlaceholderText("Enter Package Name...")
        self.input_field3.setStyleSheet("""
            QLineEdit {
                font-size: 16px;
                padding: 10px;
                border: 2px solid #25becc;
                border-radius: 5px;
                background-color: #3A3A3A;
                color: white;
            }
            QLineEdit:focus {
                border-color: #1ab8d0;
            }
        """)
        self.input_field3.setFixedSize(300, 40)

     
        start_button = QPushButton("Start Developer Mode Detection Bypass")
        start_button.setStyleSheet("""
            QPushButton {
                font-size: 0px;
                font-family: Arial, sans-serif;
                font-weight: bold;
                background-color: #1de0f2;
                color: white;
                border: 2px solid #1de0f2;
                border-radius: 5px;
                padding: 10px 20px;
                min-width: 250px;
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: #17c8d1;
            }
            QPushButton:pressed {
                background-color: #1ab8d0;
                padding: 8px 18px;
            }
        """)
        start_button.setFixedSize(340, 60)

        # Progress Bar
        self.progress_bar3 = QProgressBar()
        self.progress_bar3.setRange(0, 100)
        self.progress_bar3.setValue(0)  # Start at 0
        self.progress_bar3.setTextVisible(True)
        self.progress_bar3.setStyleSheet("""
            QProgressBar {
                color: white;
                background-color: #4A4A4A;
                border-radius: 5px;
                height: 26px;
                margin-top: 20px;
            }
            QProgressBar::chunk {
                background-color: #1de0f2;
                border-radius: 5px;
            }
        """)

      
        layout.addWidget(header_label) 
        layout.addWidget(description)  
        layout.addWidget(self.input_field3) 
        layout.addWidget(start_button)   

        
        layout.addStretch()

        layout.addWidget(self.progress_bar3) 

       
        start_button.clicked.connect(self.start_developer_mode_detection)

        page.setLayout(layout)
        self.stacked_widget.addWidget(page)

    def start_developer_mode_detection(self):
        self.progress_bar3.setValue(0)
        TARGET_PACKAGE = self.input_field3.text().strip()
        
        if not TARGET_PACKAGE:
            QMessageBox.warning(self, "Input Error", "Please enter a package name.")
            return

        for i in range(1, 101):
            QTimer.singleShot(i * 30, lambda val=i: self.progress_bar3.setValue(val))
        
        self.developer_mode_detection_bypass(TARGET_PACKAGE)

    def developer_mode_detection_bypass(self, TARGET_PACKAGE):
        frida_commands = [
            f"frida --codeshare Raphkitue/android-debug-mode-bypass -f {TARGET_PACKAGE}",
            f"frida --codeshare zionspike/bypass-developermode-check-android -f {TARGET_PACKAGE}",
        ]

        print(colored("Attempting developer mode detection bypass methods...", 'blue'))

        for attempt, command in enumerate(frida_commands, start=1):
            print(colored(f"Executing Frida command attempt {attempt}...", 'blue'))
            
            try:
                result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
                print(colored(result.stdout, 'green'))
                print(colored(result.stderr, 'red'))
                QMessageBox.information(self, "Success", f"Frida command {attempt} executed successfully.")

            except subprocess.CalledProcessError as e:
                if "is not supported" in str(e) or "access denied" in str(e):
                    QMessageBox.warning(self, "Security Block", "Operation blocked due to strong security features.")
                    print(colored("Operation blocked due to strong security features.", 'red'))
                else:
                    QMessageBox.warning(self, "Execution Error", f"Error executing Frida command: {e}")
                    print(colored(f"Error executing Frida command: {e}", 'red'))

            except Exception as e:
                QMessageBox.warning(self, "Unexpected Error", f"Unexpected error occurred: {e}")
                print(colored(f"Unexpected error: {e}", 'red'))

    def create_certificate_pinning_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        header_label = QLabel("<h2>Certificate Pinning Bypass</h2>")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-family: Arial, sans-serif;
                font-weight: bold;
                color: #1de0f2;
                margin-bottom: 20px;
            }
        """)

        description = QLabel(
            "<p>This feature bypasses SSL certificate pinning in mobile applications.<br><br>"
            "Certificate pinning prevents man-in-the-middle attacks by ensuring the app only accepts specific certificates.<br><br>"
            "By initiating the <strong>certificate pinning bypass</strong>, various techniques are applied to override this mechanism, "
            "allowing secure traffic interception for testing purposes.<br><br>"
            "This enables thorough security assessments, ensuring applications can be audited effectively.</p>"
        )
        description.setStyleSheet("""
            QLabel {
                font-size: 22px;
                font-family: Arial, sans-serif;
                font-weight: normal;
                color: white;
                line-height: 1.6;
                margin-bottom: 20px;
            }
            p {
                font-size: 16px;
                color: #CCCCCC;
                margin-bottom: 15px;
            }
            strong {
                font-weight: bold;
                color: #FF9F00;
            }
        """)

        self.input_field_cert = QLineEdit()
        self.input_field_cert.setPlaceholderText("Enter Target Package Name...")
        self.input_field_cert.setStyleSheet("""
            QLineEdit {
                font-size: 16px;
                padding: 10px;
                border: 2px solid #25becc;
                border-radius: 5px;
                background-color: #3A3A3A;
                color: white;
            }
            QLineEdit:focus {
                border-color: #1ab8d0;
            }
        """)
        self.input_field_cert.setFixedSize(300, 40)

        start_button = QPushButton("Start Certificate Pinning Bypass")
        start_button.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                font-family: Arial, sans-serif;
                font-weight: bold;
                background-color: #1de0f2;
                color: white;
                border: 2px solid #1de0f2;
                border-radius: 5px;
                padding: 10px 20px;
                min-width: 250px;
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: #17c8d1;
            }
            QPushButton:pressed {
                background-color: #1ab8d0;
                padding: 8px 18px;
            }
        """)
        start_button.setFixedSize(250, 60)

        self.progress_bar4 = QProgressBar()
        self.progress_bar4.setRange(0, 100)
        self.progress_bar4.setValue(0)
        self.progress_bar4.setTextVisible(True)
        self.progress_bar4.setStyleSheet("""
            QProgressBar {
                font-size: 0px;
                color: white;
                background-color: #4A4A4A;
                border-radius: 5px;
                text-align: center;
                height: 20px;
                margin-top: 20px;
            }
            QProgressBar::chunk {
                background-color: #1de0f2;
                border-radius: 5px;
            }
        """)

        layout.addWidget(header_label)
        layout.addWidget(description)
        layout.addWidget(self.input_field_cert)
        layout.addWidget(start_button)
        layout.addStretch()
        layout.addWidget(self.progress_bar4)

        start_button.clicked.connect(self.start_certificate_pinning_bypass)

        page.setLayout(layout)
        self.stacked_widget.addWidget(page)

    def start_certificate_pinning_bypass(self):
        self.progress_bar4.setValue(0)
        TARGET_PACKAGE = self.input_field_cert.text().strip()

        if not TARGET_PACKAGE:
            QMessageBox.warning(self, "Input Error", "Please enter a valid package name.")
            return

        for i in range(1, 101):
            QTimer.singleShot(i * 30, lambda val=i: self.progress_bar4.setValue(val))

        self.bypass_security_checks(TARGET_PACKAGE)

    def bypass_security_checks(self, TARGET_PACKAGE):
        frida_commands = [
            f"frida --codeshare pcipolloni/universal-android-ssl-pinning-bypass-with-frida -f {TARGET_PACKAGE}",
            f"frida --codeshare akabe1/frida-multiple-unpinning -f {TARGET_PACKAGE}",
            f"frida --codeshare KhanhPham2411/android-tcp-tracev2 -f {TARGET_PACKAGE}",
        ]

        print(colored("Attempting certificate pinning bypass...", 'blue'))

        try:
            device = frida.get_usb_device()
            pid = device.spawn([TARGET_PACKAGE])
            session = device.attach(pid)

            for attempt, command in enumerate(frida_commands, start=1):
                print(colored(f"Attempt {attempt}: Executing Frida command...", 'blue'))
                try:
                    result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
                    print(colored(result.stdout, 'green'))
                    print(colored(result.stderr, 'red'))
                    print(colored("Frida command executed successfully.", 'green'))

                except subprocess.CalledProcessError as e:
                    if "is not supported" in str(e) or "access denied" in str(e):
                        print(colored("Feature is secured; operation blocked due to strong security features.", 'red'))
                        QMessageBox.warning(self, "Security Block", "Operation blocked due to strong security features.")
                    else:
                        print(colored(f"Error executing Frida command: {e}", 'red'))
                        QMessageBox.warning(self, "Execution Error", f"Error executing Frida command: {e}")

                except Exception as e:
                    print(colored(f"Unexpected error: {e}", 'red'))
                    QMessageBox.warning(self, "Unexpected Error", f"Unexpected error: {e}")

            if os.path.exists(BURP_CERT_PATH):
                subprocess.run(["adb", "push", BURP_CERT_PATH, "/sdcard/Download/burp_cert.cer"], check=True)
                subprocess.run(["adb", "shell", "mv", "/sdcard/Download/burp_cert.cer", "/system/etc/security/cacerts/"], check=True)
                subprocess.run(["adb", "shell", "chmod", "644", "/system/etc/security/cacerts/burp_cert.cer"], check=True)
                print(colored("Burp Suite CA certificate installed successfully.", 'green'))
                QMessageBox.information(self, "Success", "Burp Suite CA certificate installed successfully.")
            else:
                print(colored("Burp Suite CA certificate not found. Check BURP_CERT_PATH.", 'red'))
                QMessageBox.warning(self, "Certificate Error", "Burp Suite CA certificate not found. Check the certificate path.")

        except Exception as e:
            print(colored(f"Error: {e}", 'red'))
            QMessageBox.warning(self, "Error", f"An error occurred: {e}")
            
        finally:
            try:
                session.detach()
            except Exception:
                pass

    def create_inject_code_page(self):
        page = QWidget()
        layout = QVBoxLayout()

      
        tab_widget = QTabWidget()
        tab_widget.setStyleSheet("""
            QTabWidget::pane { border: 1px solid #444; }
            QTabBar::tab { background-color: #2E2E2E; color: white; padding: 10px; border: 1px solid #444; border-bottom: none; }
            QTabBar::tab:selected { background-color: #3C3F41; border-top-left-radius: 5px; border-top-right-radius: 5px; }
        """)

      
        script_tab = QWidget()
        script_layout = QVBoxLayout()
        script_layout.setSpacing(12) 

        self.process_input = QLineEdit()
        self.process_input.setPlaceholderText("Enter Process ID or Package Name...")
        self.process_input.setStyleSheet("""
            QLineEdit {
                font-size: 14px;
                font-family: Arial, sans-serif;
                background-color: #333;
                color: white;
                border: 1px solid #555;
                padding: 8px;
                border-radius: 5px;
                margin-bottom: 10px;  /* Space between the input and button */
            }
        """)

        self.script_text_edit = QTextEdit()
        self.script_text_edit.setPlaceholderText("Enter your Frida script here...")
        self.script_text_edit.setStyleSheet("""
            QTextEdit {
                font-size: 14px;
                font-family: Arial, sans-serif;
                background-color: #333;
                color: white;
                border: 1px solid #555;
                padding: 8px;
                border-radius: 5px;
                margin-bottom: 10px;  /* Space between the input and button */
            }
        """)

      
        save_button = QPushButton("Save")
        save_button.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 5px;
                margin-right: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        save_button.clicked.connect(self.save_script)

      
        inject_button = QPushButton("Inject")
        inject_button.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
        """)
        inject_button.clicked.connect(self.inject_script)

    
        button_layout = QHBoxLayout()
        button_layout.addWidget(save_button)
        button_layout.addWidget(inject_button)

       
        script_layout.addWidget(self.process_input)
        script_layout.addWidget(self.script_text_edit)
        script_layout.addLayout(button_layout)
        script_tab.setLayout(script_layout)

       
        command_tab = QWidget()
        command_layout = QVBoxLayout()
        command_layout.setSpacing(12) 

        self.command_dropdown = QComboBox()
        self.command_dropdown.addItems(["Command 1", "Command 2", "Command 3"])
        self.command_dropdown.setStyleSheet("""
            QComboBox {
                font-size: 14px;
                background-color: #333;
                color: white;
                padding: 8px;
                border: 1px solid #555;
                border-radius: 5px;
            }
            QComboBox QAbstractItemView {
                background-color: #333;
                color: white;
            }
        """)

        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText("Enter custom command here...")
        self.command_input.setStyleSheet("""
            QLineEdit {
                font-size: 14px;
                font-family: Arial, sans-serif;
                background-color: #333;
                color: white;
                border: 1px solid #555;
                padding: 8px;
                border-radius: 5px;
                margin-bottom: 10px;
            }
        """)

        add_command_button = QPushButton("Add")
        add_command_button.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                background-color: #FF9800;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 5px;
                margin-right: 10px;
            }
            QPushButton:hover {
                background-color: #e68900;
            }
        """)
        add_command_button.clicked.connect(lambda: self.command_dropdown.addItem(self.command_input.text()))

        run_command_button = QPushButton("Run")
        run_command_button.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                background-color: #9C27B0;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #8e24aa;
            }
        """)
        run_command_button.clicked.connect(self.run_command)

       
        command_button_layout = QHBoxLayout()
        command_button_layout.addWidget(add_command_button)
        command_button_layout.addWidget(run_command_button)

       
        command_layout.addWidget(self.command_dropdown)
        command_layout.addWidget(self.command_input)
        command_layout.addLayout(command_button_layout) 
        command_tab.setLayout(command_layout)

      
        tab_widget.addTab(script_tab, "Script")
        tab_widget.addTab(command_tab, "Command")

        layout.addWidget(tab_widget)
        page.setLayout(layout)
        self.stacked_widget.addWidget(page)

    def inject_script(self):
        script = self.script_text_edit.toPlainText()
        process = self.process_input.text()

        if script and process:
            try:
                
                self.inject_code_with_frida(process, script)
                QMessageBox.information(self, "Success", "Script injected successfully.")
            except Exception as e:
                QMessageBox.warning(self, "Injection Error", f"Failed to inject script: {e}")
        else:
            QMessageBox.warning(self, "Input Error", "Both script and process ID/package name must be provided.")

    def save_script(self):
        script = self.script_text_edit.toPlainText()
        if script:
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Script", "", "JavaScript Files (*.js)", options=options)
            if file_path:
                try:
                    with open(file_path, 'w') as file:
                        file.write(script)
                    QMessageBox.information(self, "Saved", "Script saved successfully.")
                except Exception as e:
                    QMessageBox.warning(self, "Save Error", f"Failed to save the script: {e}")
        else:
            QMessageBox.warning(self, "Save Error", "No script content to save.")

    def run_command(self):
        selected_command = self.command_dropdown.currentText()
        custom_command = self.command_input.text()

        if custom_command:
            print(f"Running custom command: {custom_command}")
            QMessageBox.information(self, "Command", f"Custom command executed: {custom_command}")
        elif selected_command:
            print(f"Running predefined command: {selected_command}")
            QMessageBox.information(self, "Command", f"Predefined command executed: {selected_command}")
        else:
            QMessageBox.warning(self, "Command Error", "No command provided.")

    def inject_code_with_frida(self, package_name, script):
        device = frida.get_local_device()

        try:
            
            process = device.attach(package_name)
            print(f"Attached to process with PID {process.pid}")

           
            frida_script = process.create_script(script)

            def on_message(message, data):
                if message['type'] == 'error':
                    print(f"Error: {message['stack']}")
                elif message['type'] == 'send':
                    print(f"Send: {message['payload']}")
                elif message['type'] == 'exit':
                    print("Exited")

           
            frida_script.on('message', on_message)

            
            frida_script.load()
            sys.stdin.read()

        except Exception as e:
            print(f"Failed to attach to the process: {e}")
            raise e


    def create_reverse_engineer_page(self):
       
        page = QWidget()
        layout = QVBoxLayout()

        
        tab_widget = QTabWidget()

       
        editor_tab = QWidget()
        editor_layout = QVBoxLayout()

      
        self.file_text_edit = QTextEdit()
        self.file_text_edit.setPlaceholderText("Decompiled APK content will appear here...")
        self.file_text_edit.setStyleSheet("""
            QTextEdit {
                font-size: 14px;
                font-family: Arial, sans-serif;
                background-color: #2E2E2E;
                color: white;
                border: 1px solid #444;
                padding: 10px;
                border-radius: 5px;
            }
        """)

        
        decompile_button = QPushButton("Decompile APK")
        decompile_button.setFixedSize(150, 40)
        decompile_button.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                padding: 6px;
                background-color: #007BFF;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        decompile_button.clicked.connect(self.decompile_apk)

       
        save_button = QPushButton("Save")
        save_button.setFixedSize(100, 40)
        save_button.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                padding: 6px;
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        save_button.clicked.connect(self.save_to_file)

       
        build_run_button = QPushButton("Build and Run")
        build_run_button.setFixedSize(150, 40)
        build_run_button.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                padding: 6px;
                background-color: #FFC107;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #e0a800;
            }
        """)
        build_run_button.clicked.connect(self.build_and_run)

       
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        button_layout.setAlignment(Qt.AlignCenter)
        button_layout.addWidget(decompile_button)
        button_layout.addWidget(save_button)
        button_layout.addWidget(build_run_button)

        
        editor_layout.addLayout(button_layout)
        editor_layout.addWidget(self.file_text_edit)

        editor_tab.setLayout(editor_layout)
        tab_widget.addTab(editor_tab, "Editor")

       
        layout.addWidget(tab_widget)
        page.setLayout(layout)
        self.stacked_widget.addWidget(page)

    def decompile_apk(self):
        try:
            options = QFileDialog.Options()
            file_name, _ = QFileDialog.getOpenFileName(self, "Open APK File", "", "APK Files (*.apk);;All Files (*)", options=options)
            if file_name:
                
                with open(file_name, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.file_text_edit.setPlainText(content)
                self.current_file = file_name
                QMessageBox.information(self, "Decompiled", "APK decompiled successfully!")
            else:
                QMessageBox.warning(self, "File Error", "No APK file selected.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred during decompiling: {str(e)}")

    def save_to_file(self):
        try:
            if hasattr(self, 'current_file') and self.current_file:
                content = self.file_text_edit.toPlainText()
                with open(self.current_file, 'w', encoding='utf-8') as file:
                    file.write(content)
                QMessageBox.information(self, "Saved", "File saved successfully.")
            else:
                QMessageBox.warning(self, "Save Error", "No file opened to save.")
        except Exception as e:
            QMessageBox.critical(self, "Save Error", f"An error occurred while saving the file: {e}")

    def build_and_run(self):
        try:
            
            QMessageBox.information(self, "Build and Run", "Building and running the application...")

        except Exception as e:
            QMessageBox.critical(self, "Build Error", f"An error occurred during the build and run process: {str(e)}")
   
    def create_analyze_apk_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        

        launch_mobsf_button = QPushButton("Select APK and Launch MobSF")
        launch_mobsf_button.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                padding: 10px;
                background-color: #007BFF;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        launch_mobsf_button.clicked.connect(self.select_apk_and_launch_mobsf)

        
        self.web_view = QWebEngineView()
        self.web_view.setUrl(QUrl(MOBS_F_SERVER_URL))

        

        
        layout.addWidget(self.web_view)
        

        page.setLayout(layout)
        self.stacked_widget.addWidget(page)

    def select_apk_and_launch_mobsf(self):
        
        apk_file, _ = QFileDialog.getOpenFileName(self, "Select APK File", "", "APK Files (*.apk);;All Files (*)")
        if apk_file:
            self.apk_path = apk_file 
            self.launch_mobsf() 

    def launch_mobsf(self):
        try:
            
            url = MOBS_F_SERVER_URL 
            self.web_view.setUrl(QUrl(url)) 

           
            self.analyze_apk_with_mobsf(self.apk_path)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to launch MobSF: {str(e)}")

    def analyze_apk_with_mobsf(self, apk_path):
        print("Starting APK analysis with MobSF...")
        try:
            
            static_analysis_command = ["curl", "-F", f"file=@{apk_path}", f"{MOBS_F_SERVER_URL}/api/v1/upload"]
            subprocess.run(static_analysis_command, check=True)
            print("Static analysis completed.")

           
            dynamic_analysis_command = ["curl", "-X", "POST", f"{MOBS_F_SERVER_URL}/api/v1/dynamic/start"]
            subprocess.run(dynamic_analysis_command, check=True)
            print("Dynamic analysis completed.")

        except subprocess.CalledProcessError as e:
            print(f"Error during APK analysis with MobSF: {e}")
            QMessageBox.critical(self, "Analysis Error", f"An error occurred during the APK analysis: {e}")
        
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            QMessageBox.critical(self, "Unexpected Error", f"An unexpected error occurred: {e}")
    
    def create_report_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        heading = QLabel("<h2>Penetration Test Report</h2>")
        heading.setAlignment(Qt.AlignCenter)
        heading.setStyleSheet("color: white;")

        description = QLabel("Below is a template for a penetration test report. You can fill in the details of each test conducted.")
        description.setAlignment(Qt.AlignCenter)
        description.setStyleSheet("font-size: 16px; color: white; padding-bottom: 10px;")

        self.report_table = QTableWidget()
        self.report_table.setRowCount(5)
        self.report_table.setColumnCount(4)
        self.report_table.setHorizontalHeaderLabels(["Test Item", "Description", "Status", "Recommendation"])

        self.report_table.setStyleSheet("""
            QTableWidget {
                border: none;
                font-size: 16px;
                font-family: 'Segoe UI', sans-serif;
                background-color: transparent;
                color: white;
            }
            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid #444;
            }
            QTableWidget::item:selected {
                background-color: transparent;
            }
            QTableWidget::horizontalHeader {
                background-color: transparent;
                color: white;
                font-weight: bold;
                padding: 12px;
                font-size: 18px;
                border: none;
            }
            QTableWidget::verticalHeader {
                background-color: transparent;
                color: white;
                padding: 12px;
                font-size: 16px;
                border: none;
            }
        """)

        test_data = [
            ["Emulator Check", "Check if app is running in emulator.", "Pass", "No action needed."],
            ["Root Check", "Check if the device is rooted.", "Fail", "Consider using a non-rooted device."],
            ["Network Security", "Test SSL pinning.", "Pass", "Secure connection."],
        ]

        for row_idx, row_data in enumerate(test_data):
            for col_idx, item in enumerate(row_data):
                self.report_table.setItem(row_idx, col_idx, QTableWidgetItem(item))

        save_button = QPushButton("Save Report")
        save_button.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                font-family: 'Segoe UI', sans-serif;
                padding: 12px 30px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                transition: background-color 0.3s;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #388E3C;
            }
        """)
        save_button.clicked.connect(self.save_report)

        button_layout = QHBoxLayout()
        button_layout.addWidget(save_button, alignment=Qt.AlignCenter)

        layout.addWidget(heading)
        layout.addWidget(description)
        layout.addWidget(self.report_table)
        layout.addLayout(button_layout)

        page.setLayout(layout)
        self.stacked_widget.addWidget(page)

    def save_report(self):
      
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Report", "", "Text Files (*.txt);;CSV Files (*.csv)", options=options)

        if file_path:
            try:
                with open(file_path, 'w') as file:
                   
                    for row in range(self.report_table.rowCount()):
                        row_data = []
                        for col in range(self.report_table.columnCount()):
                            row_data.append(self.report_table.item(row, col).text())
                        file.write(",".join(row_data) + "\n")

                print(f"Report saved successfully to {file_path}")
            except Exception as e:
                print(f"Failed to save the report: {e}")    
 
    def create_about_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        tab_widget = QTabWidget()

        about_tab = QWidget()
        about_layout = QVBoxLayout()

        about_text = QLabel(
            "<h2>About GashaDriod</h2>"
            "<p>GashaDriod is a comprehensive tool designed for Android application security testing and analysis.<br><br>"
            "<br>Providing a user-friendly interface, "
            "the security posture of their Android applications.<br><br>"
            "Key features include:<br>"
            "- APK Analysis with MobSF<br>"
            "- Certificate Pinning Bypass<br>"
            "- Emulator Detection and Bypass<br>"
            "- Developer Mode Detection Bypass<br><br>"
            "With a focus on enhancing application security, AndroMermari aims to empower users to identify and mitigate potential vulnerabilities "
            "before deployment.</p>"
        )
        about_text.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-family: Arial, sans-serif;
                color: white;
                line-height: 1.6;
            }
            p {
                margin-bottom: 15px;
            }
        """)

        about_layout.addWidget(about_text)
        about_tab.setLayout(about_layout)

        command_dict_tab = QWidget()
        command_dict_layout = QVBoxLayout()

        command_dict_text = QLabel(
            "<h2>Command Dictionary</h2>"
            "<p>frida --codeshare Q0120S/root-detection-bypass -f TARGET_PACKAGE</p>"
            "<ul>"
            "<li><b>frida --codeshare KishorBal/multiple-root-detection-bypass -f TARGET_PACKAGE</li>"
            "<li><b>frida --codeshare enovella/anti-frida-bypass -f TARGET_PACKAGE</li>"
            "<li><b>frida --codeshare KishorBal/multiple-root-detection-bypass -f TARGET_PACKAGE</li>"
            "<li><b>frida --codeshare KishorBal/multiple-root-detection-bypass -f TARGET_PACKAGE</li>"
            "<li><b>frida --codeshare KishorBal/multiple-root-detection-bypass -f TARGET_PACKAGE</li>"
            "<li><b>frida --codeshare enovella/anti-frida-bypass -f TARGET_PACKAGE</li>"
            "<li><b>frida --codeshare KishorBal/multiple-root-detection-bypass -f TARGET_PACKAGE</li>"
            "<li><b>frida --codeshare KishorBal/multiple-root-detection-bypass -f TARGET_PACKAGE</li>"
            "<li><b>frida --codeshare KishorBal/multiple-root-detection-bypass -f TARGET_PACKAGE</li>"
            "<li><b>frida --codeshare enovella/anti-frida-bypass -f TARGET_PACKAGE</li>"
            "<li><b>frida --codeshare KishorBal/multiple-root-detection-bypass -f TARGET_PACKAGE</li>"
            "<li><b>frida --codeshare KishorBal/multiple-root-detection-bypass -f TARGET_PACKAGE</li>"
            "<li><b>frida --codeshare KishorBal/multiple-root-detection-bypass -f TARGET_PACKAGE</li>"
            "<li><b>frida --codeshare enovella/anti-frida-bypass -f TARGET_PACKAGE</li>"
            "<li><b>frida --codeshare KishorBal/multiple-root-detection-bypass -f TARGET_PACKAGE</li>"
            "<li><b>frida --codeshare KishorBal/multiple-root-detection-bypass -f TARGET_PACKAGE</li>"
            "<li><b>frida --codeshare KishorBal/multiple-root-detection-bypass -f TARGET_PACKAGE</li>"
            "<li><b>frida --codeshare enovella/anti-frida-bypass -f TARGET_PACKAGE</li>"
            "<li><b>frida --codeshare KishorBal/multiple-root-detection-bypass -f TARGET_PACKAGE</li>"
          
    
            "</ul>"
        )
        command_dict_text.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-family: Arial, sans-serif;
                color: white;
                line-height: 1.6;
            }
            p, ul {
                margin-bottom: 15px;
            }
            li {
                margin-bottom: 10px;
            }
        """)

        command_dict_layout.addWidget(command_dict_text)
        command_dict_tab.setLayout(command_dict_layout)

        tab_widget.addTab(about_tab, "About")
        tab_widget.addTab(command_dict_tab, "Command Dictionary")

        layout.addWidget(tab_widget)
        page.setLayout(layout)
        self.stacked_widget.addWidget(page)

    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_EnableHighDpiScaling)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)
    splash = SplashScreen()
    sys.exit(app.exec_())
