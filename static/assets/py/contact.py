# from flask import Flask, request, jsonify
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)

# # Configure the SQL Server database connection
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://INVL0077/RapidKyc?driver=ODBC+Driver+17+for+SQL+Server'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

# # Define a model for the ContactMessages table
# class ContactMessage(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(100), nullable=False)
#     subject = db.Column(db.String(255), nullable=False)
#     message = db.Column(db.Text, nullable=False)
#     created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())

#     def __repr__(self):
#         return f'<ContactMessage {self.id}>'

# # Route to handle form submission
# @app.route('/contact', methods=['POST'])
# def contact_form():
#     # Collect form data
#     data = request.form
#     name = data.get('name')
#     email = data.get('email')
#     subject = data.get('subject')
#     message = data.get('message')

#     # Create a new ContactMessage instance
#     new_message = ContactMessage(name=name, email=email, subject=subject, message=message)

#     try:
#         # Add the new message to the database
#         db.session.add(new_message)
#         db.session.commit()
#         return jsonify({'message': 'Your message has been sent. Thank you!'}), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True)
