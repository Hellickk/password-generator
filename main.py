import flet as ft
import secrets
import string

def main(page: ft.Page):
    # Настройки окна (размер как у экрана смартфона)
    page.title = "Генератор безопасных паролей"
    page.window.width = 400
    page.window.height = 620
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20

    # Функция оценки надежности пароля
    def check_strength(password):
        length = len(password)
        if length < 8:
            return "Слабый (легко взломать)", ft.Colors.RED_400
        elif length < 12:
            return "Средний (подойдет для соцсетей)", ft.Colors.ORANGE_400
        else:
            return "Надежный (взломостойкий)", ft.Colors.GREEN_400

    # Главная функция генерации пароля
    def generate_password(e):
        alphabet = string.ascii_lowercase
        guaranteed_chars = [secrets.choice(string.ascii_lowercase)]

        if use_upper.value:
            alphabet += string.ascii_uppercase
            guaranteed_chars.append(secrets.choice(string.ascii_uppercase))
            
        if use_digits.value:
            alphabet += string.digits
            guaranteed_chars.append(secrets.choice(string.digits))
            
        if use_symbols.value:
            symbols = "!@#$%^&*()_+-="
            alphabet += symbols
            guaranteed_chars.append(secrets.choice(symbols))

        length = int(length_slider.value)
        
        # Добираем оставшиеся символы до нужной длины
        remaining_length = length - len(guaranteed_chars)
        password_chars = guaranteed_chars + [secrets.choice(alphabet) for _ in range(remaining_length)]
        
        # Перемешиваем символы в случайном порядке (криптографически безопасно)
        secrets.SystemRandom().shuffle(password_chars)
        password = "".join(password_chars)

        # Выводим пароль и обновляем статус надежности
        password_field.value = password
        text, color = check_strength(password)
        strength_text.value = f"Надежность: {text}"
        strength_text.color = color
        page.update()

    # Функция копирования в буфер обмена
    def copy_to_clipboard(e):
        if password_field.value:
            page.set_clipboard(password_field.value)
            page.open(ft.SnackBar(ft.Text("Пароль скопирован в буфер обмена!")))

    # --- ЭЛЕМЕНТЫ ИНТЕРФЕЙСА ---
    title = ft.Text("🔐 Безопасный пароль", size=24, weight=ft.FontWeight.BOLD)

    password_field = ft.TextField(
        label="Ваш пароль",
        read_only=True,
        text_size=18,
        border_color=ft.Colors.BLUE_400,
    )

    strength_text = ft.Text("Надежность: —", size=14)

    copy_btn = ft.Button(
        "Скопировать",
        icon=ft.Icons.COPY,
        on_click=copy_to_clipboard,
        width=170
    )

    gen_btn = ft.Button(
        "Создать",
        icon=ft.Icons.REFRESH,
        on_click=generate_password,
        bgcolor=ft.Colors.BLUE_600,
        color=ft.Colors.WHITE,
        width=170
    )

    length_label = ft.Text("Длина пароля: 14 символов")
    
    def slider_changed(e):
        length_label.value = f"Длина пароля: {int(length_slider.value)} символов"
        page.update()

    length_slider = ft.Slider(
        min=6, max=32, divisions=26, value=14, on_change=slider_changed
    )

    use_upper = ft.Checkbox(label="Заглавные буквы (A-Z)", value=True)
    use_digits = ft.Checkbox(label="Цифры (0-9)", value=True)
    use_symbols = ft.Checkbox(label="Спецсимволы (!@#$%)", value=True)

    # Собираем все элементы на экране
    page.add(
        title,
        ft.Divider(height=10, color="transparent"),
        password_field,
        strength_text,
        ft.Row([gen_btn, copy_btn], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ft.Divider(height=20),
        length_label,
        length_slider,
        use_upper,
        use_digits,
        use_symbols
    )

    # Сразу генерируем первый пароль при запуске
    generate_password(None)

# Запуск приложения
ft.run(main)
