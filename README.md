# SMSSpamWebAPI
A web API written in python to detect whether an sms is a spam or a ham based on machine learning. This API provides three functionalities: *detect spams*, *list stored messages* and *vote whether an sms is spam or ham*. The third option gives an added functionality to the admin to retrain the machine by adding the newly obtained datasets. The spam classifier works with 98% accuracy.

## Dependencies:
### Machine learning
* Numpy
* Scipy
* Pandas
* Scikit Learn
* Natural Language Toolkit

### Web server and database
* Flask
* Flask CORS
* RethinkDB

### Database used:
* Rethinkdb

## Guide
### The web API provides three URLs:

* `http://host:port/sms` allows HTTP Post JSON object of the format: ```{"message": ["a", "b", ... ,"n"]}``` with _application/json_ Content-Type. The response is a JSON object of the format: ```{"result": ["spam", "ham", ..., "spam"]}``` for each message in the request JSON.

* `http://host:port/messages` allows HTTP Get request which responds with the list of messages in a JSON object. The JSON object is an array containing lists of objects each of the format: 
```
[{
  "id": "7e3db8ee-c8e0-478e-be87-99a1ecbf9028",
  "message": "Call me as soon as you get this message!",
  "predicted": "ham",
  "ham": 42,
  "spam": 3
}]
``` 
Where, _id_ is the ID of the message, _message_ holds the message, _predicted_ is the predicted class of the message by the classifiera and, _ham_ and _spam_ are the number of votes made by users that the message is a ham and spam respectively.

* `http://host:port/classify/<id>/<label>` allows HTTP Get where `<id>` holds the ID of the message and `<label>` holds the class (spam or ham) the message has been voted with. The response is a JSON object of the format: `{"success": true}` where the boolean value defines whether the vote has been successfully stored in the database or not.

### How to setup:
The project contains a _config.json_ file that can be edited to change the following settings:
* web
  * hostname
  * port number
* database
  * database name
  * username
  * password
  * tables[]

#### Steps
1. Run the Rethinkdb server. Download from [here](https://www.rethinkdb.com/docs/install/).
1. Execute _setup_db.py_ to set up the database.
1. Execute _createModel.py_ to create the TfidfVectorizer and the MultinomialNB objects for spam classification.
1. Execute _app.py_ to start the server.

### How it works:
Available at [SudoCoding](http://sudocoding.xyz/sms-spam-detection-using-machine-learning/).

### References and datasets:
Dataset Link: https://www.kaggle.com/uciml/sms-spam-collection-dataset<br/>
Classifier Notebook Guide: https://www.kaggle.com/muzzzdy/sms-spam-detection-with-various-classifiers
