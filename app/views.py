from flask import current_app, Blueprint, render_template, request, session, redirect, jsonify, url_for, flash
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
 

@main.route('/', methods=['GET'])
def home():
    return render_template('PaginaInicial.html')


@main.route('/dashboard', methods=['GET'])
def dashboard():
    form = ImageForm()

    return render_template('Dashboard.html', form=form)


@main.route('/process-data', methods=['POST'])
def process_data():
    form = ImageForm()
    
    if form.validate_on_submit():
        session['image'] = form.image.data.read()
        session['class_name'], session['class_index'] = PredictImageType(session['image'])

        response = {'message': session['class_name'], 'index': str(session['class_index']), 'image': str(b64encode(session['image']).decode('utf-8'))}

        return jsonify(response)
    
    errors = form.errors
    return jsonify(errors)


@main.route('/redirect-to-model', methods=['POST'])
def redirect_model():    
    pred_dict = PredictDisease(session['image'], session['class_index'])

    flash(b64encode(session['image']).decode('utf-8'))
    flash(pred_dict)

    clear_session('class_name', 'class_index', 'image')

    return redirect(url_for('main.dashboard'))


# @main.route("/classification-app", methods=['GET','POST'])
# def classification_api():
#     session['class_name'], session['class_index'] = PredictImageType(request.files['image'])
#     pred_dict = PredictDisease(session['image'], session['class_index'])
#     new_classification = Classifications(
#         user_id=current_user.id,
#         image=b64encode(session['image']).decode('utf-8'),
#         class_name=session['class_name'],
#         prediction=pred_dict,
#     )
#     return {"message": new_classification}


@current_app.errorhandler(404) 
def not_found(e):
  return render_template("404.html")


@current_app.errorhandler(405) 
def not_allowed(e):
  return render_template("404.html")