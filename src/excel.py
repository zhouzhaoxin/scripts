from openpyxl import load_workbook


def write_line_by_line(file_path, new_row_data):
    wb = load_workbook(file_path)
    ws = wb.worksheets[0]

    for row_data in new_row_data:
        ws.append(row_data)

    wb.save(file_path)
