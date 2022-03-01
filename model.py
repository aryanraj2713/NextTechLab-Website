import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model

left, right, up, down= np.load('left.npy'), np.load('right.npy'), np.load('up.npy'), np.load('down.npy')

#print(len(left) + len(right) + len(up) + len(down))

y1 = np.full((1, len(left)), 0)
y2 = np.full((1, len(right)), 1)
y3 = np.full((1, len(up)), 2)
y4 = np.full((1, len(down)), 3)


x = np.concatenate((left, right, up, down), axis = 0)
y = np.concatenate((y1, y2, y3, y4), axis = 1)[0]

arg = tf.reshape(x, (670, 8, 1))
print(arg)


model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(8, input_shape=[8], activation='relu'),
        #tf.keras.layers.Dense(, activation='relu'),
        tf.keras.layers.Dense(4, activation='softmax')
        ])

model.compile(optimizer='sgd', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.summary()
try:
    model = load_model('model.h5')
except:
    history = model.fit(arg, y, epochs=500)
    model.save("model.h5")


