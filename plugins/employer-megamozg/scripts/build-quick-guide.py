from pathlib import Path

from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parents[1]
OUTPUT = REPO_ROOT / "output" / "pdf" / "Claude_Рабочий_мегамозг_памятка.pdf"

PAGE_W, PAGE_H = A4
MARGIN = 42

INK = HexColor("#18212F")
MUTED = HexColor("#667085")
PURPLE = HexColor("#6D5DFB")
PURPLE_DARK = HexColor("#4B3FCC")
LAVENDER = HexColor("#F0EEFF")
MINT = HexColor("#DDF8EE")
MINT_DARK = HexColor("#157A64")
CORAL = HexColor("#FF765F")
CORAL_LIGHT = HexColor("#FFF0EC")
PAPER = HexColor("#F7F8FC")
LINE = HexColor("#E3E7EF")


def register_fonts() -> None:
    font_dir = Path("C:/Windows/Fonts")
    pdfmetrics.registerFont(TTFont("UI", str(font_dir / "arial.ttf")))
    pdfmetrics.registerFont(TTFont("UI-Bold", str(font_dir / "arialbd.ttf")))


def wrap(text: str, font: str, size: float, width: float) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        trial = word if not current else f"{current} {word}"
        if pdfmetrics.stringWidth(trial, font, size) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_lines(c: canvas.Canvas, text: str, x: float, y: float, width: float,
               font: str = "UI", size: float = 10.5, color=INK,
               leading: float | None = None) -> float:
    leading = leading or size * 1.35
    c.setFont(font, size)
    c.setFillColor(color)
    for line in wrap(text, font, size, width):
        c.drawString(x, y, line)
        y -= leading
    return y


