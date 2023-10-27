import datetime
import flet as ft
from signin_form import *
from signup_form import *
from users_db import *
from chat_message import *
import predict
import complaint

users_list = [{"user": "Sakthi", "password": "sakthi",
               "mobile": '044-45985645'}, {"user": "prakash", "password": "prakash", "mobile": '85497826352'}]


def main(page: ft.Page):
    print("main")
    page.title = "Safe Messenger"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def dropdown_changed(e):
        new_message.value = new_message.value + emoji_list.value
        page.update()

    def close_banner(e):

        print("close b")
        page.banner.open = False
        page.update()

    def open_dlg():
        page.dialog = dlg
        dlg.open = True
        page.update()

    def close_dlg(e):
        dlg.open = False
        page.route = "/"
        page.update()

    def sign_in(user: str, password: str):
        db = UsersDB()
        if not db.read_db(user, password):
            print("User no exist ...")
            page.banner.open = True
            page.update()
        else:
            print("Redirecting to chat...")
            page.session.set("user", user)
            page.route = "/chat"
            page.pubsub.send_all(
                Message(
                    user=user,
                    text=f"{user} has joined the chat.",
                    message_type="login_message",
                )
            )
            page.update()

    def sign_up(user: str, password: str, mobile):
        db = UsersDB()
        if db.write_db(user, password, mobile):
            print("Successfully Registered User...")
            open_dlg()

    def on_message(message: Message):
        if message.message_type == "chat_message":
            m = ChatMessage(message)
        else:
            m = ft.Text(message.text, italic=True,
                        color=ft.colors.WHITE, size=12)

        chat.controls.append(m)
        page.update()

    page.pubsub.subscribe(on_message)
    warning_count = {}

    def send_message_click(e):
        message = new_message.value
        prediction = predict.predict_text(message)

        # Track the number of warnings given to the user
        user = page.session.get("user")
        if prediction > 50:

            if user in warning_count:
                warning_count[user] += 1
            else:
                warning_count[user] = 1

                # Show an alert message to the user if the warning count is greater than 0
            if warning_count[user] < 3:
                page.pubsub.send_all(
                    Message(
                        user=page.session.get("user"),
                        text=f"The message doesn't follow the policy of the company.{user} has {3 - warning_count[user]} warnings remaining.",
                        message_type="alert",
                    )
                )

            # If the warning count is equal to 3, generate a complaint document and remove the user from the chat room
            elif warning_count[user] == 3:
                db = UsersDB()
                number = db.getNumber(page.session.get("user"))
                complaint.generate_complaint_document(
                    page.session.get("user"), number, message, datetime.datetime.now())
                page.pubsub.send_all(
                    Message(
                        user=page.session.get("user"),
                        text=f"{user} is banned from the chat room due to incomplaince with company policy.Their future messages will not reflect in the chat room",
                        message_type="alert",
                    )
                )
            else:
                page.pubsub.send_all(
                    Message(
                        user=page.session.get("user"),
                        text="This message is not displayed due to company policy",
                        message_type="alert",
                    )
                )

        else:
            if user in warning_count and warning_count[user] >= 3:
                page.pubsub.send_all(
                    Message(
                        user=page.session.get("user"),
                        text="You were banned from the chat room due to incomplaince with company policy",
                        message_type="alert",
                    )
                )
            else:
                page.pubsub.send_all(
                    Message(
                        user=page.session.get("user"),
                        text=message,
                        message_type="chat_message",
                    )
                )

            # Clear the message input field
            new_message.value = ""

            # Update the page
            page.update()

    def btn_signin(e):
        page.route = "/"
        page.update()

    def btn_signup(e):
        page.route = "/signup"
        page.update()

    def btn_exit(e):
        page.session.remove("user")
        page.route = "/"
        page.update()

    principal_content = ft.Column(
        [
            ft.Icon(ft.icons.WECHAT, size=200, color=ft.colors.BLUE),
            ft.Text(value="Safe Messenger",
                    size=50, color=ft.colors.BLACK),
        ],
        height=400,
        width=600,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
    emoji_list = ft.Dropdown(
        on_change=dropdown_changed,
        options=[
            ft.dropdown.Option("😃"),
            ft.dropdown.Option("😊"),
            ft.dropdown.Option("😂"),
            ft.dropdown.Option("🤔"),
            ft.dropdown.Option("😭"),
            ft.dropdown.Option("😉"),
            ft.dropdown.Option("🤩"),
            ft.dropdown.Option("🥰"),
            ft.dropdown.Option("😎"),
            ft.dropdown.Option("❤️"),
            ft.dropdown.Option("🔥"),
            ft.dropdown.Option("✅"),
            ft.dropdown.Option("✨"),
            ft.dropdown.Option("👍"),
            ft.dropdown.Option("🎉"),
            ft.dropdown.Option("👉"),
            ft.dropdown.Option("⭐"),
            ft.dropdown.Option("☀️"),
            ft.dropdown.Option("👀"),
            ft.dropdown.Option("👇"),
            ft.dropdown.Option("🚀"),
            ft.dropdown.Option("🎂"),
            ft.dropdown.Option("💕"),
            ft.dropdown.Option("🏡"),
            ft.dropdown.Option("🍎"),
            ft.dropdown.Option("🎁"),
            ft.dropdown.Option("💯"),
            ft.dropdown.Option("💤"),
        ],
        width=50,
        value="😃",
        alignment=ft.alignment.center,
        border_color=ft.colors.AMBER,
        color=ft.colors.AMBER,
    )

    signin_UI = SignInForm(sign_in, btn_signup)
    signup_UI = SignUpForm(sign_up, btn_signin)

    chat = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
    )

    new_message = ft.TextField(
        hint_text="Write a message...",
        autofocus=True,
        shift_enter=True,
        min_lines=1,
        max_lines=5,
        filled=True,
        expand=True,
        on_submit=send_message_click,
    )

    page.banner = ft.Banner(
        bgcolor=ft.colors.BLACK45,
        leading=ft.Icon(ft.icons.ERROR, color=ft.colors.RED, size=40),
        content=ft.Text("Log in failed, Incorrect User Name or Password"),
        actions=[
            ft.TextButton("Ok", on_click=close_banner),
        ],
    )

    dlg = ft.AlertDialog(
        modal=True,
        title=ft.Container(
            content=ft.Icon(
                name=ft.icons.CHECK_CIRCLE_OUTLINED, color=ft.colors.GREEN, size=100
            ),
            width=120,
            height=120,
        ),
        content=ft.Text(
            value="Congratulations,\n your account has been successfully created\n Please Sign In",
            text_align=ft.TextAlign.CENTER,
        ),
        actions=[
            ft.ElevatedButton(
                text="Continue", color=ft.colors.WHITE, on_click=close_dlg
            )
        ],
        actions_alignment="center",
        on_dismiss=lambda e: print("Dialog dismissed!"),
    )

    def route_change(route):
        if page.route == "/":
            page.clean()
            page.add(
                ft.Row(
                    [principal_content, signin_UI],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            )

        if page.route == "/signup":
            page.clean()
            page.add(
                ft.Row(
                    [principal_content, signup_UI],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            )

        if page.route == "/chat":
            if page.session.contains_key("user"):
                page.clean()
                page.add(
                    ft.Row(
                        [
                            ft.Text(value="Safe Messenger",
                                    color=ft.colors.WHITE),
                            ft.ElevatedButton(
                                text="Log Out",
                                bgcolor=ft.colors.RED_800,
                                on_click=btn_exit,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    )
                )
                page.add(
                    ft.Container(
                        content=chat,
                        border=ft.border.all(1, ft.colors.OUTLINE),
                        border_radius=5,
                        padding=10,
                        expand=True,
                    )
                )
                page.add(
                    ft.Row(
                        controls=[
                            emoji_list,
                            new_message,
                            ft.IconButton(
                                icon=ft.icons.SEND_ROUNDED,
                                tooltip="Send message",
                                on_click=send_message_click,
                            ),
                        ],
                    )
                )

            else:
                page.route = "/"
                page.update()

    page.on_route_change = route_change
    page.add(
        ft.Row([principal_content, signin_UI],
               alignment=ft.MainAxisAlignment.CENTER)
    )


ft.app(target=main, view=ft.WEB_BROWSER)
