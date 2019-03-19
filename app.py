from flask import Flask, request, render_template, redirect, session, Session, send_file
from flask_pymongo import PyMongo
import numpy as np
import pandas as pd

# Machine learning stuff

l1=['back_pain','constipation','abdominal_pain','diarrhoea','mild_fever','yellow_urine',
'yellowing_of_eyes','acute_liver_failure','fluid_overload','swelling_of_stomach',
'swelled_lymph_nodes','malaise','blurred_and_distorted_vision','phlegm','throat_irritation',
'redness_of_eyes','sinus_pressure','runny_nose','congestion','chest_pain','weakness_in_limbs',
'fast_heart_rate','pain_during_bowel_movements','pain_in_anal_region','bloody_stool',
'irritation_in_anus','neck_pain','dizziness','cramps','bruising','obesity','swollen_legs',
'swollen_blood_vessels','puffy_face_and_eyes','enlarged_thyroid','brittle_nails',
'swollen_extremeties','excessive_hunger','extra_marital_contacts','drying_and_tingling_lips',
'slurred_speech','knee_pain','hip_joint_pain','muscle_weakness','stiff_neck','swelling_joints',
'movement_stiffness','spinning_movements','loss_of_balance','unsteadiness',
'weakness_of_one_body_side','loss_of_smell','bladder_discomfort','foul_smell_of urine',
'continuous_feel_of_urine','passage_of_gases','internal_itching','toxic_look_(typhos)',
'depression','irritability','muscle_pain','altered_sensorium','red_spots_over_body','belly_pain',
'abnormal_menstruation','dischromic _patches','watering_from_eyes','increased_appetite','polyuria','family_history','mucoid_sputum',
'rusty_sputum','lack_of_concentration','visual_disturbances','receiving_blood_transfusion',
'receiving_unsterile_injections','coma','stomach_bleeding','distention_of_abdomen',
'history_of_alcohol_consumption','fluid_overload','blood_in_sputum','prominent_veins_on_calf',
'palpitations','painful_walking','pus_filled_pimples','blackheads','scurring','skin_peeling',
'silver_like_dusting','small_dents_in_nails','inflammatory_nails','blister','red_sore_around_nose',
'yellow_crust_ooze']

disease=['Fungal infection','Allergy','GERD','Chronic cholestasis','Drug Reaction',
'Peptic ulcer diseae','AIDS','Diabetes','Gastroenteritis','Bronchial Asthma','Hypertension',
' Migraine','Cervical spondylosis',
'Paralysis (brain hemorrhage)','Jaundice','Malaria','Chicken pox','Dengue','Typhoid','hepatitis A',
'Hepatitis B','Hepatitis C','Hepatitis D','Hepatitis E','Alcoholic hepatitis','Tuberculosis',
'Common Cold','Pneumonia','Dimorphic hemmorhoids(piles)',
'Heartattack','Varicoseveins','Hypothyroidism','Hyperthyroidism','Hypoglycemia','Osteoarthristis',
'Arthritis','(vertigo) Paroymsal  Positional Vertigo','Acne','Urinary tract infection','Psoriasis',
'Impetigo']

l2=[]
for x in range(0,len(l1)):
    l2.append(0)

# TESTING DATA df -------------------------------------------------------------------------------------
df=pd.read_csv("Training.csv")

df.replace({'prognosis':{'Fungal infection':0,'Allergy':1,'GERD':2,'Chronic cholestasis':3,'Drug Reaction':4,
'Peptic ulcer diseae':5,'AIDS':6,'Diabetes ':7,'Gastroenteritis':8,'Bronchial Asthma':9,'Hypertension ':10,
'Migraine':11,'Cervical spondylosis':12,
'Paralysis (brain hemorrhage)':13,'Jaundice':14,'Malaria':15,'Chicken pox':16,'Dengue':17,'Typhoid':18,'hepatitis A':19,
'Hepatitis B':20,'Hepatitis C':21,'Hepatitis D':22,'Hepatitis E':23,'Alcoholic hepatitis':24,'Tuberculosis':25,
'Common Cold':26,'Pneumonia':27,'Dimorphic hemmorhoids(piles)':28,'Heart attack':29,'Varicose veins':30,'Hypothyroidism':31,
'Hyperthyroidism':32,'Hypoglycemia':33,'Osteoarthristis':34,'Arthritis':35,
'(vertigo) Paroymsal  Positional Vertigo':36,'Acne':37,'Urinary tract infection':38,'Psoriasis':39,
'Impetigo':40}},inplace=True)

