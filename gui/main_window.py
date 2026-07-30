from PySide6.QtWidgets import (
    QMainWindow,
    QStackedWidget,
    QGraphicsOpacityEffect,
)
from PySide6.QtCore import (
    QEasingCurve,
    QParallelAnimationGroup,
    QPropertyAnimation,
    QPoint,
)
from gui.login_window import LoginPage
from gui.dashboard_window import DashboardPage
from gui.theme import *
from gui.register_window import CreateAccountPage


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        

        self.setStyleSheet(f"""
            QWidget {{
                background: {BACKGROUND};
            }}
        """)

        self.setWindowTitle("SecureDB")
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.create_account_page = CreateAccountPage()
        self.stack.addWidget(self.create_account_page)

        self.login_page = LoginPage()

        self.login_effect = QGraphicsOpacityEffect()
        self.login_page.setGraphicsEffect(self.login_effect)
        self.login_effect.setOpacity(1.0)

        self.login_page.login_successful.connect(self.show_dashboard)

        self.login_page.show_create_account.connect(
            lambda: self.transition(self.login_page, self.create_account_page, -1)
        )

        self.create_account_page.back_requested.connect(
            lambda: self.transition(self.create_account_page, self.login_page, 1)
        )
        self.create_account_page.account_created.connect(self.on_account_created)

        self.stack.addWidget(self.login_page)
        self.stack.setCurrentWidget(self.login_page)

        self.dashboard_page = None

    def show_dashboard(self, user, key):

        self.dashboard_page = DashboardPage(user, key)

        self.dashboard_effect = QGraphicsOpacityEffect()
        self.dashboard_page.setGraphicsEffect(self.dashboard_effect)
        self.dashboard_effect.setOpacity(0.0)

        self.stack.addWidget(self.dashboard_page)

        self.fade_out = QPropertyAnimation(self.login_effect, b"opacity")
        self.fade_out.setDuration(250)
        self.fade_out.setStartValue(1.0)
        self.fade_out.setEndValue(0.0)

        self.fade_out.finished.connect(self.finish_dashboard_transition)

        self.fade_out.start()

    def finish_dashboard_transition(self):

        self.stack.setCurrentWidget(self.dashboard_page)

        self.dashboard_page.logout_requested.connect(self.show_login)

        self.fade_in = QPropertyAnimation(self.dashboard_effect, b"opacity")
        self.fade_in.setDuration(250)
        self.fade_in.setStartValue(0.0)
        self.fade_in.setEndValue(1.0)

        self.fade_in.start()

    def show_login(self):

        self.login_page.reset()

        self.fade_out = QPropertyAnimation(self.dashboard_effect, b"opacity")
        self.fade_out.setDuration(250)
        self.fade_out.setStartValue(1.0)
        self.fade_out.setEndValue(0.0)

        self.fade_out.finished.connect(self.finish_login_transition)

        self.fade_out.start()

    def finish_login_transition(self):

        self.stack.setCurrentWidget(self.login_page)

        self.fade_in = QPropertyAnimation(self.login_effect, b"opacity")
        self.fade_in.setDuration(250)
        self.fade_in.setStartValue(0.0)
        self.fade_in.setEndValue(1.0)

        self.fade_in.start()

        self.stack.removeWidget(self.dashboard_page)
        self.dashboard_page.deleteLater()
        self.dashboard_page = None

    def show_create_account(self):
        self.create_account_page.reset()
        self.stack.setCurrentWidget(self.create_account_page)

    def show_login_from_register(self):
        self.create_account_page.reset()
        self.stack.setCurrentWidget(self.login_page)

    def transition(self, from_page, to_page, direction=1):
        """
        direction = 1   -> next page comes from the right
        direction = -1  -> next page comes from the left
        """

        offset = QPoint(15 * direction, 0)

        # Create opacity effects if needed
        if from_page.graphicsEffect() is None:
            from_page.setGraphicsEffect(QGraphicsOpacityEffect(from_page))

        if to_page.graphicsEffect() is None:
            to_page.setGraphicsEffect(QGraphicsOpacityEffect(to_page))

        from_effect = from_page.graphicsEffect()
        to_effect = to_page.graphicsEffect()

        # Initial states
        from_effect.setOpacity(1.0)
        to_effect.setOpacity(0.0)

        original_pos = from_page.pos()

        to_page.move(original_pos + offset)
        self.stack.setCurrentWidget(to_page)

        # ---------------- Fade Out ----------------

        fade_out = QPropertyAnimation(from_effect, b"opacity")
        fade_out.setDuration(220)
        fade_out.setStartValue(1.0)
        fade_out.setEndValue(0.0)
        fade_out.setEasingCurve(QEasingCurve.OutCubic)

        # ---------------- Fade In -----------------

        fade_in = QPropertyAnimation(to_effect, b"opacity")
        fade_in.setDuration(220)
        fade_in.setStartValue(0.0)
        fade_in.setEndValue(1.0)
        fade_in.setEasingCurve(QEasingCurve.OutCubic)

        # ---------------- Slide Out ----------------

        slide_out = QPropertyAnimation(from_page, b"pos")
        slide_out.setDuration(220)
        slide_out.setStartValue(original_pos)
        slide_out.setEndValue(original_pos - offset)
        slide_out.setEasingCurve(QEasingCurve.OutCubic)

        # ---------------- Slide In -----------------

        slide_in = QPropertyAnimation(to_page, b"pos")
        slide_in.setDuration(220)
        slide_in.setStartValue(original_pos + offset)
        slide_in.setEndValue(original_pos)
        slide_in.setEasingCurve(QEasingCurve.OutCubic)

        # ---------------- Run ----------------

        self.transition_group = QParallelAnimationGroup(self)

        self.transition_group.addAnimation(fade_out)
        self.transition_group.addAnimation(fade_in)
        self.transition_group.addAnimation(slide_out)
        self.transition_group.addAnimation(slide_in)

        def cleanup():
            from_page.move(original_pos)
            from_effect.setOpacity(1.0)
            to_effect.setOpacity(1.0)

        self.transition_group.finished.connect(cleanup)
        self.transition_group.start()

    def on_account_created(self):
        self.login_page.reset()
        self.login_page.status.setStyleSheet(f"color: {ACCENT};")
        self.login_page.status.setText("Account created successfully!")

        self.transition(
            self.create_account_page,
            self.login_page,
            1
        )