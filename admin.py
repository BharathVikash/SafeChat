import flet as ft
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from chat_message import *
import hashlib
from admin_signin import SignInForm
from google.cloud.firestore_v1.base_query import FieldFilter
cred = credentials.Certificate(
    "bullyprotect-b925b-firebase-adminsdk-evorn-308e4bbf98.json")
firebase_admin.initialize_app(cred)
print("ADMIN ONLINE!")

db = firestore.client()


def main(page):
    def sha256_hash(input_string):

        sha256 = hashlib.sha256()

        sha256.update(input_string.encode('utf-8'))

        hashed_string = sha256.hexdigest()

        return hashed_string

    def sign_in(user: str, password: str):
        users_ref = db.collection("admin").document(user)
        docs = users_ref.get()
        auth = False

        msg = 'No user with the Username Found!'
        if docs.exists:
            auth = True
            msg = ''
            data = docs.to_dict()
            if data["password"] != password:
                auth = False
                msg = "Log in failed, Incorrect User Name or Password"

        if not auth:
            ShowBanner(msg)

        else:

            page.session.set("user", user)
            page.route = "/panel"
            page.update()

    signin_UI = SignInForm(sign_in)

    def close_banner(e):

        page.banner.open = False
        page.update()

    def ShowBanner(msg):
        page.banner = ft.Banner(
            bgcolor=ft.colors.BLACK45,
            leading=ft.Icon(ft.icons.ERROR, color=ft.colors.RED, size=40),
            content=ft.Text(msg),
            actions=[
                ft.TextButton("Ok", on_click=close_banner),
            ],
        )
        page.banner.open = True
        page.update()
    principal_content = ft.Column(
        [
            ft.Icon(ft.icons.WECHAT, size=200, color=ft.colors.BLUE),
            ft.Text(value="ADMIN PANEL",
                    size=50, color=ft.colors.BLACK),
        ],
        height=400,
        width=600,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    def btn_exit(e):
        page.session.remove("user")
        page.route = "/"
        page.update()

    users_ref = db.collection("users")
    query = users_ref.where(filter=FieldFilter('raised', '==', True))


# Get the documents in the result set
    docs = query.stream()
    users = {}
    for doc in docs:
        user_data = doc.to_dict()
        users[user_data['username']] = user_data

    def unban(user):
        users_ref = db.collection("users").document(user)
        users_ref.update({"is_banned": False})
        users_ref.update({"raised": False})
        docs = users_ref.get().to_dict()

        users_ref.update(
            {"total_warnings": docs["warnings"]+docs["total_warnings"]})
        users_ref.update({"warnings": 0})
        refresh()

    def reject_request(user):
        users_ref = db.collection("users").document(user)
        users_ref.update({"raised": False})
        refresh()

    def refresh(e=''):
        page.clean()
        page.add(
            ft.Row(
                [
                    ft.Text(value="Safe Messenger",
                            color=ft.colors.WHITE),
                    ft.IconButton(icon=ft.icons.REFRESH,                    icon_color="blue400",
                                  icon_size=20,
                                  tooltip="Refresh",
                                  on_click=refresh),
                    ft.ElevatedButton(
                        text="Log Out",
                        bgcolor=ft.colors.RED_800,
                        on_click=btn_exit,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
            )
        )

        users_ref = db.collection("users")
        query = users_ref.where(filter=FieldFilter('raised', '==', True))

        # Get the documents in the result set
        docs = query.stream()
        users = {}
        for doc in docs:
            user_data = doc.to_dict()
            users[user_data['username']] = user_data
        row = []
        for user in users:
            row.append(ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(users[user]['username'])),
                    ft.DataCell(ft.Text(users[user]['mobile'])),
                    ft.DataCell(ft.Text(users[user]['message'])),
                    ft.DataCell(ft.Text(users[user]['prev_bans'])),
                    ft.DataCell(ft.Text(users[user]['warnings'])),
                    ft.DataCell(ft.Text(users[user]['total_warnings'])),
                    ft.DataCell(ft.Row([ft.IconButton(
                        icon=ft.icons.ADD_BOX_ROUNDED,
                        icon_color="blue400",
                        icon_size=20,
                        tooltip="Unban",
                        on_click=lambda e: unban(user),
                    ), ft.IconButton(
                        icon=ft.icons.DELETE_FOREVER_ROUNDED,
                        icon_color="red400",
                        icon_size=20,
                        tooltip="Reject request",
                        on_click=lambda e: reject_request(user),
                        data=user,
                    ),]),),


                ],
            ),)
        page.add(
            ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Username")),
                    ft.DataColumn(ft.Text("Mobile"), numeric=True),
                    ft.DataColumn(ft.Text("Message")),
                    ft.DataColumn(
                        ft.Text("Previous Bans"), numeric=True),
                    ft.DataColumn(
                        ft.Text("Warnings"), numeric=True),
                    ft.DataColumn(
                        ft.Text("Life Time Warnings"), numeric=True),

                    ft.DataColumn(ft.Text("Unban")),

                ],
                rows=[x for x in row

                      ],


            ),
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

        if page.route == '/panel':

            if page.session.contains_key("user"):

                refresh()

            else:
                page.route = "/"
                page.update()
    page.add(
        ft.Row([principal_content, signin_UI],
               alignment=ft.MainAxisAlignment.CENTER)
    )
    page.on_route_change = route_change


ft.app(target=main, view=ft.WEB_BROWSER)
