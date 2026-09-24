from sklearn.metrics import accuracy_score,f1_score,precision_score,recall_score
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pandas as pd 
from sklearn.datasets import make_classification


import mlflow
import mlflow.sklearn

mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("fraud_detection")


X,y=make_classification(n_samples=1000,n_informative=2,n_redundant=4,n_features=20,random_state=42)



X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42,stratify=y)



mlflow.set_experiment("fraud_detection")

with mlflow.start_run():
    n_estimators=200
    max_depth=10
    min_samples_split=4


    model=RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        random_state=42
    )

    model.fit(X_train,y_train)

    predictions=model.predict(X_test)

    
    acc=accuracy_score(y_test,predictions)
    prec=precision_score(y_test,predictions)
    f1=f1_score(y_test,predictions)
    recall=recall_score(y_test,predictions)


    mlflow.log_params({
        "n_estimators":n_estimators,
        "max_depth":max_depth,
        "min_samples_split":min_samples_split
    })

    mlflow.log_metrics({
        "accuracy":acc,
        "precision":prec,
        "f1":f1,
        "recall":recall
    })


    mlflow.sklearn.log_model(model,name="fraud_detection",skops_trusted_types=["sklearn.tree._tree.Tree"])

    print(f"Accuracy Score: {acc}")
    print(f"Precision Score: {prec}")
    print(f"f1 Score: {f1}")
    print(f"Recall Score: {recall}")