import flet as ft

from utils.style import *
from utils.Database import Database
from utils.function import hesh_password


class LoginPage:
    def __init__(self):
        self.email_input = ft.Container(
            content=ft.TextField(
                label="Email",
                bgcolor=secondaryBqColor,
                border=ft.InputBorder.NONE,
                filled=True,
                color=secondaryFontColor,
            ),
            border_radius=15,
        )
        self.password_input = ft.Container(
            content=ft.TextField(
                label="Enter Password",
                password=True,
                can_reveal_password=True,
                bgcolor=secondaryBqColor,
                border=ft.InputBorder.NONE,
                filled=True,
                color=secondaryFontColor,
            ),
            border_radius=15,  # Убрали лишнюю запятую
        )
        self.message_error = ft.SnackBar(
            content=ft.Text("Error", color=inputBqErrorColor),
        )

    def view(self, page: ft.Page):
        # Page setup
        page.title = "Page Authorization"
        page.window.width = defaultWidthWindows
        page.window.height = defaultHeightWindows
        page.window.min_width = 800
        page.window.min_height = 400

        # Define fonts
        page.fonts = {
            "muller-extrabold": "fonts/muller-extrabold.ttf",
            "prisma-pro-shadow": "fonts/prisma-pro-shadow.ttf",
        }

        dashboard_link = ft.Container(
            content=ft.Text("dashboard", color=defaultFontColor),
            on_click=lambda e: page.go('/dashboard'),  # Removed trailing comma here
        )

        signup_link = ft.Container(
            content=ft.Text("Create Account", color=defaultFontColor),
            on_click=lambda e: page.go('/signup'),  # Убрали лишнюю запятую
        )

        def authorization(e):
            db = Database()  # Создание экземпляра Database
            email = self.email_input.content.value
            password = hesh_password(self.password_input.content.value)

            # Проверка пользователя в базе данных
            if db.login_user(email, password):
                page.session.set("auth_user", True)
                page.go('/dashboard')
            else:
                self.message_error.open = True  # Открываем Snackbar правильно
                page.snack_bar = self.message_error  # Указываем Snackbar на странице
                page.update()  # Обновляем страницу для отображения Snackbar

        # Layout
        return ft.View(
            '/',
            controls=[
                ft.Row(
                    expand=True,
                    controls=[
                        # Left Panel
                        ft.Container(
                            expand=2,
                            padding=ft.padding.all(40),
                            content=ft.Column(
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Text(
                                        "Welcome",
                                        color=defaultFontColor,
                                        size=25,
                                        font_family="prisma-pro-shadow",
                                    ),

                                    self.message_error,  # Error message bar
                                    self.email_input,
                                    self.password_input,
                                    ft.Container(
                                        content=ft.Text("Authorization", color=defaultFontColor),
                                        alignment=ft.alignment.center,
                                        height=40,
                                        bgcolor=hoverBqColor,
                                        on_click=lambda e: authorization(e),  # Убрали лишнюю запятую
                                    ),

                                    signup_link,  # Sign-up link to the sign-up page
                                    dashboard_link, # Dashboard link to the dashboard
                                ],
                            ),
                        ),
                        # Right Panel
                        ft.Container(
                            expand=3,
                            image_src="images/bg_login.jpg",
                            image_fit=ft.ImageFit.COVER,
                            content=ft.Column(
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Icon(
                                        name=ft.icons.SCREEN_LOCK_PORTRAIT_ROUNDED,
                                        color=hoverBqColor,
                                        size=140,
                                    ),
                                    ft.Text(
                                        "Authorization",
                                        color=hoverBqColor,
                                        size=15,
                                        weight=ft.FontWeight.BOLD,
                                        font_family="muller-extrabold",
                                    ),
                                ],
                            ),
                        ),
                    ],
                )
            ],
            bgcolor=defaultBqColor,
            padding=0,
        )
