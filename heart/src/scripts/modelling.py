from heart.src.scripts.processing import tts
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, f1_score, cohen_kappa_score, hamming_loss, classification_report
import pickle

def xgb_model():
  X_train, X_test, y_train, y_test = tts()
  xgb = XGBClassifier(use_label_encoder=False, eval_metric='mlogloss').fit(X_train, y_train)
  y_pred = xgb_pred(xgb, X_test)
  save_model_log(y_test, y_pred)
  save_model(xgb)

def xgb_pred(model, x_test):
  y_pred = model.predict(x_test)
  return y_pred

def save_model_log(y_test, y_pred):
  with open('../rest_api_proj/heart/log/Model_out_log.txt', 'w') as f:
    write_log(f, y_test, y_pred)
    f.close()

def save_model(model):
    with open('../rest_api_proj/heart/data/model/model.pkl', 'wb') as files:
      pickle.dump(model, files)

def write_log(f, y_test, y_pred):
  f.write("Model : XGBoost Classifier\n")
  f.write("Accuracy score : {:.4f}\n".format(accuracy_score(y_test, y_pred)))
  f.write("Cohen's kappa score : {:.4f}\n".format(cohen_kappa_score(y_test, y_pred)))
  f.write("Hamming Loss : {:.4f}\n".format(hamming_loss(y_test, y_pred)))
  f.write("F1 score : {:.4f}\n".format(f1_score(y_test, y_pred)))
  f.write("Report : \n")
  f.write(classification_report(y_test, y_pred))