def header(c: canvas.Canvas, page: int, label: str) -> None:
    c.setFillColor(INK)
    c.roundRect(MARGIN, PAGE_H - 88, PAGE_W - 2 * MARGIN, 46, 14, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("UI-Bold", 11)
    c.drawString(MARGIN + 18, PAGE_H - 61, label)
    c.setFont("UI", 9)
    c.setFillColor(HexColor("#C9D1DE"))
    c.drawRightString(PAGE_W - MARGIN - 18, PAGE_H - 61, f"стр. {page}")


def footer(c: canvas.Canvas) -> None:
    c.setStrokeColor(LINE)
    c.line(MARGIN, 32, PAGE_W - MARGIN, 32)
    c.setFont("UI", 8.5)
    c.setFillColor(MUTED)
    c.drawString(MARGIN, 18, "Рабочий мегамозг для Claude Pro")
    c.drawRightString(PAGE_W - MARGIN, 18, "Версия 1.1.0")


def pill(c: canvas.Canvas, x: float, y: float, number: str, title: str,
         body: str, color, background) -> None:
    w = (PAGE_W - 2 * MARGIN - 14) / 2
    h = 105
    c.setFillColor(background)
    c.roundRect(x, y - h, w, h, 16, fill=1, stroke=0)
    c.setFillColor(color)
    c.circle(x + 26, y - 27, 14, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("UI-Bold", 11)
    c.drawCentredString(x + 26, y - 31, number)
    c.setFillColor(INK)
    c.setFont("UI-Bold", 12)
    c.drawString(x + 49, y - 31, title)
    draw_lines(c, body, x + 18, y - 58, w - 36, size=9.5, color=MUTED, leading=12.5)


def menu_row(c: canvas.Canvas, x: float, y: float, number: str, text: str,
             tint, accent) -> None:
    w = (PAGE_W - 2 * MARGIN - 10) / 2
    c.setFillColor(tint)
    c.roundRect(x, y - 29, w, 29, 9, fill=1, stroke=0)
    c.setFillColor(accent)
    c.setFont("UI-Bold", 9.5)
    c.drawString(x + 11, y - 19, number)
    c.setFillColor(INK)
    c.setFont("UI", 9.2)
    c.drawString(x + 36, y - 19, text)


def page_one(c: canvas.Canvas) -> None:
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    header(c, 1, "БЫСТРЫЙ СТАРТ")

    y = PAGE_H - 125
    c.setFillColor(INK)
    c.setFont("UI-Bold", 25)
    c.drawString(MARGIN, y, "Claude, который снимает рутину")
    y -= 24
    draw_lines(
        c,
        "Один рабочий Project, простое меню и готовые сценарии для контента, клиентов, продаж и управления бизнесом.",
        MARGIN,
        y,
        PAGE_W - 2 * MARGIN,
        size=11,
        color=MUTED,
        leading=15,
    )

    top = PAGE_H - 190
    col2 = MARGIN + (PAGE_W - 2 * MARGIN - 14) / 2 + 14
    pill(c, MARGIN, top, "1", "Открой Project", "Всегда работай внутри проекта «Рабочий мегамозг». Здесь лежат знания бизнеса.", PURPLE, LAVENDER)
    pill(c, col2, top, "2", "Напиши СТАРТ", "Если не знаешь формулировку, просто напиши СТАРТ и выбери нужную цифру.", MINT_DARK, MINT)
    pill(c, MARGIN, top - 119, "3", "Приложи материал", "Добавь созвон, транскрибацию, скриншот, переписку, заметки или документ.", CORAL, CORAL_LIGHT)
    pill(c, col2, top - 119, "4", "Проверь факты", "Перед публикацией проверь имена, цены, даты, цифры, ссылки и обещания.", PURPLE_DARK, LAVENDER)

    y = top - 259
    c.setFont("UI-Bold", 15)
    c.setFillColor(INK)
    c.drawString(MARGIN, y, "Что можно выбрать в меню")
    y -= 20
    left = MARGIN
    right = MARGIN + (PAGE_W - 2 * MARGIN - 10) / 2 + 10
    items = [
        ("1", "Пост в Telegram"), ("2", "Сценарий Reels"),
        ("3", "Серия сторис"), ("4", "Разбор клиента"),
        ("5", "Кастдев и аудитория"), ("6", "Лид-магнит / воронка"),
        ("7", "Прогрев"), ("8", "Диалог и возражение"),
        ("9", "Упаковка профиля"), ("10", "Состояние бизнеса"),
        ("11", "Разобрать новый файл"), ("0", "Своя задача"),
    ]
    for index, (number, text) in enumerate(items):
        row = index // 2
        x = left if index % 2 == 0 else right
        tint = LAVENDER if row % 2 == 0 else white
        accent = PURPLE if index % 2 == 0 else MINT_DARK
        menu_row(c, x, y - row * 35, number, text, tint, accent)

    c.setFillColor(INK)
    c.roundRect(MARGIN, 48, PAGE_W - 2 * MARGIN, 48, 13, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("UI-Bold", 10.5)
    c.drawString(MARGIN + 16, 76, "Главный принцип")
    c.setFont("UI", 9.2)
    c.drawString(MARGIN + 16, 60, "Не объясняй Claude весь бизнес заново: актуальные факты должны жить в Project.")
    footer(c)
    c.showPage()


def info_box(c: canvas.Canvas, x: float, y: float, w: float, h: float,
             title: str, lines: list[str], accent, tint) -> None:
    c.setFillColor(tint)
    c.roundRect(x, y - h, w, h, 15, fill=1, stroke=0)
    c.setFillColor(accent)
    c.roundRect(x, y - h, 6, h, 3, fill=1, stroke=0)
    c.setFillColor(INK)
    c.setFont("UI-Bold", 12.5)
    c.drawString(x + 18, y - 25, title)
    cursor = y - 48
    for item in lines:
        c.setFillColor(accent)
        c.circle(x + 22, cursor + 3, 2.5, fill=1, stroke=0)
        cursor = draw_lines(c, item, x + 32, cursor + 7, w - 50, size=9.4, color=MUTED, leading=12.5) - 6


def page_two(c: canvas.Canvas) -> None:
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    header(c, 2, "ПРАВИЛА И БЫСТРЫЕ КОМАНДЫ")

    y = PAGE_H - 125
    c.setFillColor(INK)
    c.setFont("UI-Bold", 23)
    c.drawString(MARGIN, y, "Три правила рабочего кабинета")
    y -= 25
    draw_lines(c, "Эта система разгружает только тогда, когда знания актуальны, а решения подтверждены владельцем.", MARGIN, y, PAGE_W - 2 * MARGIN, size=10.8, color=MUTED, leading=14.5)

    box_w = (PAGE_W - 2 * MARGIN - 12) / 2
    top = PAGE_H - 190
    info_box(c, MARGIN, top, box_w, 176, "Что загружать", [
        "Продукты, цены, офферы и реальные условия.",
        "Кастдевы, созвоны, отзывы и живой язык аудитории.",
        "Сильные тексты автора, правила голоса и контент.",
        "Метрики, решения, ограничения и актуальные приоритеты.",
    ], MINT_DARK, MINT)
    info_box(c, MARGIN + box_w + 12, top, box_w, 176, "Что не загружать", [
        "Пароли, данные банковских карт и секретные ключи.",
        "Лишние персональные данные клиентов.",
        "Несколько противоречивых версий одного оффера.",
        "Непроверенные цифры, отзывы и обещания как факты.",
    ], CORAL, CORAL_LIGHT)

    y = top - 205
    c.setFillColor(INK)
    c.setFont("UI-Bold", 15)
    c.drawString(MARGIN, y, "Когда обновлять Project")
    y -= 25
    steps = [
        ("После созвона", "положить новый материал во входящие и попросить Claude сделать выжимку."),
        ("После решения", "подготовить точный фрагмент и обновить один профильный файл."),
        ("Раз в неделю", "очистить входящие, обновить метрики и зафиксировать три приоритета."),
        ("Раз в месяц", "проверить продукты, аудиторию, воронки, голос и правила продаж."),
    ]
    for i, (title, body) in enumerate(steps, 1):
        c.setFillColor(white)
        c.roundRect(MARGIN, y - 54, PAGE_W - 2 * MARGIN, 46, 12, fill=1, stroke=0)
        c.setFillColor(PURPLE)
        c.circle(MARGIN + 23, y - 31, 12, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont("UI-Bold", 9.5)
        c.drawCentredString(MARGIN + 23, y - 34, str(i))
        c.setFillColor(INK)
        c.setFont("UI-Bold", 10.2)
        c.drawString(MARGIN + 45, y - 25, title)
        c.setFont("UI", 9.2)
        c.setFillColor(MUTED)
        c.drawString(MARGIN + 45, y - 41, body)
        y -= 56

    c.setFillColor(INK)
    c.roundRect(MARGIN, 52, PAGE_W - 2 * MARGIN, 116, 14, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("UI-Bold", 11)
    c.drawString(MARGIN + 17, 145, "Быстрые команды")
    c.setFont("UI", 8.8)
    c.setFillColor(HexColor("#DCE2EC"))
    c.drawString(MARGIN + 17, 124, "НАСТРОЙКА | ОБНОВИТЬ БАЗУ | ПРОВЕРЬ ПЕРЕД ПУБЛИКАЦИЕЙ")
    c.drawString(MARGIN + 17, 106, "ДЕНЬ | НЕДЕЛЯ | РАЗБОР НЕДЕЛИ | ЧТО Я УПУСКАЮ")
    c.setFont("UI-Bold", 9.2)
    c.setFillColor(white)
    c.drawString(MARGIN + 17, 78, "Для клиентов: один чат - один клиент.")
    footer(c)
    c.showPage()


def main() -> None:
    register_fonts()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUTPUT), pagesize=A4)
    c.setTitle("Рабочий мегамозг для Claude Pro - памятка v1.1")
    c.setAuthor("juicix")
    page_one(c)
    page_two(c)
    c.save()
    print(OUTPUT)


if __name__ == "__main__":
    main()
