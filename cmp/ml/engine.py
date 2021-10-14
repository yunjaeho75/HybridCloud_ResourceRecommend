import numpy as np
import tensorflow as tf
import os as _os
import json
from .. import core
from ..data import helper as data_helper
from ..model import helper as model_helper
from ..core import options, logger, util



def window_generator_for_learner(ws, source):
    log = logger.get(__name__)

    # 데이터 분할 (학습 70%, 검증 20%, 확인 10%)
    log.info(f'splite train data (train 70%, valid 20%, test 10%)...')
    train, valid, test, features = core.make_splite_dataset(source)
    
    # 학습 데이터 평균과 표준편차 구하기
    mean = train.mean()
    std = train.std()
    ws.mean = mean.to_numpy().flatten()[0]
    ws.std = std.to_numpy().flatten()[0]

    log.info(f'train data nomarization...')
    log.debug(f"(mean: {ws.mean}, std: {ws.std})")

    # 학습 데이터 정규화
    train_df = core.standardization(train, mean, std)
    val_df = core.standardization(valid, mean, std)
    test_df = core.standardization(test, mean, std)

    # Parameter
    param = data_helper.get(ws).window_parameter()
    log.debug(f'{param}')

    wide_window = core.WindowGenerator(input_width=param.in_step,
                                label_width=param.out_step,
                                shift=param.out_step,
                                train_df = train_df[param.in_feature],
                                val_df = val_df[param.in_feature],
                                test_df = test_df[param.in_feature],
                                label_columns=param.out_feature)    
    return wide_window

def window_generator_for_estimator(ws, source):    
    log = logger.get(__name__)
    log.info(f'train data nomarization...')
    log.debug(f"(mean: {ws.mean}, std: {ws.std})")
    test_df = core.standardization(source, ws.mean, ws.std)
    
    # Parameter
    param = data_helper.get(ws).window_parameter()
    log.debug(f'{param}')

    wide_window = core.WindowGenerator(input_width=param.in_step,
                                label_width=0,
                                shift=0,
                                train_df = None,
                                val_df = None,
                                test_df = test_df[param.in_feature],
                                label_columns=param.out_feature)    
    return wide_window
    

# create time window
def window_generator(ws, source):
    if ws.service == options.service.learner:
        return window_generator_for_learner(ws, source)

    if ws.service == options.service.estimator:
        return window_generator_for_estimator(ws, source)
        

#load_model    
def load_model(ws):
    return model_helper.load(ws)

# get model
def get_model(ws):
    return model_helper.get(ws)

# comple model
def compile(model, window):
    return compile_and_fit(model, window, patience=2, epochs=20)

# evaluate model
def evaluate(model, window):
    val = model.evaluate(window.val)
    test = model.evaluate(window.test)
    return val, test

# predict model
def predict(model, window):
    return model.predict(window.test)

# save model
def save(ws, model):
    return model_helper.save(ws, model)

# * 모델 컴파일에 사용하는 함수
def compile_and_fit(obj, window, patience=2, epochs=20):
    model = obj.get_model()
    early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss',
                                                    patience=patience,
                                                    mode='min')

    model.compile(loss=tf.losses.MeanSquaredError(),
                optimizer=tf.optimizers.Adam(),
                metrics=[tf.keras.metrics.MeanAbsolutePercentageError(), tf.metrics.MeanAbsoluteError()])

    history = model.fit(window.train, epochs=epochs,
                        validation_data=window.val,
                        callbacks=[early_stopping])
    
    return history

# export predict result of model
def export(ws, pred):
    log = logger.get(__name__)
    path = ws.export_path()
    log.info(f'export to file: {path}')
    if util.exists_exception(log, path):
        with open(path, 'w') as f:
            json.dump(pred, f, indent='\t')

