from flask import Flask, render_template, request,jsonify
from flask_mysqldb import MySQL
from keras.models import load_model
import cv2
import numpy as np
import base64
from PIL import Image
import io
import re

import yaml

img_size=100
db=yaml.safe_load(open('db.yaml'))

app = Flask(__name__, static_folder="./templates/assets")
app.config['MYSQL_HOST']=db['mysql_host']
app.config['MYSQL_USER']=db['mysql_user']
app.config['MYSQL_PASSWORD']=db['mysql_password']
app.config['MYSQL_DB']=db['mysql_db']
app.config['MYSQL_PORT']=db['mysql_port']

mysql=MySQL(app)

model=load_model('model-018.h5')

label_dict={0:'Covid19 Negative', 1:'Covid19 Positive'}

def preprocess(img):

	img=np.array(img)

	if(img.ndim==3):
		gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	else:
		gray=img

	gray=gray/255
	resized=cv2.resize(gray,(img_size,img_size))
	reshaped=resized.reshape(1,img_size,img_size)
	return reshaped

@app.route("/",methods=["GET","POST"])
def index():
	if request.method=='POST':
		userdet=request.form
		idd=userdet['srno']
		name=userdet['fullname']
		age=userdet['age1']
		resu=userdet['Radiob']
		cur=mysql.connection.cursor()
		cur.execute("INSERT INTO coviddb(id,name,age,result) VALUES(%s,%s,%s,%s)",(idd,name,age,resu))
		mysql.connection.commit()
		cur.close()
	return(render_template("index.html"))

@app.route("/predict", methods=["POST"])
def predict():
	print('HERE')
	message = request.get_json(force=True)
	encoded = message['image']
	decoded = base64.b64decode(encoded)
	dataBytesIO=io.BytesIO(decoded)
	dataBytesIO.seek(0)
	image = Image.open(dataBytesIO)

	test_image=preprocess(image)

	prediction = model.predict(test_image)
	result=np.argmax(prediction,axis=1)[0]
	accuracy=float(np.max(prediction,axis=1)[0])

	label=label_dict[result]

	print(prediction,result,accuracy)

	response = {'prediction': {'result': label,'accuracy': accuracy}}

	return response

@app.route("/thankyou.html", methods=["POST"])
def thanks():
	if request.method=='POST':
		userdet=request.form
		idd=userdet['srno']
		name=userdet['fullname']
		age=userdet['age1']
		resu=userdet['Radiob']
		cur=mysql.connection.cursor()
		cur.execute("INSERT INTO coviddb(id,name,age,result) VALUES(%s,%s,%s,%s)",(idd,name,age,resu))
		mysql.connection.commit()
		cur.close()
	return(render_template("thankyou.html"))

app.run(debug=True)

#<img src="" id="img" crossorigin="anonymous" width="400" alt="Image preview...">
	