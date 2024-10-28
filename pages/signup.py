import flet as ft
import time
from pages.login import LoginPage
from utils.Database import Database
from utils.style import *
from utils.Validation import Validation
from utils.function import hesh_password


class SignupPage:

    validators = Validation()

    def __init__(self):
        # Defining input fields correctly
        self.email_input = ft.Container(
            content=ft.TextField(
                label="Email",
                bgcolor=secondaryBqColor,
                border=ft.InputBorder.NONE,
                filled=True,
                color=secondaryFontColor,
                on_change=self.clear_error  # Автоматическая очистка ошибки
            ),
            border_radius=15,
        )
        self.login_input = ft.Container(
            content=ft.TextField(
                label="Login",
                bgcolor=secondaryBqColor,
                border=ft.InputBorder.NONE,
                filled=True,
                color=secondaryFontColor,
                on_change=self.clear_error  # Автоматическая очистка ошибки
            ),
            border_radius=15,
        )
        self.password_input = ft.Container(
            content=ft.TextField(
                label="Password",
                password=True,
                can_reveal_password=True,
                bgcolor=secondaryBqColor,
                border=ft.InputBorder.NONE,
                filled=True,
                color=secondaryFontColor,
                on_change=self.clear_error  # Автоматическая очистка ошибки
            ),
            border_radius=15,
        )
        self.confirm_password_input = ft.Container(
            content=ft.TextField(
                label="Confirm Password",
                password=True,
                can_reveal_password=True,
                bgcolor=secondaryBqColor,
                border=ft.InputBorder.NONE,
                filled=True,
                color=secondaryFontColor,
                on_change=self.clear_error  # Автоматическая очистка ошибки
            ),
            border_radius=15,
        )
        self.error_field = ft.Text('', color='red')

    def clear_error(self, e):
        """ Функция для очистки сообщений об ошибках при изменении любого поля ввода """
        self.error_field.value = ""
        self.error_field.update()

    def view(self, page: ft.Page):
        page.title = "Page Registration"
        page.window.width = defaultWidthWindows
        page.window.height = defaultHeightWindows
        page.window.min_width = 800
        page.window.min_height = 400

        login_link = ft.Container(
            content=ft.Text("Login", color=defaultFontColor),
            on_click=lambda e: page.go('/'),  # Removed trailing comma here
        )



        # Load custom fonts
        page.fonts = {"muller-extrabold": "fonts/muller-extrabold.ttf"}

        def signup(e):
            email_value = self.email_input.content.value
            login_value = self.login_input.content.value
            password_value = self.password_input.content.value
            confirm_password_value = self.confirm_password_input.content.value

            # Проверка на заполнение всех полей
            if email_value and login_value and password_value and confirm_password_value:
                db = Database()

                # Проверка валидности email
                if not self.validators.is_valid_email(email_value):
                    self.email_input.content.bgcolor = inputBqErrorColor
                    self.error_field.value = 'Invalid email format'
                    self.error_field.size = 12
                    self.email_input.update()
                    self.error_field.update()
                elif db.check_email(email_value):  # Проверка на занятость email
                    self.email_input.content.bgcolor = inputBqErrorColor
                    self.error_field.value = "This email is already taken"
                    self.error_field.size = 12
                    self.email_input.update()
                    self.error_field.update()
                elif db.check_login(login_value):  # Проверка на занятость логина
                    self.login_input.content.bgcolor = inputBqErrorColor
                    self.error_field.value = "This login is already taken"
                    self.error_field.size = 12
                    self.login_input.update()
                    self.error_field.update()
                elif not self.validators.is_valid_password(password_value):  # Проверка пароля
                    self.password_input.content.bgcolor = inputBqErrorColor
                    self.error_field.value = "Invalid password"
                    self.error_field.size = 12
                    self.password_input.update()
                    self.error_field.update()
                elif password_value != confirm_password_value:  # Сравнение паролей
                    self.error_field.value = "Passwords do not match"
                    self.error_field.size = 12
                    self.error_field.update()
                else:
                    # Регистрация пользователя в базе данных
                    db.register_user(email_value, login_value,hesh_password(password_value))
                    self.error_field.value = "Registration successful!"
                    self.error_field.size = 12
                    self.error_field.color = ft.colors.GREEN
                    self.error_field.update()
                    time.sleep(2)  # Пауза для отображения успешного сообщения
                    page.go("/")  # Перенаправление на главную страницу
            else:
                self.error_field.value = "All fields are required!"
                self.error_field.size = 12
                self.error_field.update()

        return ft.View(
            "/",
            controls=[
                ft.Row(
                    expand=True,
                    controls=[
                        # Left panel
                        ft.Container(
                            expand=2,
                            padding=ft.padding.all(40),
                            content=ft.Column(
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Text(
                                        "Welcome to Registration",
                                        color=defaultFontColor,
                                        size=25,
                                        font_family="prisma-pro-shadow",
                                    ),
                                    self.error_field,
                                    self.email_input,
                                    self.login_input,
                                    self.password_input,
                                    self.confirm_password_input,
                                    ft.Container(
                                        content=ft.Text("Register", color=defaultFontColor),
                                        alignment=ft.alignment.center,
                                        height=40,
                                        bgcolor=hoverBqColor,
                                        on_click=lambda e: signup(e),
                                    ),
                                    login_link
                                ]
                            )
                        ),
                        # Right panel with background image
                        ft.Container(
                            expand=3,
                            image_src="images/bg_login.jpg",
                            image_fit=ft.ImageFit.COVER,
                            content=ft.Column(
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Icon(
                                        name=ft.icons.VERIFIED_USER_ROUNDED,
                                        color=hoverBqColor,
                                        size=140,
                                    ),
                                    ft.Text(
                                        "Form Registration",
                                        color=hoverBqColor,
                                        size=15,
                                        weight=ft.FontWeight.BOLD,
                                        font_family="muller-extrabold",
                                    ),
                                ]
                            ),
                        ),
                    ]
                )
            ],
            bgcolor=defaultBqColor,
            padding=0
        )
