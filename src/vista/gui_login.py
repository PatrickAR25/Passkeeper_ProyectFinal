from PyQt6 import QtWidgets, QtCore
from src.logica.login_manager import LoginManager
from src.vista.gui_main_passkeeper import PassKeeperApp


class LoginWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.login_manager = LoginManager()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Login - PassKeeper")
        self.resize(400, 350)
        self.setStyleSheet("background-color: #ECF0F1;")  # Fondo claro

        # Diseño principal
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Título
        title_label = QtWidgets.QLabel("Bienvenido a PassKeeper")
        title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #2C3E50;")
        layout.addWidget(title_label)

        # Formulario de inicio de sesión
        form_layout = QtWidgets.QFormLayout()
        form_layout.setSpacing(15)

        self.username_input = self._create_input("Usuario", echo_mode=QtWidgets.QLineEdit.EchoMode.Normal)
        form_layout.addRow(self._create_label("Usuario:"), self.username_input)

        self.password_input = self._create_input("Contraseña", echo_mode=QtWidgets.QLineEdit.EchoMode.Password)
        form_layout.addRow(self._create_label("Contraseña:"), self.password_input)

        layout.addLayout(form_layout)

        # Botones
        button_layout = QtWidgets.QHBoxLayout()
        self.login_button = QtWidgets.QPushButton("Iniciar Sesión", self)
        self.login_button.setStyleSheet(self._button_style("#2ECC71"))
        self.login_button.clicked.connect(self.login)
        button_layout.addWidget(self.login_button)

        self.register_button = QtWidgets.QPushButton("Registrarse", self)
        self.register_button.setStyleSheet(self._button_style("#3498DB"))
        self.register_button.clicked.connect(self.register)
        button_layout.addWidget(self.register_button)

        layout.addLayout(button_layout)

        # Pie de página
        footer_label = QtWidgets.QLabel("Tu seguridad, nuestra prioridad ❤️")
        footer_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        footer_label.setStyleSheet("font-size: 12px; color: #7F8C8D;")
        layout.addWidget(footer_label)

    def _create_input(self, placeholder_text, echo_mode):
        """Crea una entrada con texto negro y placeholder visible."""
        input_field = QtWidgets.QLineEdit(self)
        input_field.setPlaceholderText(placeholder_text)
        input_field.setEchoMode(echo_mode)
        input_field.setStyleSheet(self._input_style())
        return input_field

    def _create_label(self, text):
        """Crea etiquetas con texto negro."""
        label = QtWidgets.QLabel(text)
        label.setStyleSheet("color: #2C3E50; font-size: 14px;")
        return label

    def login(self):
        """Lógica para iniciar sesión."""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            self._show_message("Error", "Por favor, completa todos los campos.")
            return

        if self.login_manager.authenticate_user(username, password):
            self._show_message("Éxito", "Inicio de sesión exitoso.")
            self.open_main_app()
        else:
            self._show_message("Error", "Credenciales incorrectas.")

    def register(self):
        """Lógica para registrarse."""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            self._show_message("Error", "Por favor, completa todos los campos.")
            return

        if self.login_manager.register_user(username, password):
            self._show_message("Éxito", "Usuario registrado correctamente.")
        else:
            self._show_message("Error", "El usuario ya existe.")

    def open_main_app(self):
        """Abre la aplicación principal y cierra la ventana de login."""
        self.main_app = PassKeeperApp()
        self.main_app.show()
        self.close()

    def _show_message(self, title, message):
        """Muestra un QMessageBox con estilos personalizados."""
        msg_box = QtWidgets.QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStyleSheet(self._message_box_style())
        msg_box.exec()

    @staticmethod
    def _message_box_style():
        """Estilo para mensajes de QMessageBox."""
        return """
        QMessageBox {
            background-color: white;
            color: #000000;  /* Texto negro */
            font-size: 14px;
        }
        QMessageBox QLabel {
            color: #000000;  /* Texto negro */
        }
        QMessageBox QPushButton {
            background-color: #3498DB;
            color: white;
            font-size: 12px;
            padding: 5px;
            border-radius: 3px;
        }
        QMessageBox QPushButton:hover {
            background-color: #2980B9;
        }
        """

    @staticmethod
    def _input_style():
        """Estilo para campos de entrada."""
        return """
        QLineEdit {
            background-color: white;
            border: 1px solid #BDC3C7;
            border-radius: 5px;
            padding: 8px;
            font-size: 14px;
            color: #000000;  /* Texto negro */
        }
        QLineEdit:focus {
            border: 1px solid #3498DB;
        }
        QLineEdit::placeholder {
            color: #7F8C8D;  /* Placeholder en gris oscuro */
        }
        """

    @staticmethod
    def _button_style(color):
        """Estilo para botones."""
        return f"""
        QPushButton {{
            background-color: {color};
            color: white;
            font-size: 14px;
            font-weight: bold;
            padding: 10px;
            border-radius: 5px;
        }}
        QPushButton:hover {{
            background-color: #1ABC9C;
        }}
        QPushButton:pressed {{
            background-color: #16A085;
        }}
        """


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec())
