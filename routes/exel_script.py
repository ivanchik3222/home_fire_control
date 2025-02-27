from flask import Blueprint, jsonify, send_file
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side
from db_models import Inspection_form, Inspection_ticket
from io import BytesIO

exel_bp = Blueprint('excel', __name__)

def get_excel(form_id):
    # Получаем запись из БД
    form = Inspection_form.query.get(form_id)
    if not form:
        return jsonify({"error": "Форма не найдена"}), 404

    # Получаем запись из Inspection_ticket
    ticket = Inspection_ticket.query.filter_by(assigment_id=form.assigment_id).first()
    
    # Преобразуем JSON-ответы в список
    json_data = form.answers  # Это словарь {'question1': 'Yes', 'question2': 'No'}
    data = [{"№": i + 1, "вопрос": q, "ответ": a} for i, (q, a) in enumerate(json_data.items())]

    # Создаём Excel-файл
    wb = Workbook()
    ws = wb.active
    ws.title = f"Inspection Report {form_id}"

    # Добавляем стили
    bold_center = Font(bold=True)
    center_align = Alignment(horizontal="center")
    thin_border = Border(left=Side(style="thin"), right=Side(style="thin"), top=Side(style="thin"), bottom=Side(style="thin"))
    top_bottom_border = Border(top=Side(style="thin"), bottom=Side(style="thin"))  # Только верхняя и нижняя граница
    no_border = Border()  # Полностью убирает границы

    # Заполняем заголовки
    headers = ["№", "Вопрос", "Ответ"]
    ws.append(headers)

    for col_num, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num, value=header)
        cell.font = bold_center
        cell.alignment = center_align
        cell.border = thin_border

    # Заполняем основную таблицу
    for row_index, row in enumerate(data, start=2):
        ws.append([row["№"], row["вопрос"], row["ответ"]])

        for col_index in range(1, 4):
            cell = ws.cell(row=row_index, column=col_index)

            if row_index == 4:  
                cell.border = no_border  # Полностью убираем границы
            else:
                cell.border = thin_border  # Обычные границы

    # **Переносим вторую таблицу вправо (начиная с колонки E)**
    if ticket:
        start_col = 5  # E-колонка
        start_row = 1

        # Объединяем заголовок E1:F1
        ws.merge_cells(start_row=start_row, start_column=start_col, end_row=start_row, end_column=start_col + 1)
        header_cell = ws.cell(row=start_row, column=start_col, value="Данные о проверке")
        header_cell.font = bold_center
        header_cell.alignment = center_align
        header_cell.border = thin_border

        # Данные второй таблицы
        ticket_data = [
            ["Дата проверки", ticket.inspection_date.strftime("%d.%m.%Y") if ticket.inspection_date else "Нет данных"],
            ["Категория жителей", ticket.resident_category or "Нет данных"],
            ["Количество человек в семье", str(ticket.family_size) or "Нет данных"]
        ]

        for row_index, row in enumerate(ticket_data, start=start_row + 1):
            for col_index, value in enumerate(row, start=start_col):
                cell = ws.cell(row=row_index, column=col_index, value=value)
                cell.border = thin_border  # Границы для всей второй таблицы

    # **Исправляем границы 7-й строки**
    if ws.max_row >= 7:
        for col_index in range(1, 3):  # A и B должны иметь границы
            cell = ws.cell(row=7, column=col_index)
            cell.border = thin_border
        # C (3-я колонка) не должна иметь границ
        cell_7C = ws.cell(row=7, column=3)
        cell_7C.border = no_border

    # Автоматическое расширение первого столбца
    max_width = max(len(str(cell.value)) for cell in ws["A"] if cell.value)  # Самая длинная строка в первом столбце
    ws.column_dimensions["A"].width = max_width + 2

    # Настраиваем ширину остальных столбцов
    ws.column_dimensions["B"].width = 30  # Вопрос
    ws.column_dimensions["C"].width = 20  # Ответ

    # Настроим ширину для второй таблицы
    ws.column_dimensions["E"].width = 25
    ws.column_dimensions["F"].width = 20

    # Сохраняем в память (не создавая файл на диске)
    file_stream = BytesIO()
    wb.save(file_stream)
    file_stream.seek(0)

    return send_file(file_stream, as_attachment=True, download_name=f"inspection_report_{form_id}.xlsx", mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


exel_bp.add_url_rule('/get_excel/<int:form_id>', view_func=get_excel, methods=['GET'])
