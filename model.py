import tensorflow as tf


class ANN(object):

    def __init__(self, in_shape_list, out_shape):
        self.name = None
        self.model = tf.keras.models.Sequential()
        self.model.add(tf.keras.Input(shape=(in_shape_list[0],)))
        for i in range(3):
            self.model.add(
                tf.keras.layers.Dense(units=in_shape_list[i + 1], activation='relu', input_shape=(in_shape_list[i],)))
            self.model.add(tf.keras.layers.Dropout(0.2))  # regularization
        self.model.add(tf.keras.layers.Dense(units=out_shape, activation='softmax'))

        opt = tf.keras.optimizers.SGD(learning_rate=0.0001, momentum=0.01)
        self.model.compile(optimizer=opt,
                           loss=tf.keras.losses.MeanSquaredLogarithmicError())

    def fit(self, X_train, y_train, epoch=1):
        print("updating " + self.name)
        self.model.fit(X_train, y_train, epochs=epoch, batch_size=10)
        print("updating done")

    def predict(self, testX):
        prediction = self.model(testX, training=False)
        return prediction.index(max(prediction))


class room_model(ANN):
    def __init__(self):
        super().__init__([72, 100, 50, 25], 9)
        self.name = "room_model"


class weapon_model(ANN):
    def __init__(self):
        super().__init__([42, 60, 30, 15], 6)
        self.name = "weapon_model"


class char_model(ANN):
    def __init__(self):
        super().__init__([42, 60, 30, 15], 6)
        self.name = "char_model"
