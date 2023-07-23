import tensorflow_addons as tfa
from keras.models import load_model

import cv2, numpy as np

tfa.register_all(custom_kernels=False)

def reSize(file):
    img = cv2.imdecode(np.fromstring(file.read(), np.uint8), 1)
    img = cv2.resize(img, (128, 128))
    return img


def predict(img, myModel):
    
    model_paths = {
        "Model 1": ["CNN_dataset1.h5",reSize],
        "Model 2": ["TL_Dataset1.h5",reSize],
        "Model 3": ["CNN_dataset2.h5",reSize],
        "Model 4": ["TL_Dataset2.h5", reSize]
    }
    my = model_paths[myModel]
    function = my[1]
    img = function(img)
    model = load_model(my[0])
    print(model)
    hmm = model.predict(np.expand_dims(img / 255, axis = 0))
    print(hmm)
    hmm = list(hmm[0])
    
    lis = ["Mild_Demented", "Moderate_Demented", "Non_Demented", "Very_Mild_Demented"]
    return hmm