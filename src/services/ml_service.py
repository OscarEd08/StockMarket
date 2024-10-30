import numpy as np
from sklearn.svm import SVC
from keras.api.models import load_model

class MLService:
    def __init__(self):
        self.svm_model = SVC()  # Cargar modelo entrenado si es necesario
        self.lstm_model = load_model("models/lstm_model.h5")  # LSTM ya entrenado

    def predict_with_svm(self, data):
        """Genera predicción con SVM usando datos estructurados."""
        input_data = np.array(data).reshape(1, -1)
        return self.svm_model.predict(input_data)

    def predict_with_lstm(self, sequence):
        """Genera predicción de series temporales con LSTM."""
        input_sequence = np.array(sequence).reshape(1, len(sequence), 1)
        return self.lstm_model.predict(input_sequence)