# print(df.head())

X= df[l1]

y = df[["prognosis"]]
np.ravel(y)
# print(y)

# TRAINING DATA tr --------------------------------------------------------------------------------
tr=pd.read_csv("Testing.csv")
tr.replace({'prognosis':{'Fungal infection':0,'Allergy':1,'GERD':2,'Chronic cholestasis':3,'Drug Reaction':4,
'Peptic ulcer diseae':5,'AIDS':6,'Diabetes ':7,'Gastroenteritis':8,'Bronchial Asthma':9,'Hypertension ':10,
'Migraine':11,'Cervical spondylosis':12,
'Paralysis (brain hemorrhage)':13,'Jaundice':14,'Malaria':15,'Chicken pox':16,'Dengue':17,'Typhoid':18,'hepatitis A':19,
'Hepatitis B':20,'Hepatitis C':21,'Hepatitis D':22,'Hepatitis E':23,'Alcoholic hepatitis':24,'Tuberculosis':25,
'Common Cold':26,'Pneumonia':27,'Dimorphic hemmorhoids(piles)':28,'Heart attack':29,'Varicose veins':30,'Hypothyroidism':31,
'Hyperthyroidism':32,'Hypoglycemia':33,'Osteoarthristis':34,'Arthritis':35,
'(vertigo) Paroymsal  Positional Vertigo':36,'Acne':37,'Urinary tract infection':38,'Psoriasis':39,
'Impetigo':40}},inplace=True)

X_test= tr[l1]
y_test = tr[["prognosis"]]
np.ravel(y_test)
# ------------------------------------------------------------------------------------------------------


class Diagnosis:
    def __init__(self):
        self.disease = None
        self.accuracy = 0


def decision_tree(symptoms):

    diagnosis = Diagnosis()

    from sklearn import tree

    clf3 = tree.DecisionTreeClassifier()   # empty model of the decision tree
    clf3 = clf3.fit(X, y)

    # calculating accuracy-------------------------------------------------------------------
    from sklearn.metrics import accuracy_score
    y_pred = clf3.predict(X_test)
    print(accuracy_score(y_test, y_pred))
    print(accuracy_score(y_test, y_pred, normalize=False))
    # -----------------------------------------------------

    p_symptoms = [symptoms[0], symptoms[1], symptoms[2], symptoms[3], symptoms[4]]

    for k in range(0,len(l1)):
        # print (k,)
        for z in p_symptoms:
            if z == l1[k]:
                l2[k] = 1

    input_test = [l2]
    predict = clf3.predict(input_test)
    predicted = predict[0]

    h = 'no'
    for a in range(0, len(disease)):
        if predicted == a:
            h = 'yes'
            break

    if h == 'yes':
        diagnosis.disease = disease[a]
        # t1.delete("1.0", END)
        # t1.insert(END, disease[a])
    else:
        diagnosis.disease = 'Not Found'
        # t1.delete("1.0", END)
        # t1.insert(END, "Not Found")

    return diagnosis


def random_forest(symptoms):

    diagnosis = Diagnosis()

    from sklearn.ensemble import RandomForestClassifier
    clf4 = RandomForestClassifier()
    clf4 = clf4.fit(X, np.ravel(y))

    # calculating accuracy-------------------------------------------------------------------
    from sklearn.metrics import accuracy_score
    y_pred = clf4.predict(X_test)
    print(accuracy_score(y_test, y_pred))
    print(accuracy_score(y_test, y_pred, normalize=False))
    # -----------------------------------------------------

    p_symptoms = [symptoms[0], symptoms[1], symptoms[2], symptoms[3], symptoms[4]]

    for k in range(0,len(l1)):
        for z in p_symptoms:
            if z == l1[k]:
                l2[k]=1

    input_test = [l2]
    predict = clf4.predict(input_test)
    predicted = predict[0]

    h = 'no'
    for a in range(0, len(disease)):
        if predicted == a:
            h = 'yes'
            break

    if h == 'yes':
        diagnosis.disease = disease[a]
        # t2.delete("1.0", END)
        # t2.insert(END, disease[a])
    else:
        diagnosis.disease = 'Not Found'
        # t2.delete("1.0", END)
        # t2.insert(END, "Not Found")

    return diagnosis


