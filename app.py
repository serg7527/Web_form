from flask import Flask, request, jsonify
from tinydb import TinyDB, Query
import re

app = Flask(__name__)
db = TinyDB('forms_db.json')

# Регулярные выражения для валидации типов полей
date_pattern = re.compile(r'^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.(\d{4})$|^\d{4}-\d{2}-\d{2}$')
phone_pattern = re.compile(r'^\+7 \d{3} \d{3} \d{2} \d{2}$')
email_pattern = re.compile(r'^[\w.-]+@([\w-]+\.)+[\w-]{2,4}$')

@app.route('/get_form', methods=['POST'])
def get_form():
    data = request.json  # Получаем JSON-данные
    
    # Получаем все шаблоны форм из базы данных
    FormTemplate = Query()
    templates = db.all()

    # Проверяем каждый шаблон из базы
    for template in templates:
        template_fields = template['fields']

        # Проверяем совпадение полей
        if all(field in data and validate_field(data[field], template_fields[field]) for field in template_fields):
            return jsonify({"form_name": template['name']})

    # Если не нашли подходящий шаблон, возвращаем несоответствующие поля с типами
    response = {}
    for field_name in data.keys():
        if field_name not in template_fields:
            response[field_name] = determine_field_type(data[field_name])

    return jsonify(response)

def validate_field(value, field_type):
    if field_type == 'date':
        return bool(date_pattern.match(value))
    elif field_type == 'phone':
        return bool(phone_pattern.match(value))
    elif field_type == 'email':
        return bool(email_pattern.match(value))
    return True  # Для текстовых полей валидация не требуется

def determine_field_type(value):
    if bool(date_pattern.match(value)):
        return 'date'
    elif bool(phone_pattern.match(value)):
        return 'phone'
    elif bool(email_pattern.match(value)):
        return 'email'
    return 'text'  # Если не подходит ни под одно, то это текст

if __name__ == '__main__':
    app.run(debug=True)