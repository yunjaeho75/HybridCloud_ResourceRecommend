import numpy as np
import tensorflow as tf

def make_splite_dataset(df, t=0.7, v=0.2):
    n = len(df)
    a = df[0:int(n*t)]
    b = df[int(n*t):int(n*(t+v))]
    c = df[int(n*(t+v)):]
    d = df.shape[1]
    return a, b, c, d


# 데이터 표준화 함수
# def standardization(df, mean, std):
#     return (df - mean) / std
def standardization(pred, mean, std, inverse=False):
    if inverse is True :
        return pred * std + mean
    return (pred - mean) / std

# 데이터 윈도우 생성기
class WindowGenerator():
    def __init__(self, input_width, label_width, shift,
                 train_df, val_df, test_df,
                 label_columns):
        
        # Store the raw data.
        self.train_df = train_df
        self.val_df = val_df
        self.test_df = test_df

        # Work out the label column indices.
        self.label_columns = label_columns
        if label_columns is not None:
            self.label_columns_indices = {name: i for i, name in enumerate(label_columns)}

        if train_df is not None:
            self.column_indices = {name: i for i, name in enumerate(train_df.columns)}
        
        elif val_df is not None:
            self.column_indices = {name: i for i, name in enumerate(val_df.columns)}
        
        elif test_df is not None:
            self.column_indices = {name: i for i, name in enumerate(test_df.columns)}
        
        # Work out the window parameters.
        self.input_width = input_width
        self.label_width = label_width
        self.shift = shift

        self.total_window_size = input_width + shift

        self.input_slice = slice(0, input_width)
        self.input_indices = np.arange(self.total_window_size)[self.input_slice]

        self.label_start = self.total_window_size - self.label_width
        self.labels_slice = slice(self.label_start, None)
        self.label_indices = np.arange(self.total_window_size)[self.labels_slice]

        # print('\n'.join([
        #     f'self.input_width: {self.input_width}',
        #     f'self.label_width: {self.label_width}',
        #     f'self.shift: {self.shift}',
        #     f'self.total_window_size: {self.total_window_size}',
        #     f'self.input_slice: {self.input_slice}',
        #     f'self.input_indices: {self.input_indices}',
        #     f'self.label_start: {self.label_start}',
        #     f'self.labels_slice: {self.labels_slice}',
        #     f'self.label_indices: {self.label_indices}'])
        # )
        

    def split_window(self, features):        
        inputs = features[:, self.input_slice, :]
        labels = features[:, self.labels_slice, :]
        
        if self.label_columns is not None:
            labels = tf.stack(
                [labels[:, :, self.column_indices[name]] for name in self.label_columns],
                axis=-1)

        # Slicing doesn't preserve static shape information, so set the shapes
        # manually. This way the `tf.data.Datasets` are easier to inspect.
        inputs.set_shape([None, self.input_width, None])
        labels.set_shape([None, self.label_width, None])
        
        return inputs, labels

    def make_dataset(self, data):
        if data is None:
            return None

        data = np.array(data, dtype=np.float32)
        ds = tf.keras.preprocessing.timeseries_dataset_from_array(
            data=data,
            targets=None,
            sequence_length=self.total_window_size,
            sequence_stride=1,
            shuffle=True,
            batch_size=32,)

        ds = ds.map(self.split_window)
        
        return ds

    def shape(self):
        return self.test.element_spec
        
    @property
    def train(self):
        return self.make_dataset(self.train_df)

    @property
    def val(self):
        return self.make_dataset(self.val_df)

    @property
    def test(self):
        return self.make_dataset(self.test_df)

    @property
    def example(self):
        """Get and cache an example batch of `inputs, labels` for plotting."""
        result = getattr(self, '_example', None)
        if result is None:
            if self.train is not None:
                result = next(iter(self.train))
            elif self.val is not None:
                result = next(iter(self.val))
            elif self.test is not None:
                result = next(iter(self.test))
            self._example = result

        # if result is None:
        #     # No example batch was found, so get one from the `.train` dataset
        #     result = next(iter(self.train))
        #     # And cache it for next time
        #     self._example = result

        return result

    def __repr__(self):
        return '\n'.join([
            f'Total window size: {self.total_window_size}',
            f'Input indices: {self.input_indices}',
            f'Label indices: {self.label_indices}',
            f'Label column name(s): {self.label_columns}'])

    def describe(self):
        fmt = '\n'
        if self.train_df is not None:
            fmt.join(f'Train:\n{self.train_df.describe()}\n')
        if self.val_df is not None:
            fmt.join(f'Valid:\n{self.val_df.describe()}\n')
        if self.test_df is not None:
            fmt.join(f'Test:\n{self.test_df.describe()}\n')
        return fmt
        # return '\n'.join([
        #     f'Train:\n{self.train_df.describe()}\n',
        #     f'Valid:\n{self.val_df.describe()}\n',
        #     f'Test:\n{self.test_df.describe()}\n'])