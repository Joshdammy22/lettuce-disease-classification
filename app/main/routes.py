from flask import Blueprint, render_template, url_for, flash, redirect, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from .forms import UploadForm
from app.models import Image as DBImage, Diagnosis, DiseaseInfo, db, Feedback
from app.utils import *
from PIL import Image as PILImage  # Use an alias for PIL's Image module



main = Blueprint('main', __name__)

@main.route("/")
def index():
    return render_template('index.html')


@main.route("/history")
@login_required
def history():
    # Define the number of results per page
    per_page = 10
    # Get the page number from the request; default to 1 if not provided
    page = request.args.get('page', 1, type=int)
    # Query the diagnosis history for the current user, ordered by date
    diagnoses_query = Diagnosis.query.filter_by(user_id=current_user.id).order_by(Diagnosis.diagnosis_date.desc())
    diagnoses = diagnoses_query.paginate(page=page, per_page=per_page, error_out=False)
    # Pass the paginated results to the template
    return render_template('history.html', diagnoses=diagnoses)


@main.route("/view_diagnosis/<int:diagnosis_id>")
@login_required
def view_diagnosis(diagnosis_id):
    diagnosis = Diagnosis.query.get_or_404(diagnosis_id)
    
    # Ensure the diagnosis belongs to the current user
    if diagnosis.user_id != current_user.id:
        return redirect(url_for('main.history'))
    
    return render_template('view_diagnosis.html', diagnosis=diagnosis)


@main.route("/upload", methods=['GET', 'POST'])
@login_required
def upload_image():
    form = UploadForm()
    if form.validate_on_submit():
        if form.image.data:
            image_file = secure_filename(form.image.data.filename)
            image_path = os.path.join(current_app.root_path, 'static/uploads', image_file)
            form.image.data.save(image_path)

            # Perform the first classification
            diagnosis_result, confidence_score = classify_health(image_path)

            if diagnosis_result == 'Healthy':
                diagnosis_results = {
                    'diagnosis': 'Healthy',
                    'image_file': image_file
                }
                disease_info_id = None
                disease_confidence_score = 0.0
                disease_name = " "
            else:
                # Perform the second classification if diseased
                disease_name, disease_confidence_score = classify_disease(image_path)

                # Fetch details of the disease from the database
                disease_info = DiseaseInfo.query.filter_by(name=disease_name).first()
                
                if disease_info:
                    diagnosis_results = {
                        'diagnosis': 'Diseased',
                        'disease_name': disease_info.name,
                        'description': disease_info.description,
                        'causes': disease_info.causes,
                        'solutions': disease_info.recommendation_text,
                        'recommendations': disease_info.recommendation_text,
                        'image_file': image_file
                    }
                    disease_info_id = disease_info.id
                else:
                    diagnosis_results = {
                        'diagnosis': 'Diseased',
                        'disease_name': disease_name,
                        'description': 'Details not found',
                        'causes': 'Details not found',
                        'solutions': 'Details not found',
                        'recommendations': 'Details not found',
                        'image_file': image_file
                    }
                    disease_info_id = None

            # Save the image entry to the database
            new_image = DBImage(user_id=current_user.id, image_path=image_path)
            db.session.add(new_image)
            db.session.commit()

            # Save the diagnosis to the database
            diagnosis_entry = Diagnosis(
                image_id=new_image.id,  # Use the ID of the saved image
                disease_info_id=disease_info_id,
                diagnosis=diagnosis_results['diagnosis'],
                confidence_score=disease_confidence_score if diagnosis_results['diagnosis'] == 'Diseased' else confidence_score,
                user_id=current_user.id
            )
            db.session.add(diagnosis_entry)
            db.session.commit()
            
            diagnosis_results['diagnosis_id'] = diagnosis_entry.id
            
            return redirect(url_for('main.results', **diagnosis_results))
    return render_template('uploads.html', title='Upload Image', form=form)



@main.route("/results")
def results():
    diagnosis = request.args.get('diagnosis')
    image_file = request.args.get('image_file')
    diagnosis_id = request.args.get('diagnosis_id')

    if diagnosis == 'Diseased':
        disease_name = request.args.get('disease_name')
        description = request.args.get('description')
        causes = request.args.get('causes')
        solutions = request.args.get('solutions')
        recommendations = request.args.get('recommendations')
        return render_template('results.html', diagnosis=diagnosis, disease_name=disease_name, 
                               description=description, causes=causes, solutions=solutions, 
                               recommendations=recommendations, image_file=image_file,
                               diagnosis_id=diagnosis_id)
    return render_template('results.html', diagnosis=diagnosis, image_file=image_file,
                           diagnosis_id=diagnosis_id)


@main.route('/submit_feedback/<int:diagnosis_id>', methods=['POST'])
def submit_feedback(diagnosis_id):
    accuracy_feedback = request.form.get('accuracy_feedback')
    recommendation_feedback = request.form.get('recommendation_feedback')
    
    feedback = Feedback(
        diagnosis_id=diagnosis_id,
        accuracy_feedback=accuracy_feedback,
        recommendation_feedback=recommendation_feedback
    )
    
    db.session.add(feedback)
    db.session.commit()
    
    flash('Thank you for your feedback!', 'success')
    return redirect(url_for('main.results', diagnosis_id=diagnosis_id))