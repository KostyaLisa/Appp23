import os

import flet as ft
from dotenv import set_key, load_dotenv

from utils.style import *
from pathlib import Path


class DashboardPage:
    env_file_path = Path('.') / 'env.'
    load_dotenv(dotenv_path= env_file_path)
    AUTH_USER = False
    # check_token = ''
    # check_channel = ''

    token_bot = os.getenv('TOKEN_BOT')
    channel_link = os.getenv('CHANNEL_LINK')

    def view(self, page: ft.Page):
        self.AUTH_USER = page.session.get('auth_user')
        page.title = "Dashboard"
        page.window.width = defaultWidthWindows
        page.window.height = defaultHeightWindows
        page.window.min_width = 900
        page.window.min_height = 400
        print(self.token_bot)

        # Define fonts
        page.fonts = {
            "muller-extrabold": "fonts/muller-extrabold.ttf",
            "prisma-pro-shadow": "fonts/prisma-pro-shadow.ttf",
        }

        # Function starting
        def save_settings(e):
            token_bot = token_input.content.value
            channel_link = channel_input.content.value
            set_key(dotenv_path=self.env_file_path, key_to_set='TOKEN_BOT', value_to_set=token_bot)
            set_key(dotenv_path=self.env_file_path, key_to_set='CHANNEL_LINK', value_to_set=channel_link)
            token_input.disabled = True
            channel_input.disabled = True
            page.session.set('TOKEN_BOT', token_bot)
            page.session.set('CHANNEL_LINK', channel_link)
            self.check_token = page.session.get('TOKEN_BOT')
            self.check_channel = page.session.get('CHANNEL_LINK')
            save_btn.text = "Saving"
            save_btn.disabled = True
            save_btn.update()
            token_input.update()
            channel_input.update()
            page.update()

        def input_form(label,value):
            return ft.TextField(label=f'{label}', value=value,
                                bgcolor=secondaryBqColor,
                                border=ft.InputBorder.NONE,
                                filled=True,
                                color=secondaryFontColor)

        def input_disable(value):
            return ft.TextField(value=value,
                                bgcolor=secondaryBqColor,
                                border=ft.InputBorder.NONE,
                                filled=True,
                                disabled=True,
                                color=secondaryFontColor)

        # Style menu

        style_menu = ft.ButtonStyle(color={ft.ControlState.HOVERED: ft.colors.WHITE,
                                           ft.ControlState.DEFAULT: menuColorFont},
                                    icon_size=14,
                                    overlay_color=hoverBqColor,
                                    shadow_color=hoverBqColor)

        # Sidebar

        logotype = ft.Container(
            padding=ft.padding.symmetric(17, 13),
            content=ft.Row(
                controls=[
                    ft.Image(src='images/logo.png', width=45, height=32, fit=ft.ImageFit.FILL),
                    ft.Text('Tlogo', expand=True, color=defaultFontColor, font_family='muller-extrabold', size=16)
                ], alignment=ft.MainAxisAlignment.START,
                spacing=5,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

        sidebar_menu = ft.Container(
            padding=ft.padding.symmetric(0, 13),
            content=ft.Column(
                controls=[
                    ft.Text('Menu', color=menuColorFont, size=12, font_family='muller-extrabold'),
                    ft.TextButton('Header', icon='space_dashboard_rounded', style=style_menu,
                                  on_click=lambda e: page.go('/dashboard')),
                    ft.TextButton('Send', icon='post_add', style=style_menu,
                                  on_click=lambda e: page.go('/posting')),
                    ft.TextButton('Test Button', icon='verified_user', style=style_menu),

                ],

            )
        )

        # Text button
        note_text = ft.TextField(label="Новая заметка", width=250)
        note_priority = ft.TextField(label="Приоритет", width=250)
        add_note_btn = ft.ElevatedButton(text="Добавить заметку")
        search_btn = ft.ElevatedButton()


        if not self.token_bot and not page.session.get('TOKEN_BOT'):
            token_input = ft.Container(
                content=input_form('Enter Token', page.session.get('TOKEN_BOT')),
                border_radius=15)
        elif page.session.get('TOKEN_BOT'):
            token_input = ft.Container(
                content=input_disable(page.session.get('TOKEN_BOT')),
                border_radius=15)
        else:
            token_input = ft.Container(
                content=input_disable(self.token_bot),
                border_radius=15)
        if not self.channel_link and not page.session.get('CHANNEL_LINK'):
            channel_input = ft.Container(
                content=input_form('Enter link to channel',page.session.get('CHANNEL_LINK')),
                border_radius=15)
        elif page.session.get('CHANNEL_LINK'):
            channel_input = ft.Container(
                content=input_disable(page.session.get('CHANNEL_LINK')),
                border_radius=15)
        else:
            channel_input = ft.Container(
                content=input_disable(self.channel_link),
                border_radius=15)

        if not self.token_bot and not self.channel_link:
            save_btn = ft.ElevatedButton('Save Data', bgcolor=hoverBqColor, color=defaultFontColor, icon='settings',
                                         on_click=lambda e: save_settings(e))
        else:
            save_btn = ft.ElevatedButton('Saving', bgcolor=hoverBqColor, color=defaultFontColor, icon='save',
                                         disabled=True)

        # Header

        header = ft.Container(content=ft.Row(controls=[
            ft.Text('Control Panel', color=defaultFontColor, size=20, font_family='muller-extrabold'),
            ft.Row(controls=[
                # ft.TextButton('Logout', icon='exit_to_app', style=style_menu),
                #
                # ft.Text('Welcome, John Doe', color=defaultFontColor, size=12, font_family='muller-extrabold'),
                #
                # ft.TextButton('Help', icon='help', style=style_menu),
                #
                # ft.TextButton('Settings', icon='settings', style=style_menu),
                #
                # ft.TextButton('Profile', icon='account_circle', style=style_menu),
                #
                # ft.TextButton('Notifications', icon='notifications', style=style_menu),
                #
                # ft.TextButton('Messages', icon='message', style=style_menu),
                #
                # ft.TextButton('Help', icon='help', style=style_menu),
                ft.CircleAvatar(foreground_image_src='images/avatar.png',
                                content=ft.Text('Avatar')),
                ft.IconButton(
                    icon=ft.icons.NOTIFICATIONS_ROUNDED,
                    icon_size=20,
                    hover_color=hoverBqColor,
                    icon_color=defaultFontColor,

                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ))

        return ft.View(
            "/dashboard",
            controls=[
                ft.Row(
                    expand=True,  # changer horizontal(expand delite) o vertical menu
                    controls=[
                        ft.Container(
                            expand=1,
                            content=ft.Column(
                                controls=[
                                    logotype,
                                    sidebar_menu
                                ]
                            ),
                            bgcolor=secondaryBqColor,

                        ),
                        ft.Container(
                            expand=4,
                            padding=ft.padding.symmetric(15, 10),
                            content=ft.Column([header, token_input, channel_input, save_btn]

                                              )
                        )
                    ]
                )

            ], bgcolor=defaultBqColor,
            padding=0
        )
