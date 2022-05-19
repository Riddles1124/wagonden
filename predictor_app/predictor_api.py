import pickle as pkl
from keras.processing.image import load_img
from tensorflow.keras.models import Sequential


with open("./models/model.pkl","rb") as m:
    model = pkl.load(m)

feature_name=model.target_names

def make_prediction(x_input):
    image = load_img(x_input,
            grayscale=False,
            target_size=(200,200,3),
            interpolation='nearest'
            )
    predictions = model.predict(image)
    return prediction







