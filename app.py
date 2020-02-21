from flask import Flask,render_template,request
from sklearn.externals import joblib
import pandas as pd
import numpy as np

app=Flask(__name__)

mul_class = open('model.pkl',"rb")
ml_model = joblib.load(mul_class)

@app.route('/')
def index():
    return render_template('index.html')

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


if __name__=="__main__":
    app.run()

