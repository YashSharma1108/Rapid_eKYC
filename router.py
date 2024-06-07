from flask import Flask, request, render_template, jsonify
import dbController as db
import base64
import pyodbc

app = Flask(__name__)

# Function to connect to the SQL Server database using Windows authentication
def get_db_connection():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=INVL0077;'
        'DATABASE=RapidKyc;'
        'Trusted_Connection=yes;'
    )
    return conn

@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')

@app.route("/blog", methods=['GET'])
def blog():
    return render_template('blog.html')

@app.route("/box", methods=['GET'])
def box():
    return render_template('box.html')

@app.route("/step1", methods=['GET'])
def step1():
    return render_template('step1.html')

@app.route("/step2", methods=['GET'])
def step2():
    return render_template('step2.html')

@app.route("/sample", methods=['GET'])
def sample():
    return render_template('sample.html')

@app.route("/step4", methods=['GET'])
def step4():
    return render_template('step4.html')

@app.route("/fetchData", methods=['POST'])
def fetchData():
    try:
        captured_image = request.form['capturedImage']
        # Decode the base64 image data
        image_data = base64.b64decode(captured_image.split(",")[1])

        userinfo = db.fetchData(image_data)
        return jsonify({"message": "Image processed successfully", "userinfo": userinfo}), 200
    except Exception as e:
        print(f"Error processing image: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route("/verifyFace", methods=['GET'])
def verifyFace():
    try:
        image = request.files['userImage']
        data = image.stream.read()
        # Assuming face1 and face2 are correctly defined and used in db.compareFace
        return db.compareFace(face1, face2)
    except Exception as e:
        print(f"Error verifying face: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route("/report/addreport", methods=['POST'])
def add_report():
    try:
        username = request.form['username']
        note = request.form['note']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO report (username, note) VALUES (?, ?)", (username, note))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Report submitted successfully"}), 200
    except Exception as e:
        print(f"Error submitting report: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == '__main__':
    app.run(debug=True)
