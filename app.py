from flask import Flask, request, jsonify
from tinydb import TinyDB, Query
import re

app = Flask(__name__)
db = TinyDB('form_templates.json')

def validate_email(email):
       return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def validate_phone(phone):
       return re.match(r"^\+7 \d{3} \d{3} \d{2} \d{2}$", phone)

def validate_date(date):
       return re.match(r"^(\d{2}|\d{4})[.-](\d{2})[.-](\d{2}|\d{4})$", date)

@app.route('/get_form', methods=['POST'])
def get_form():
       data = request.form.to_dict()
       form_templates = db.all()
       for template in form_templates:
           fields = {key: template[key] for key in template if key != 'name'}
           if all(key in data and fields[key] == type_field(data[key]) for key in fields):
               return jsonify(template['name'])

       return jsonify({key: type_field(data[key]) for key in data})

def type_field(value):
       if validate_date(value):
           return "date"
       elif validate_phone(value):
           return "phone"
       elif validate_email(value):
           return "email"
       return "text"

if __name__ == '__main__':
    app.run(debug=True)