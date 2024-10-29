import os
import flet as ft
from utils.Database import Database
from utils.Validation import Validation
from utils.style import *


class PostPage:



    token_bot = os.getenv('TOKEN_BOT')
    channel_link = os.getenv('CHANNEL_LINK')
    validation = Validation()
    db = Database()

    def view(self, page: ft.Page):
        noteInputBqColor = ft.colors.GREY_200  # Light gray background
        noteInputFontColor = ft.colors.BLACK  # Black font color
        noteInputBorderColor = ft.colors.GREY_400  # Gray border color

        searchFieldBqColor = ft.colors.WHITE  # White background for the search field
        searchFieldFontColor = ft.colors.BLACK  # Black font color
        searchFieldBorderColor = ft.colors.GREY_400  # Gray border color


        page.title = "Add post"
        page.window.width = defaultWidthWindows
        page.window.height = defaultHeightWindows
        page.window.min_width = 900
        page.window.min_height = 400

        # Define fonts
        page.fonts = {
            "muller-extrabold": "fonts/muller-extrabold.ttf",
            "prisma-pro-shadow": "fonts/prisma-pro-shadow.ttf",
        }

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
                    ft.Text('Menu', color=menuColorFont, size=12),
                    ft.TextButton('Header', icon='space_dashboard_rounded', style=style_menu,
                                  on_click=lambda e: page.go('/dashboard')),
                    ft.TextButton('Send', icon='post_add', style=style_menu,
                                  on_click=lambda e: page.go('/posting')),
                    ft.TextButton('Test Button', icon='verified_user', style=style_menu),
                ]
            )
        )

        # Header
        header = ft.Container(content=ft.Row(controls=[
            ft.Text('Control Panel', color=defaultFontColor, size=20, font_family='muller-extrabold'),
            ft.Row(controls=[
                ft.CircleAvatar(foreground_image_src='images/avatar.png', content=ft.Text('Avatar')),
                ft.IconButton(icon=ft.icons.NOTIFICATIONS_ROUNDED, icon_size=20, hover_color=hoverBqColor,
                              icon_color=defaultFontColor)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN))

        # Add input fields for new note
        self.note_input = ft.TextField(
            hint_text="Write a new note...",
            multiline=True,
            min_lines=2,
            max_lines=4,
            expand=True,


        )

        self.priority_input = ft.Dropdown(
            options=[
                ft.dropdown.Option("1 - Low"),
                ft.dropdown.Option("2 - Medium"),
                ft.dropdown.Option("3 - High")
            ],
            hint_text="Select priority",
        )

        # Add a button to save the note
        save_button = ft.ElevatedButton(
            text="Save Note",
            on_click=self.save_note_handler
        )

        search_field = ft.TextField(
            hint_text="Search notes...",
            on_change=self.update_notes_view
        )  # Remove the comma here

        sort_dropdown = ft.Dropdown(
            options=[ft.dropdown.Option("Priority"), ft.dropdown.Option("Date")],
            on_change=self.update_notes_view
        )

        self.notes_list = ft.Column()

        notes_section = ft.Container(
            content=ft.Column([
                ft.Row(
                    controls=[search_field, sort_dropdown],  # Use list format here
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                self.notes_list
            ]),
            padding=ft.padding.all(10),
            expand=True
        )

        # New note form section
        new_note_section = ft.Container(
            content=ft.Column([
                ft.Row([self.note_input, self.priority_input], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                save_button
            ]),
            padding=ft.padding.all(10),
            expand=True
        )
        # Layout structure
        view = ft.View(
            "/dashboard",
            controls=[
                ft.Row(
                    expand=True,
                    controls=[
                        ft.Container(
                            expand=1,
                            content=ft.Column(
                                controls=[logotype, sidebar_menu]
                            ),
                            bgcolor=secondaryBqColor,
                        ),
                        ft.Container(
                            expand=4,
                            padding=ft.padding.symmetric(15, 10),
                            content=ft.Column([header, new_note_section, notes_section]),
                            bgcolor=secondaryBqColor
                        ),

                    ]
                )
            ], bgcolor=defaultBqColor, padding=0
        )

        # Load notes once the view is attached to the page
        page.on_load = lambda e: self.load_notes()  # Load notes only after the page has fully loaded
        return view

    def save_note_handler(self, e):
        """Handler for saving a new note."""
        note_text = self.note_input.value
        priority_text = self.priority_input.value

        if note_text and priority_text:
            priority = int(priority_text.split(" - ")[0])  # Extract the priority number
            user_id = 1  # Replace with the actual user ID logic in a real app

            # Save the note to the database
            self.db.create_note(user_id, note_text, priority)

            # Clear input fields
            self.note_input.value = ""
            self.priority_input.value = None

            # Refresh the notes list
            self.load_notes()

            # Update the page to reflect changes
            self.note_input.update()
            self.priority_input.update()
            self.notes_list.update()

    def load_notes(self, search_query="", sort_by="priority"):
        """Load and display notes based on search and sort criteria."""
        self.notes_list.controls.clear()
        notes = self.db.get_user_notes_sorted(search_query, sort_by)

        for note in notes:
            note_control = ft.Row(
                controls=[
                    ft.Text(note[2]),  # Display the note text
                    ft.Text(f"Priority: {note[3]}"),
                    ft.IconButton(icon=ft.icons.DELETE,
                                  on_click=lambda e, note_id=note[0]: self.delete_note_handler(note_id))
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
            self.notes_list.controls.append(note_control)

        self.notes_list.update()

    def update_notes_view(self, e):
        """Update notes display based on search query and sort order."""
        search_query = e.control.parent.controls[0].value  # Value from search field
        sort_by = e.control.parent.controls[1].value  # Value from sort dropdown
        self.load_notes(search_query, sort_by)

    def delete_note_handler(self, note_id):
        """Handle deleting a note."""
        self.db.delete_note(note_id)
        self.load_notes()
