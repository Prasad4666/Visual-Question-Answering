# import the necessary packages
from flask import Flask, render_template, redirect, url_for, request,session,Response
from werkzeug import secure_filename
from DNNtest import *
import os
import cv2

app = Flask(__name__)

app.secret_key = '1234'
app.config["CACHE_TYPE"] = "null"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/', methods=['GET', 'POST'])
def landing():
	return render_template('home.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
	return render_template('home.html')

@app.route('/info', methods=['GET', 'POST'])
def info():
	return render_template('info.html')



@app.route('/image', methods=['GET', 'POST'])
def image():
	if request.method == 'POST':
		if request.form['sub']=='Upload':
			savepath = r'upload/'
			photo = request.files['photo']
			photo.save(os.path.join(savepath,(secure_filename(photo.filename))))
			image = cv2.imread(os.path.join(savepath,secure_filename(photo.filename)))
			cv2.imwrite(os.path.join("static/images/","test_image.jpg"),image)
			return render_template('image.html')
		elif request.form['sub'] == 'Answer':
			que = request.form['que'].lower()
			que1 = que.split(" ")
			objects = objectDetector()
			if('is there' in que):
				obj = que1[2]
				if(obj in objects):
					ans = "Yes "+obj+" is there in picture"
				else:
					ans = "No "+obj+" is not there in picture"
			elif('what are different' in que):
				ans = "Picture contains "+str(objects)
			elif 'what is the color' in que:
                # Assuming you have a function getColor() to get the color of the object
				obj = que1[2]
				if obj in objects:
					color = getColor(obj, image)  # getColor function needs to be defined
					ans = "The color of " + obj + " is " + color + "."
				else:
					ans = "Object not found in the picture."
			elif 'how many objects' in que:
				ans = "There are " + str(len(objects)) + " objects in the picture."
			else:
				ans = "I'm sorry, I don't understand the question."
			return render_template('image.html',result1=ans)
	return render_template('image.html')

# No caching at all for API endpoints.
@app.after_request
def add_header(response):
	# response.cache_control.no_store = True
	response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
	response.headers['Pragma'] = 'no-cache'
	response.headers['Expires'] = '-1'
	return response


if __name__ == '__main__' and run:
	app.run(host='0.0.0.0', debug=True, threaded=True)
