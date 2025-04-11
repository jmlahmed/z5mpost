import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit,
                             QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QStackedLayout)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from database import get_db, User
from sqlalchemy.orm import Session

class WelcomePage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Welcome")
        layout = QVBoxLayout()
        logo_label = QLabel("شعار التطبيق هنا")  # استبدل بنص أو تحميل صورة
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo_label)
        login_button = QPushButton("تسجيل الدخول")
        login_button.clicked.connect(self.parent().go_to_login)
        create_account_button = QPushButton("إنشاء حساب")
        create_account_button.clicked.connect(self.parent().go_to_create_account)
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(login_button)
        buttons_layout.addWidget(create_account_button)
        layout.addLayout(buttons_layout)
        self.setLayout(layout)

class LoginPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("تسجيل الدخول")
        layout = QVBoxLayout()
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("اسم المستخدم")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("كلمة المرور")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        login_button = QPushButton("تسجيل الدخول")
        login_button.clicked.connect(self.login)
        back_button = QPushButton("رجوع")
        back_button.clicked.connect(self.parent().go_to_welcome)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(login_button)
        layout.addWidget(back_button)
        self.setLayout(layout)
        self.db: Session = next(get_db())

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        user = self.db.query(User).filter(User.username == username, User.password == password).first() # يجب استخدام تشفير كلمات المرور في التطبيق الحقيقي
        if user:
            QMessageBox.information(self, "نجاح", f"تم تسجيل الدخول بنجاح: {user.username}")
            self.parent().go_to_profile(user) # الانتقال إلى صفحة الملف الشخصي
        else:
            QMessageBox.warning(self, "خطأ", "اسم المستخدم أو كلمة المرور غير صحيحة.")

class CreateAccountPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("إنشاء حساب")
        layout = QVBoxLayout()
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("اسم المستخدم")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("كلمة المرور")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("تأكيد كلمة المرور")
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        create_button = QPushButton("إنشاء حساب")
        create_button.clicked.connect(self.create_account)
        back_button = QPushButton("رجوع")
        back_button.clicked.connect(self.parent().go_to_welcome)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.confirm_password_input)
        layout.addWidget(create_button)
        layout.addWidget(back_button)
        self.setLayout(layout)
        self.db: Session = next(get_db())

    def create_account(self):
        username = self.username_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()
        if password != confirm_password:
            QMessageBox.warning(self, "خطأ", "كلمة المرور وتأكيد كلمة المرور غير متطابقتين.")
            return
        existing_user = self.db.query(User).filter(User.username == username).first()
        if existing_user:
            QMessageBox.warning(self, "خطأ", "اسم المستخدم موجود بالفعل.")
            return
        new_user = User(username=username, password=password) # يجب استخدام تشفير كلمات المرور
        self.db.add(new_user)
        self.db.commit()
        QMessageBox.information(self, "نجاح", "تم إنشاء الحساب بنجاح.")
        self.parent().go_to_login()

class ProfilePage(QWidget):
    def __init__(self, parent, user):
        super().__init__(parent)
        self.setWindowTitle("الملف الشخصي")
        self.user = user
        layout = QVBoxLayout()
        username_label = QLabel(f"اسم المستخدم: {self.user.username}")
        layout.addWidget(username_label)
        # إضافة عرض الصورة الشخصية وزر التعديل هنا
        back_button = QPushButton("رجوع")
        back_button.clicked.connect(self.parent().go_to_main_app) # سيتم تعديل هذا لاحقًا
        layout.addWidget(back_button)
        self.setLayout(layout)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("تطبيق المنشورات")
        self.setGeometry(100, 100, 800, 600)
        self.stack_layout = QStackedLayout()
        self.welcome_page = WelcomePage(self)
        self.login_page = LoginPage(self)
        self.create_account_page = CreateAccountPage(self)
        self.profile_page = None # سيتم إنشاؤه عند تسجيل الدخول

        self.stack_layout.addWidget(self.welcome_page)
        self.stack_layout.addWidget(self.login_page)
        self.stack_layout.addWidget(self.create_account_page)

        main_layout = QVBoxLayout()
        main_layout.addLayout(self.stack_layout)
        self.setLayout(main_layout)

        self.current_user = None
        self.show()

    def go_to_welcome(self):
        self.stack_layout.setCurrentIndex(0)

    def go_to_login(self):
        self.stack_layout.setCurrentIndex(1)

    def go_to_create_account(self):
        self.stack_layout.setCurrentIndex(2)

    def go_to_profile(self, user):
        self.current_user = user
        self.profile_page = ProfilePage(self, user)
        self.stack_layout.addWidget(self.profile_page)
        self.stack_layout.setCurrentWidget(self.profile_page)

    def go_to_main_app(self):
        # هنا سيتم الانتقال إلى صفحة المنشورات الرئيسية
        QMessageBox.information(self, "معلومة", "سيتم الانتقال إلى صفحة المنشورات.")
        self.stack_layout.setCurrentIndex(0) # مؤقتًا للرجوع إلى الصفحة الرئيسية

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec())