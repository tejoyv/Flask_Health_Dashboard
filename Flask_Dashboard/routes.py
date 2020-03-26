from Flask_Dashboard import app,db,bcrypt
from flask import Flask,render_template,url_for,flash,redirect,request
from Flask_Dashboard.models import User,Doctor
from Flask_Dashboard.forms import RegisterationForm,LoginForm,DoctorForm
from flask_login import login_user,current_user,logout_user,login_required
from sklearn.externals import joblib
import secrets
import pandas as pd
import numpy as np

mul_class = open('model.pkl',"rb")
ml_model = joblib.load(mul_class)

@app.route('/')
def index():
    doctor=Doctor.query.all()
    return render_template('index.html',doctor=doctor)

@app.route('/prescription')
def prescription():
    return render_template('drug_prescription.html')

@app.route('/live_monitor')
def live_monitor():
    return render_template('live_monitor.html')


@app.route("/predict",methods=['GET','POST'])
def predict():
    # Importing the dataset
    df = pd.read_csv('vital_med.csv')
    df.drop(['Unnamed: 8','Unnamed: 9','Unnamed: 10'],axis=1,inplace=True)
    X=df.iloc[:,:-1].values
    Y=df.iloc[:,7].values
    df

    # Describing the dataset
    df.isnull().sum()
    df.shape
    df.describe()

    # Create a set of dummy variables from the drugname variable
    df = pd.get_dummies(df, columns=['drugname'])

    # Splitting the dataset into the Training set and Test set
    from sklearn.model_selection import train_test_split
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.25, random_state = 0)

    # Feature Scaling
    from sklearn.preprocessing import StandardScaler
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)


    # Fitting the Decision Tree to the training set
    from sklearn.tree import DecisionTreeClassifier
    classifier=DecisionTreeClassifier(criterion='entropy',random_state=0)
    classifier.fit(X_train,Y_train)

    # Predicting the Test set results
    y_pred = classifier.predict(X_test)

    # Making the Confusion Matrix
    from sklearn.metrics import confusion_matrix
    from sklearn.metrics import accuracy_score
    cm = confusion_matrix(Y_test, y_pred)
    accuracy_score(Y_test, y_pred)
    
    if request.method == "POST":
            Child_ID = request.form['Child_ID']
            Body_Temperature = float(request.form['Body_Temperature'])
            SaO2_Rate = float(request.form['SaO2_Rate'])
            Pulse_Rate = float(request.form['Pulse_Rate'])
            Respiration_Rate = float(request.form['Respiration_Rate'])
            Systolic_Blood_Pressure = float(request.form['Systolic_Blood_Pressure'])
            Diastolic_Blood_Pressure=float(request.form['Diastolic_Blood_Pressure'])
            pred_args = [Child_ID,Body_Temperature,SaO2_Rate,Pulse_Rate,Respiration_Rate,Systolic_Blood_Pressure,Diastolic_Blood_Pressure]
            pred_args_arr = np.array(pred_args)
            pred_args_arr = pred_args_arr.reshape(1,-1)
            
            model_prediction=classifier.predict(pred_args_arr)
    return render_template("predict.html",prediction=model_prediction)


@app.route('/emergency')
def emergency():
    #import herepy
    import json
    import requests

    #placesApi = herepy.PlacesApi('HYeyw8jHy0KxEuySBUjmaPNOfJs9ImQktb3_9XA6Eyg')
    #response = placesApi.onebox_search([22.304106,73.1561776], 'hospital')

    res=requests.get('https://ipinfo.io/')
    data=res.json()
    location=data['loc'].split(',')

    lati=location[0]
    longi=location[1]


    import requests
    response = requests.get('https://places.sit.ls.hereapi.com/places/v1/autosuggest?at='+lati+','+longi+'&q=hospital&apiKey=HYeyw8jHy0KxEuySBUjmaPNOfJs9ImQktb3_9XA6Eyg')


    json_data = response.json()
    
    results=json_data['results']
    #results=results.pop()
    lst=[]
    #pl=[]
    view1=[]
    for i in range(2,len(results)-2):
        title=results[i]['title']
        pla=results[i]['id']
    
        lst.append(title)
        
        #pl.append(pla)
        response1=requests.get('https://places.sit.ls.hereapi.com/places/v1/places/'+pla+';context=Zmxvdy1pZD03NmU3ZGM3OC1kNjk0LTU5ZTgtOTk3MS1mYjUxN2I1M2YyMTdfMTU4MzIxNTkxMjIxMF85MzU5Xzc2JnJhbms9MQ?app_id=vteXuQuLoQCZpY7asnWm&app_code=PSYtOzMtpewSp9FKymXKrw')
        json_data1=response1.json()
        view1.append(json_data1['view'])

    
    sno=[]
    for i in range(1,len(lst)):
        sno.append(i)
    
    obj = zip(sno, lst,view1)
    #print(view1)
    return render_template('emergency.html',res=obj)

@app.route("/register",methods=['POST','GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created ! You are now able to log in !','success')
        return redirect(url_for('login'))
    return render_template('register.html',title="Register",form=form)

@app.route("/login",methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page=request.args.get('next')        # next parameter query args gets
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful.Please check email and password','danger')
    return render_template('login.html',title="Login",form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect (url_for('login'))

@app.route('/doctor',methods=['POST','GET'])
@login_required
def doctor():
    form=DoctorForm()
    if form.validate_on_submit():
        doctor = Doctor(doctor=form.doctor.data,drugName=form.drug_Name.data,status=form.status.data,dosage=form.dosage.data,frequency=form.frequency.data)
        db.session.add(doctor)
        db.session.commit()
        flash('Doctor Details added to homepage','success')
        return redirect(url_for('index'))
    return render_template('doctor_form.html',form=form)