import numpy as np
import cv2 as cv
from tensorflow import keras

# Загружаем модель
try:
    # --- ИЗМЕНЕНИЕ 1: Загружаем файл .keras ---
    model = keras.models.load_model('image_classifier.keras')
    class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
    print("Модель 'image_classifier.keras' успешно загружена.")
except Exception as e:
    print(f"Ошибка при загрузке модели: {e}")
    model = None

def recognize(image_path):
    """Распознает изображение и возвращает имя класса."""
    if model is None:
        return "Ошибка: модель не загружена"

    try:
        # Подготовка изображения
        image = cv.imread(image_path)
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        image = cv.resize(image, (32, 32))

        # Готовим данные для модели
        data_for_predict = np.array([image]) / 255.0

        # --- ИЗМЕНЕНИЕ 2: Возвращаем стандартный .predict() ---
        # Теперь, когда мы загрузили настоящую Keras модель, у нее есть метод .predict()
        prediction = model.predict(data_for_predict)

        # Находим индекс класса с самой высокой вероятностью
        index = np.argmax(prediction)
        result = class_names[index]
        return result

    except Exception as e:
        print(f"!!! ПОЙМАНА ОШИБКА В БЛОКЕ TRY: {e}")
        return "Не удалось обработать изображение"