def naive_bayes(symptoms):

    diagnosis = Diagnosis()

    from sklearn.naive_bayes import GaussianNB
    gnb = GaussianNB()
    gnb = gnb.fit(X, np.ravel(y))

    # calculating accuracy-------------------------------------------------------------------
    from sklearn.metrics import accuracy_score
    y_pred=gnb.predict(X_test)
    print(accuracy_score(y_test, y_pred))
    print(accuracy_score(y_test, y_pred, normalize=False))
    # -----------------------------------------------------

    p_symptoms = [symptoms[0], symptoms[1], symptoms[2], symptoms[3], symptoms[4]]
    for k in range(0,len(l1)):
        for z in p_symptoms:
            if z == l1[k]:
                l2[k] = 1

    input_test = [l2]
    predict = gnb.predict(input_test)
    predicted = predict[0]

    h = 'no'
    for a in range(0, len(disease)):
        if predicted == a:
            h = 'yes'
            break

    if h == 'yes':
        diagnosis.disease = disease[a]
        # t3.delete("1.0", END)
        # t3.insert(END, disease[a])
    else:
        diagnosis.disease = 'Not Found'
        # t3.delete("1.0", END)
        # t3.insert(END, "Not Found")

    return diagnosis

# Machine learning stuff ends

# Flask stuff


app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super_secret_key'
session = Session()
app.config["MONGO_URI"] = "mongodb://localhost:27017/KbDPES"

mongo = PyMongo(app)


@app.route('/', methods=["GET", "POST"])
def hello_world():
    if 'username' in session:
        return redirect('/details')
    else:
        return render_template('index.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    username = request.form['username']
    password = request.form['password']
    users = mongo.db.users
    existing_user = users.find_one({'username': username})

    if existing_user is None:
        session['temp_username'] = username
        session['temp_password'] = password
        return render_template('register.html', username=username, password=password)
    else:
        if password == existing_user['password']:
            session['username'] = username
            return redirect('/details')
        else:
            return redirect('/error')


@app.route('/registered', methods=["POST"])
def registered():
    users = mongo.db.users
    username = session['temp_username']
    password = session['temp_password']
    first_name = request.form['fname']
    last_name = request.form['lname']
    age = request.form['age']
    gender = request.form['gender']
    users.insert({'username': username, 'password': password, 'fname': first_name, 'lname': last_name,
              'age': age, 'gender': gender})
    session.pop('temp_username', None)
    session.pop('temp_password', None)
    session['username'] = username
    return redirect('/details')


@app.route('/details')
def details():
    session_username = session['username']
    user = mongo.db.users
    username = user.find_one({'username': session_username})
    first_name = username['fname']
    last_name = username['lname']
    name = first_name + " " + last_name
    gender = username['gender']
    age = username['age']
    symptoms = sorted(l1)
    return render_template('details.html', username=session_username, name=name, gender=gender, age=age,
                           symptoms=symptoms, len=len(symptoms))


@app.route('/predict', methods=["GET", "POST"])
def predict():
    symptoms = [None] * 5
    symptoms[0] = request.form['symptom_1']
    symptoms[1] = request.form['symptom_2']
    symptoms[2] = request.form['symptom_3']
    symptoms[3] = request.form['symptom_4']
    symptoms[4] = request.form['symptom_5']
    for i in range(0, 5):
        if symptoms[i] == 'None':
            symptoms[i] = None

    # To try:
    # symptoms = request.form['symptoms']

    algorithm = request.form['submit']

    disease = None
    if algorithm == 'Decision Tree':
        diagnosis = decision_tree(symptoms)
    elif algorithm == 'Random Forest':
        diagnosis = random_forest(symptoms)
    elif algorithm == 'Naive Bayes':
        diagnosis = naive_bayes(symptoms)
    result = diagnosis.disease
    return render_template('status.html', result=result)


@app.route('/error')
def error():
    return render_template('index.html', error_message="Please check the credentials")


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')


@app.route('/delete_<username>')
def delete_user(username):
    user = mongo.db.users
    username = user.find_one({'username': username})
    user.remove(username)
    return 'Removed'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)