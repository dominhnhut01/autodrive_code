from google.cloud import storage

from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

from PIL import Image
import os
import numpy as np
import random as rd
import string

import load_model
from path_finding import dijksar_algorithm

#Set up the credential for Google Cloud
credential_path="prediction-deployment-49af6ad6168f.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

#Initialize Flask object and SQLAlchemy
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

#Loading the model and saving the segmentation result to the path: "/temp_img/seg_map.png"
model_path='trained_model/final_model.tar.gz'
MODEL=load_model.DeepLabModel(model_path)


#Initialize the Google Cloud information
UPLOAD_FOLDER='/tmp'
CLOUD_PROJECT = 'prediction-deployment'
BUCKET_NAME = 'tf1-model'
IMAGE_FOLDER = 'images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = "TESTSTRING"

client = storage.Client()
bucket = client.get_bucket(BUCKET_NAME)


def key_generator():
	#Generating a unique key for each request
	num = rd.randint(0,100)
	letter = rd.choice(string.ascii_letters)
	return str(num)+str(letter)

def img_resize(img_path):
	#Resizing the input image to the appropriate size
	img = Image.open(img_path)
	init_width,init_height=img.size
	hw_ratio= float(init_height)/float(init_width)
	width=450
	height=int(float(width)*hw_ratio)
	img = img.resize((width,height))
	os.remove(img_path)
	if img.mode == 'L':
		pass
	else:
		img = img.convert('RGB')
	img.save(img_path)


class ImgInfo(db.Model):
	#Database
	id = db.Column(db.Integer, primary_key=True)
	x1_coordinate = db.Column(db.Integer, nullable=True)
	x2_coordinate = db.Column(db.Integer, nullable=True)
	y1_coordinate = db.Column(db.Integer, nullable=True)
	y2_coordinate = db.Column(db.Integer, nullable=True)

	unique_key = db.Column(db.String(200),nullable = True)
	img_url = db.Column(db.String(200),nullable = True)
	seg_map_url = db.Column(db.String(200),nullable = True)
	shortest_path_url = db.Column(db.String(200),nullable = True)

	def __repr__(self):
		return '<Element: %r>' %self.element_name


@app.route('/',methods= ['POST','GET'])
def main():
	#Homepage
	return render_template('index.html')

@app.route('/upload_file', methods = ['GET', 'POST'])
def upload_file():
	#Upload the client's image to the web and save it to Google Cloud for further processing
	#Predict the segmentation map for the input image and save it to Google Cloud
	try:
		if request.method == 'POST':
			#Uploading the image the client submit to Google Cloud
			unique_key = key_generator()

			input_img = request.files['image']
			filename = "input_img"+"_"+unique_key
			img_path = 'templates/temp_img/{}.jpg'.format(filename)
			input_img.save(img_path)
			img_resize(img_path)
			GCP_name = '{}/{}'.format(IMAGE_FOLDER, filename)
			blob = storage.Blob(GCP_name, bucket)
			blob.upload_from_filename(img_path)

			blob = bucket.blob(GCP_name)

			#Make the image public for viewing
			blob.make_public()

			img_url = blob.public_url



			load_model.main(MODEL, img_path, unique_key)


			#Uploading the segmentation map result to Google Cloud
			seg_map_name = "seg_map"+"_"+unique_key
			seg_map_path = 'templates/temp_img/{}.jpg'.format(seg_map_name)
			img_resize(seg_map_path)
			GCP_seg_map_name='{}/{}'.format(IMAGE_FOLDER,seg_map_name)
			blob = storage.Blob(GCP_seg_map_name, bucket)
			blob.upload_from_filename(seg_map_path)

			blob = bucket.blob(GCP_seg_map_name)

			#Make the image public for viewing
			blob.make_public()

			seg_map_url = blob.public_url

			current_img = ImgInfo(unique_key=unique_key,img_url=img_url,seg_map_url=seg_map_url)

			try:
				db.session.add(current_img)
				db.session.commit()
				return render_template('initialize.html', current_img= current_img)
			except:
				return 'Error adding data to database'
		else:
			return render_template('upload_file.html')

	except:
		return render_template('error_catching.html')

@app.route('/add/<x1_coordinate>/<x2_coordinate>/<y1_coordinate>/<y2_coordinate>/<id>', methods= ['POST','GET'])
def add(x1_coordinate,x2_coordinate,y1_coordinate,y2_coordinate,id):	
	#Saving the coordinate of the points the client chose to the database
	try:	
		current_img= ImgInfo.query.get_or_404(id)

		current_img.x1_coordinate = int(round(float(x1_coordinate),0))
		current_img.x2_coordinate = int(round(float(x2_coordinate),0))
		current_img.y1_coordinate = int(round(float(y1_coordinate),0))
		current_img.y2_coordinate = int(round(float(y2_coordinate),0))

		print(current_img.x1_coordinate,current_img.y1_coordinate,current_img.x2_coordinate,current_img.y2_coordinate)
		db.session.commit()
		return redirect('/result/{}'.format(current_img.id))

	except:
		return render_template('error_catching.html')

@app.route('/result/<id>', methods= ['POST','GET'])
def result(id):	
	#Generating the shortest path between two points
	try:	
		current_img= ImgInfo.query.get_or_404(id)
		seg_map_npy = np.load("templates/temp_img/seg_map_npy_{}.npy".format(current_img.unique_key))

		x1_coordinate= current_img.x1_coordinate
		x2_coordinate= current_img.x2_coordinate
		y1_coordinate= current_img.y1_coordinate
		y2_coordinate= current_img.y2_coordinate

		skeleton, shortest_path=dijksar_algorithm.dijksar(seg_map_npy,(int(y1_coordinate),int(x1_coordinate)),(int(y2_coordinate),int(x2_coordinate)))
		temp_shortest_path = np.where(shortest_path==0,255,shortest_path)
		shortest_path = np.where(temp_shortest_path==1,0,temp_shortest_path)
		
		PIL_shortest_path = Image.fromarray(shortest_path)
		PIL_shortest_path = PIL_shortest_path.convert('L')
		
		shortest_path_dir = 'templates/temp_img/shortest_path.jpg'
		PIL_shortest_path.save(shortest_path_dir)
		img_resize(shortest_path_dir)

		shortest_path_name = 'shortest_path'+"_"+current_img.unique_key
		GCP_shortest_path_name='{}/{}'.format(IMAGE_FOLDER, shortest_path_name)
		blob = storage.Blob(GCP_shortest_path_name, bucket)
		blob.upload_from_filename(shortest_path_dir)

		blob = bucket.blob(GCP_shortest_path_name)

		#Make the image public for viewing
		blob.make_public()

		shortest_path_url = blob.public_url
		current_img.shortest_path_url=shortest_path_url

		db.session.commit()
		return render_template('result.html', current_img=current_img)	

	except:
		return render_template('error_catching.html')

if __name__=='__main__':
	app.run(debug=True, host='0.0.0.0')