import os
from flask import Flask, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
# from flask import send_from_directory

from predict_pix_bru import pix_bru_classifier

UPLOAD_FOLDER = '/Users/sabihhasan/Desktop/projects/images_webapp/images_upload/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'JPG'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# def classifier():
#     print(predict_classifier('testing/bruno/IMG_4236.jpg'))


def html_template():
	return """
    <!doctype html>
    <title>Pixel/Bruno Classifier</title>
    <h1>Pixel and Bruno Classifier</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    """


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            image_path = os.path.join('./images_upload/', filename)
            return classify(image_path)
            # return html_template()

    return html_template()


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/uploads/<filename>')
def classify(image_path):
    msg = pix_bru_classifier(image_path)
    index_html = html_template()
    output_html = index_html + '\n' + '<h1>%s</h1>' % msg
    return output_html



if __name__ == '__main__':
    app.secret_key = 'flaskproject_secretkey_2'
    app.run(debug=True)




