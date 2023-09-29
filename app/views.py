from flask import current_app, Blueprint, render_template, request, session, redirect, jsonify, url_for, flash
import requests
from .models import PredictImageType, PredictDisease
from base64 import b64encode
from .forms import ImageForm


main = Blueprint('main', __name__)


def clear_session(*args):
    if args:
        for arg in args:
            session.pop(arg)
        return
    
    session.clear()
 

@main.route('/sobre', methods=['GET'])
def home():
    return render_template('PaginaSobre.html')


@main.route('/', methods=['GET'])
def dashboard():
    form = ImageForm()

    return render_template('Dashboard.html', form=form)


@main.route('/process-data', methods=['POST'])
def process_data():
    form = ImageForm()
    
    session['image'] = form.image.data.read()
    session['class_name'], session['class_index'] = PredictImageType(session['image'])

    response = {'message': session['class_name'], 'index': str(session['class_index']), 'image': str(b64encode(session['image']).decode('utf-8'))}

    return jsonify(response)


@main.route('/redirect-to-model', methods=['POST'])
def redirect_model():

    if request.form:
        session['class_index'] = int(request.form.get('index'))


    if (session['class_index'] == 5):
        api_url = "https://knee-medvision-85e204f5fcab.herokuapp.com/kneeRXClassifier"
        
        files = {'uploaded_file': ('image.jpg', session['image'])}  
        
        response = requests.post(api_url, files=files)
        
        if response.status_code == 200:
            pred_dict = response.json()

    elif (session['class_index'] == 4):
        api_url = "https://knee-medvision-85e204f5fcab.herokuapp.com/kneeRXClassifier"
        
        files = {'uploaded_file': ('image.jpg', session['image'])}  
        
        response = requests.post(api_url, files=files)
        
        if response.status_code == 200:
            pred_dict = response.json()
    else:
        pred_dict = PredictDisease(session['image'], session['class_index'])

    flash(b64encode(session['image']).decode('utf-8'))
    flash(pred_dict)

    clear_session('class_name', 'class_index', 'image')

    return redirect(url_for('main.dashboard'))


@main.route("/classificationApp", methods=['GET','POST'])
def classification_api():
    uploaded_file = request.files.get('uploaded_file')
    if uploaded_file:
        file_data = uploaded_file.read()
        class_name, class_index = PredictImageType(file_data)
        if (class_name != 'Non medical image'):
            if (class_name == "Knee XR"):
                api_url = "https://knee-medvision-85e204f5fcab.herokuapp.com/kneeRXClassifier"
                
                files = {'uploaded_file': ('image.jpg', file_data)}  
                
                response = requests.post(api_url, files=files)
                
                if response.status_code == 200:
                    resultado = response.json()
                    return {
                        "tipoImagem": class_name,
                        "doenca": resultado
                    }
                else:
                    return {
                        "tipoImagem": class_name,
                        "error": "Falha ao enviar imagem para classificação"
                    }
            elif (class_name == "Knee MRI"):
                api_url = "https://knee-medvision-85e204f5fcab.herokuapp.com/kneeMRIClassifier"
                
                files = {'uploaded_file': ('image.jpg', file_data)}  
                
                response = requests.post(api_url, files=files)
                
                if response.status_code == 200:
                    resultado = response.json()
                    return {
                        "tipoImagem": class_name,
                        "doenca": resultado
                    }
                else:
                    return {
                        "tipoImagem": class_name,
                        "error": "Falha ao enviar imagem para classificação"
                    }
            else:
                resultado = PredictDisease(file_data, class_index)
                return {
                    "tipoImagem": class_name,
                    "doenca": resultado
                }
        else:
            return {
                "tipoImagem": class_name,
            }


@main.route("/clear-session", methods=['POST'])
def clear_session_route():
    session.clear()
    return 'Session cleared'

@current_app.errorhandler(404) 
def not_found(e):
  return render_template("404.html")


@current_app.errorhandler(405) 
def not_allowed(e):
  return render_template("404.html")