from PIL import Image
import matplotlib.pyplot as plt
from skimage import io


def split_and_rotate_image(image_path, root='static/'):

    try:
        img = Image.open(image_path)
        width, height = img.size

        mid_x = width // 2
        mid_y = height // 2

        # crop(left, upper, right, lower)
        top_left = img.crop((0, 0, mid_x, mid_y))
        top_right = img.crop((mid_x, 0, width, mid_y))
        bottom_left = img.crop((0, mid_y, mid_x, height))
        bottom_right = img.crop((mid_x, mid_y, width, height))

        new_img = Image.new('RGB', (width, height))

        new_img.paste(top_left, (mid_x, 0))
        new_img.paste(top_right, (mid_x, mid_y))
        new_img.paste(bottom_right, (0, mid_y))
        new_img.paste(bottom_left, (0, 0))

        # 6. Сохраняем результат и возвращаем путь к нему
        puzzled_path = root + 'puzzled_image.png'
        new_img.save(puzzled_path)
        return puzzled_path

    except Exception as e:
        print(f"Ошибка в split_and_rotate_image: {e}")
        return None


def GRAPHS(path, root, name):
    image = io.imread(path)

    plt.clf()  # Очищаем фигуру перед новым графиком

    plt.hist(image.ravel(), bins=256, color='Orange', label='Total', range=(0, 256))
    plt.hist(image[:, :, 0].ravel(), bins=256, color='Red', alpha=0.7, label='Red Channel', range=(0, 256))
    plt.hist(image[:, :, 1].ravel(), bins=256, color='Green', alpha=0.7, label='Green Channel', range=(0, 256))
    plt.hist(image[:, :, 2].ravel(), bins=256, color='Blue', alpha=0.7, label='Blue Channel', range=(0, 256))

    plt.xlabel('Intensity Value')
    plt.ylabel('Count')
    plt.legend()
    plt.title(name)

    plt.savefig(root)