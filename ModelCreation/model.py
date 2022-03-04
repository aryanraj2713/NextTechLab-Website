import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model

left, right, up, down= np.load('left.npy'), np.load('right.npy'), np.load('up.npy'), np.load('down.npy')

y1 = np.full((1, len(left)), 0)
y2 = np.full((1, len(right)), 1)
y3 = np.full((1, len(up)), 2)
y4 = np.full((1, len(down)), 3)


x = np.concatenate((left, right, up, down), axis = 0)
y = np.concatenate((y1, y2, y3, y4), axis = 1)[0]

arg = tf.reshape(x, (670, 8, 1))
                
model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(8, input_shape=[8], activation='relu'),
        tf.keras.layers.Dense(4, activation='softmax')
        ])

model.compile(optimizer='sgd', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.summary()
try:
    model = load_model('sample_model.h5')
except:
    history = model.fit(arg, y, epochs=1)
    model.save("sample_model.h5")

#visualizing
"""
history_dict = history.history
print(history_dict.keys())
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
epochs = range(len(acc))

plt.plot(epochs, acc, 'b', label='Training Accuracy')
plt.plot(epochs, val_acc, 'r', label='Validation Accuracy')
plt.title('Accuracy Graph')
plt.legend()
plt.figure()

loss = history.history['loss']
val_loss = history.history['val_loss']
plt.plot(epochs, loss, 'b', label='Training Loss')
plt.plot(epochs, val_loss, 'r', label='Validation Loss')
plt.title('Loss Graph')
plt.legend()
plt.show()"""
