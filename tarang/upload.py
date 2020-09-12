from flask import Flask, request
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "It is secret key"



@app.route('/')
@app.route('/upload')
def upload_file():
   return '<html><body><form action = "/uploader" method = "POST" enctype = "multipart/form-data"><input type = "file" name = "file" /><input type = "submit"/></form></body></html>'
    
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_files():
   if request.method == 'POST':
      f = request.files['file']
      app.config['UPLOAD_FOLDER'] = 'static/images/'
      f.save('static/'+secure_filename(f.filename))
      return 'file uploaded successfully'


if __name__ == '__main__':
	app.run(debug=True)