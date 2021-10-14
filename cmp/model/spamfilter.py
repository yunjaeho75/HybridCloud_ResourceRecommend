import io
from keras.models import Sequential
from keras.models import Model
from keras.layers import Input, Dense, LSTM, Bidirectional, Activation, Dropout, Reshape, Lambda
from tensorflow.keras import activations
import tensorflow as tf
from . import metahelper
from ..core import util

OUT_STEP = 60

tf.get_logger().setLevel('INFO')

def get_model_summary(model):
    stream = io.StringIO()
    model.summary(print_fn=lambda x: stream.write(x + '\n'))
    summary_string = stream.getvalue()
    stream.close()
    return summary_string

class helper(metahelper.AbstractHelper):
    
    def names(self, name) -> str:
        return "spamfilter"
            
    def create(self, param):
        self.in_step = param.in_step
        self.out_step = param.out_step
        self.in_feature = param.in_feature
        self.out_feature = param.out_feature
        self.model = Sequential()
        return self.model

    def summary(self):
        return self.model.summary()
        
    def summary_str(self):
        return get_model_summary(self.model)

    def get_model(self):
        return self.model

    def load(self, path):        
        self.model = tf.keras.models.load_model(path)
        return self.model

    def save(self, path):
        self.model.save(path)
        
    def evaluate(self, data):
        result = self.model.evaluate(data)
        return dict(zip(self.model.metrics_names, result))
    
    def predict(self, data):
        inputs, labels = next(iter(data))
        ret = dict()
        ret['label'] = 'None'
        #ret['predict'] = self.model.predict(inputs).flatten().tolist()
        ret['predict'] = self.model.predict(inputs)
        return ret



class model_v1(helper):    
    def create(self, param):
        model = super().create(param)
        model = Sequential()
        model.add(Bidirectional(LSTM(512, return_sequences=True, activation="tanh"),
                                input_shape=(self.in_step, self.in_feature)))
        model.add(Dropout(0.3))
        model.add(Bidirectional(LSTM(512, activation="tanh")))
        model.add(Dropout(0.3))
        model.add(Dense(1))
        self.model = model
        return self.model


class model_v2(helper):    
    def create(self, param):
        model = super().create(param)
        model.add(
            Bidirectional(
                LSTM(512, return_sequences=True, activation="tanh"),
                input_shape=(self.in_step, self.in_feature)
            )
        )
        model.add(Dropout(0.3))
        model.add(Lambda(lambda x: x[:, -self.out_step:, :]))
        model.add(Dropout(0.3))
        model.add(Bidirectional(LSTM(512, return_sequences=True, activation="tanh")))
        model.add(Dropout(0.3))
        #model.add(Dense(units=OUT_STEP, activation=activations.linear))
        model.add(Dense(units=1, activation=activations.linear))
        #model.add(Reshape((OUT_STEP, 1), input_shape=(OUT_STEP,OUT_STEP)))
        self.model = model
        return self.model