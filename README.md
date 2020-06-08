# Flask_Dashboard
Flask Dashboard for Health Monitoring Project

The project graphs the realtime sensor data collected from the DS18b20 temp sensor and the pulse sensor in the Monitoring tab. The sensory data is collected and visualized via the ThingSpeak Api Platform. For the hardware requirements, data from DS18b20 and pulse sensor are sent via the NodeMCU Wifi Module. The codes for the NodeMCU programming are in the Sensors file.

Database Used - SQLLite (used SQLAlchemy ORM - Object Relational Mapper ) for user authentication and fetching doctor details in the dashboard.

Use "/register" for Registeration and "/login" routes for Login. "/doctor" route for the Doctor Form whose results are displayed on Dashboard. Also the Prescription page suggests a drug name based on the vital parameters (body temp,pulse rate,respiratory rate,sao2 rate,systolic and diastolic blood pressure) on the basis of drug predictions made by a machine learning model trained on a custom dataset "vital_med.csv". ( P.s. the dataset is a custom dataset and has been used only for learning purpose. The drug predictions are not to be implemented).

The emergency page lists out the nearby hospitals in the city along with the details. The data is retrieved from the Here Api (pip install herepy) and the location for the query string is set dynamic according to the current location where the project is ran.

To run the project, clone the repository and create a virtualenv.

In project folder , type in cmd - virtualenv . cd Scripts > activate cd.. python app.py Make sure to install all the libraries and dependencies. Make sure that the version of the libraries are the same eg. scikit-learn version should be same in virtual environment as well as your PC.

[Project Demo](https://drive.google.com/file/d/1IgJRfAWQI5n-0PTsPWqMO0AMa72ScZCD/view?usp=sharing "Project Demo")
