import numpy as np
import cv2 as cv
from tensorflow.keras.models import load_model

try:
    model = load_model('image_classifier.keras')
    class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
    print("Модель 'image_classifier.keras' успешно загружена.")
except Exception as e:
    print(f"Ошибка при загрузке модели: {e}")
    model = None

def recognize(image_path):
    if model is None:
        return "Ошибка: модель не загружена"

    try:
        # Подготовка изображения
        image = cv.imread(image_path)
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        image = cv.resize(image, (32, 32))

        data_for_predict = np.array([image]) / 255.0

        prediction = model.predict(data_for_predict)

        # Находим индекс класса с самой высокой вероятностью
        index = np.argmax(prediction)
        result = class_names[index]
        return result

    except Exception as e:
        print(f"!!! ПОЙМАНА ОШИБКА В БЛОКЕ TRY: {e}")
        return "Не удалось обработать изображение"