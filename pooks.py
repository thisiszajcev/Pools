import flet as ft
import requests
import json

def main(page: ft.Page):
    page.title = "API Fetcher"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.padding = 20
    page.theme_mode = ft.ThemeMode.LIGHT  # Устанавливаем темную тему по умолчанию

    # Поле для ввода "Пул ID"
    pool_id_input = ft.TextField(label="Пул ID", width=200)

    # Большое текстовое поле для отображения данных
    output_text = ft.TextField(label="Результат", read_only=True, multiline=True, width=500, height=400)

    worker_count_text = ft.Text("Воркеров: 0")
    ip_count_text = ft.Text("IP: 0")

    # Поля для ввода дополнительных данных
    worker_input = ft.TextField(label="Worker", value="Worker", width=200)
    stratum1_input = ft.TextField(label="Stratum 1", value="stratum+tcp://btc.viabtc.io:3333", width=200)
    stratum2_input = ft.TextField(label="Stratum 2", value="stratum+tcp://btc.viabtc.io:25", width=200)
    stratum3_input = ft.TextField(label="Stratum 3", value="stratum+tcp://btc.viabtc.io:443", width=200)
    password_input = ft.TextField(label="Password", value="123", width=200)

    # Функция для обработки нажатия на кнопку
    def fetch_data(e):
        pool_id = pool_id_input.value
        if pool_id:
            url = "https://api.umnus.ru/test4.php"
            payload = {"pool_profile_id": pool_id}
            try:
                response = requests.post(url, json=payload)
                response.raise_for_status()
                data = response.json()
                output_text.value = json.dumps(data, indent=4, ensure_ascii=False)

                worker_count = sum(1 for item in data if "worker_clients_devices" in item)
                ip_count = sum(1 for item in data if "ip_addr_clients_devices" in item and item["ip_addr_clients_devices"].strip() not in ["", "nodata"])

                worker_count_text.value = f"Воркеров: {worker_count}"
                ip_count_text.value = f"IP: {ip_count}"

            except requests.exceptions.RequestException as err:
                output_text.value = f"Ошибка запроса: {err}"
            except json.JSONDecodeError:
                output_text.value = "Ошибка обработки ответа от сервера"
        else:
            output_text.value = "Пожалуйста, введите Пул ID"
        page.update()

    # Функция для обработки нажатия на кнопку "Прописать"
    def apply_action(e):
        if not device_options.value:
            page.snack_bar = ft.SnackBar(ft.Text("Сначала выберите тип устройства"), open=True)
            page.update()
            return

        def on_dialog_result(e):
            if e.control.data == "yes":
                print("Применение данных устройств")  # Здесь будет ваш код
            page.dialog.open = False
            page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Подтверждение"),
            content=ft.Text("Вы точно хотите прописать данные устройства?"),
            actions=[
                ft.TextButton("Да", data="yes", on_click=on_dialog_result),
                ft.TextButton("Нет", data="no", on_click=on_dialog_result),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    # Кнопка ">"
    fetch_button = ft.ElevatedButton(">", on_click=fetch_data)

    # Кнопка "Прописать"
    apply_button = ft.ElevatedButton("Прописать", on_click=apply_action)

    # Переключатель для выбора темы
    def switch_theme(e):
        page.theme_mode = ft.ThemeMode.DARK if theme_switch.value else ft.ThemeMode.LIGHT
        page.update()

    theme_switch = ft.Switch(label="Тема", on_change=switch_theme, value=True)  # Переключатель в положении темной темы

    # Переключатели для выбора типа устройства
    device_options = ft.RadioGroup(
        content=ft.Column(
            [
                ft.Radio(value="Antminer", label="Antminer"),
                ft.Radio(value="Ant Vnish", label="Ant Vnish"),
                ft.Radio(value="Whatsminer", label="Whatsminer")
            ]
        )
    )

    # Переключатели для выбора типа устройства
    device_type_options = ft.RadioGroup(
        content=ft.Column(
            [
                ft.Radio(value="only_antminer", label="Только AntMiner"),
                ft.Radio(value="only_whatsminer", label="Только Whatsminer"),
                ft.Radio(value="all", label="Все")
            ]
        )
    )

    # Добавление элементов на страницу
    page.add(
        ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Container(worker_input, margin=ft.margin.only(top=32)),
                                ft.Container(stratum1_input, margin=ft.margin.only(top=10)),
                                ft.Container(stratum2_input, margin=ft.margin.only(top=10)),
                                ft.Container(stratum3_input, margin=ft.margin.only(top=10)),
                                ft.Container(password_input, margin=ft.margin.only(top=10)),
                                ft.Text("Устройство:"),
                                device_options,
                            ],
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        pool_id_input,
                                        fetch_button,
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                                output_text,
                                ft.Column(
                                    controls=[
                                        worker_count_text,
                                        ip_count_text,
                                        apply_button,
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        ft.Column(
                            controls=[
                                device_type_options,
                            ],
                            alignment=ft.MainAxisAlignment.START,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    controls=[
                        theme_switch,
                    ],
                    alignment=ft.MainAxisAlignment.END,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
        )
    )

# Запуск приложения
ft.app(target=main)
