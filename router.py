from flask import Flask, request, render_template
import dbController as db

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')

@app.route("/blog", methods=['GET'])
def blog():
    return render_template('blog.html')

@app.route("/box", methods=['GET'])
def box():
    return render_template('box.html')

@app.route("/step1", methods=['Get'])
def step1():
    return render_template('step1.html')

@app.route("/step2", methods=['get'])
def step2():
    return render_template('step2.html')

@app.route("/sample", methods=['get'])
def sample():
    return render_template('sample.html')

@app.route("/fetchData", methods=['POST'])
def fetchData():
    file = request.files['image']

    data = file.stream.read()
    # data = base64.b64encode(data).decode()

    userinfo = db.fetchData(data)



@app.route("/verifyFace", methods=['GET'])
def verifyFace():
    image = request.files['userImage']

    data = image.stream.read()

    return db.compareFace(face1, face2)




#############################report#################################################


@app.route("/report/addreport", methods=['POST'])
def addreport():
    return "this is coming from server."



if __name__ == '__main__':
    app.run(debug=True) 