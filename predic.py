
from keras.models import load_model
import numpy as np 
from keras import backend as K
import tensorflow as tf


def f1_m(y_true, y_pred):
    precision = precision_m(y_true, y_pred)
    recall = recall_m(y_true, y_pred)
    return 2*((precision*recall)/(precision+recall+K.epsilon()))

def precision_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision

def recall_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall

model  = tf.keras.models.load_model('model.h5'
                                ,custom_objects={
                                    'f1_m': f1_m,
                                    'precision_m': precision_m,
                                    'recall_m': recall_m}
                                )

def predict(ids):
                    # Pad input_ids to shape (None, 768)
    padded_input_ids = np.pad(ids, ((0,0),(0,256)), mode='constant')

                    # Predict using the padded input_ids
    prediction = model.predict(padded_input_ids)

                    # Get the predicted class
    predicted_class = np.argmax(prediction)

                    # Map the predicted class to its label
    risk_labels = {0: "Low Risk", 1: "Medium Risk", 2: "High Risk"}
    return risk_labels[predicted_class]
                