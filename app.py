<<<<<<< HEAD
import os
import certifi
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId

app = Flask(__name__)

# --- Configuration ---
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# --- MongoDB Connection ---
uri = "mongodb+srv://mythili1302cs_db_user:lewYTpcn8HBuxCj1@cluster0.u5e7qem.mongodb.net/?appName=Cluster0"

try:
    client = MongoClient(uri, tls=True, tlsAllowInvalidCertificates=True, tlsCAFile=certifi.where())
    db = client['my_website_db']
    collection = db['users']
    print("✅ Database Connected Successfully!")
except Exception as e:
    print(f"❌ MongoDB Connection Error: {e}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', '').strip()
    gender_filter = request.args.get('gender_filter', '').strip()
    per_page = 10
    offset = (page - 1) * per_page

    query = {}
    if search_query:
        query["$or"] = [
            {"age": {"$regex": search_query, "$options": "i"}},
            {"body_type": {"$regex": search_query, "$options": "i"}}
        ]
    
    if gender_filter:
        query["gender"] = gender_filter

    total_users = collection.count_documents(query)
    users = list(collection.find(query).skip(offset).limit(per_page))
    total_pages = (total_users + per_page - 1) // per_page if total_users > 0 else 1

    return render_template('dashboard.html', 
                           users=users, 
                           page=page, 
                           total_pages=total_pages, 
                           search_query=search_query,
                           gender_filter=gender_filter)

@app.route('/edit/<user_id>')
def edit_profile(user_id):
    search_query = request.args.get('search', '')
    gender_filter = request.args.get('gender_filter', '')
    page = request.args.get('page', 1)
    
    user = collection.find_one({"_id": ObjectId(user_id)})
    return render_template('edit.html', user=user, search_query=search_query, gender_filter=gender_filter, page=page)

@app.route('/update_profile/<user_id>', methods=['POST'])
def update_profile(user_id):
    try:
        current_page = request.form.get('page', 1)
        search_query = request.form.get('search', '')
        gender_filter = request.form.get('gender_filter', '')
        
        updated_data = {
            "gender": request.form.get('gender'),
            "age": request.form.get('age'),
            "body_type": request.form.get('body_type'),
            "image_filename": request.form.get('image_url')
        }
        
        collection.update_one({"_id": ObjectId(user_id)}, {"$set": updated_data})
        
        return redirect(url_for('dashboard', page=current_page, search=search_query, gender_filter=gender_filter))
    except Exception as e:
        return f"Update failed: {e}"

@app.route('/delete_one/<user_id>', methods=['POST'])
def delete_one(user_id):
    try:
        collection.delete_one({"_id": ObjectId(user_id)})
        return redirect(url_for('dashboard', 
                                page=request.args.get('page', 1), 
                                search=request.args.get('search', ''),
                                gender_filter=request.args.get('gender_filter', '')))
    except Exception as e:
        return f"Error: {e}"

@app.route('/delete_page', methods=['POST'])
def delete_page():
    try:
        user_ids = request.form.getlist('user_ids')
        if user_ids:
            collection.delete_many({"_id": {"$in": [ObjectId(uid) for uid in user_ids]}})
        return redirect(url_for('dashboard'))
    except Exception as e:
        return f"Error: {e}"

@app.route('/delete_all', methods=['POST'])
def delete_all():
    collection.delete_many({})
    return redirect(url_for('dashboard'))

@app.route('/add_new')
def add_new():
    return render_template('form.html')

@app.route('/save_profile', methods=['POST'])
def save_profile():
    try:
        gender = request.form.get('gender')
        age = request.form.get('age')
        body_type = request.form.get('body_type')
        image_file = request.files.get('image')
        image_url = request.form.get('image_url')

        final_image = image_url if image_url else ""
        if image_file and image_file.filename != '':
            filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            final_image = filename

        collection.insert_one({"gender": gender, "age": age, "body_type": body_type, "image_filename": final_image})
        return redirect(url_for('dashboard'))
    except Exception as e:
        return f"Failed: {e}"


@app.route('/view_profiles')
def view_profiles():

    age_query = request.args.get('search', '').strip() 
    gender_filter = request.args.get('gender_filter', '').strip()
    body_type_filter = request.args.get('body_type_filter', '').strip()
    
    query = {}
    
    if age_query:
        query["age"] = age_query
    
    if gender_filter:
        query["gender"] = gender_filter

    if body_type_filter:
        query["body_type"] = body_type_filter

    # டேட்டாபேஸில் இருந்து ஃபில்டர் செய்து எடுக்கிறோம்
    profiles = list(collection.find(query))
    
    # view.html பக்கத்திற்கு அனுப்புகிறோம்
    return render_template('view.html', profiles=profiles)
if __name__ == '__main__':
=======
import os
import certifi
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId

app = Flask(__name__)

# --- Configuration ---
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# --- MongoDB Connection ---
uri = "mongodb+srv://mythili1302cs_db_user:lewYTpcn8HBuxCj1@cluster0.u5e7qem.mongodb.net/?appName=Cluster0"

try:
    client = MongoClient(uri, tls=True, tlsAllowInvalidCertificates=True, tlsCAFile=certifi.where())
    db = client['my_website_db']
    collection = db['users']
    print("✅ Database Connected Successfully!")
except Exception as e:
    print(f"❌ MongoDB Connection Error: {e}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', '').strip()
    gender_filter = request.args.get('gender_filter', '').strip()
    per_page = 10
    offset = (page - 1) * per_page

    query = {}
    if search_query:
        query["$or"] = [
            {"age": {"$regex": search_query, "$options": "i"}},
            {"body_type": {"$regex": search_query, "$options": "i"}}
        ]
    
    if gender_filter:
        query["gender"] = gender_filter

    total_users = collection.count_documents(query)
    users = list(collection.find(query).skip(offset).limit(per_page))
    total_pages = (total_users + per_page - 1) // per_page if total_users > 0 else 1

    return render_template('dashboard.html', 
                           users=users, 
                           page=page, 
                           total_pages=total_pages, 
                           search_query=search_query,
                           gender_filter=gender_filter)

@app.route('/edit/<user_id>')
def edit_profile(user_id):
    search_query = request.args.get('search', '')
    gender_filter = request.args.get('gender_filter', '')
    page = request.args.get('page', 1)
    
    user = collection.find_one({"_id": ObjectId(user_id)})
    return render_template('edit.html', user=user, search_query=search_query, gender_filter=gender_filter, page=page)

@app.route('/update_profile/<user_id>', methods=['POST'])
def update_profile(user_id):
    try:
        current_page = request.form.get('page', 1)
        search_query = request.form.get('search', '')
        gender_filter = request.form.get('gender_filter', '')
        
        updated_data = {
            "gender": request.form.get('gender'),
            "age": request.form.get('age'),
            "body_type": request.form.get('body_type'),
            "image_filename": request.form.get('image_url')
        }
        
        collection.update_one({"_id": ObjectId(user_id)}, {"$set": updated_data})
        
        return redirect(url_for('dashboard', page=current_page, search=search_query, gender_filter=gender_filter))
    except Exception as e:
        return f"Update failed: {e}"

@app.route('/delete_one/<user_id>', methods=['POST'])
def delete_one(user_id):
    try:
        collection.delete_one({"_id": ObjectId(user_id)})
        return redirect(url_for('dashboard', 
                                page=request.args.get('page', 1), 
                                search=request.args.get('search', ''),
                                gender_filter=request.args.get('gender_filter', '')))
    except Exception as e:
        return f"Error: {e}"

@app.route('/delete_page', methods=['POST'])
def delete_page():
    try:
        user_ids = request.form.getlist('user_ids')
        if user_ids:
            collection.delete_many({"_id": {"$in": [ObjectId(uid) for uid in user_ids]}})
        return redirect(url_for('dashboard'))
    except Exception as e:
        return f"Error: {e}"

@app.route('/delete_all', methods=['POST'])
def delete_all():
    collection.delete_many({})
    return redirect(url_for('dashboard'))

@app.route('/add_new')
def add_new():
    return render_template('form.html')

@app.route('/save_profile', methods=['POST'])
def save_profile():
    try:
        gender = request.form.get('gender')
        age = request.form.get('age')
        body_type = request.form.get('body_type')
        image_file = request.files.get('image')
        image_url = request.form.get('image_url')

        final_image = image_url if image_url else ""
        if image_file and image_file.filename != '':
            filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            final_image = filename

        collection.insert_one({"gender": gender, "age": age, "body_type": body_type, "image_filename": final_image})
        return redirect(url_for('dashboard'))
    except Exception as e:
        return f"Failed: {e}"


@app.route('/view_profiles')
def view_profiles():
    # HTML Form-ல் இருந்து வரும் Data-வை எடுக்கிறோம்
    # குறிப்பு: index.html-ல் Age-க்கு 'search' என்ற பெயரை வைத்துள்ளீர்கள்
    age_query = request.args.get('search', '').strip() 
    gender_filter = request.args.get('gender_filter', '').strip()
    body_type_filter = request.args.get('body_type_filter', '').strip()
    
    # MongoDB Query உருவாக்குகிறோம்
    query = {}
    
    if age_query:
        query["age"] = age_query
    
    if gender_filter:
        query["gender"] = gender_filter

    if body_type_filter:
        query["body_type"] = body_type_filter

    # டேட்டாபேஸில் இருந்து ஃபில்டர் செய்து எடுக்கிறோம்
    profiles = list(collection.find(query))
    
    # view.html பக்கத்திற்கு அனுப்புகிறோம்
    return render_template('view.html', profiles=profiles)
if __name__ == '__main__':
>>>>>>> 76baebd5b94eb6e68bf4293202a3392cbed1a86f
    app.run(debug=True, port=5000)