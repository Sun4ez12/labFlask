import os
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SelectField
from werkzeug.utils import secure_filename

# Импорт собственных модулей
import neural
import defs

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config["SECRET_KEY"] = "a-very-secret-key-that-you-should-change"
app.config["RECAPTCHA_PUBLIC_KEY"] = "6Lf6hmsrAAAAAEavmY8GVt0VlMH5sMH00ZAjiyYY"
app.config["RECAPTCHA_PRIVATE_KEY"] = "6Lf6hmsrAAAAAPupLxmnlsu4QHIx2BGuJ33t7_6A"
app.config['UPLOAD_FOLDER'] = 'static'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


class NeuralNetForm(FlaskForm):
    upload_first = FileField(
        'Загрузите изображение для распознавания',
        validators=[
            FileRequired(message='Нужно выбрать файл!'),
            FileAllowed(ALLOWED_EXTENSIONS, 'Только изображения!')
        ]
    )
    recaptcha = RecaptchaField()


class ImageTaskForm(FlaskForm):
    upload_file = FileField(
        'Загрузите изображение для обработки',
        validators=[
            FileRequired(message='Нужно выбрать файл!'),
            FileAllowed(ALLOWED_EXTENSIONS, 'Только изображения!')
        ]
    )



@app.route("/", methods=["GET", "POST"])
def home():
    form = NeuralNetForm()

    if form.validate_on_submit():
        f = form.upload_first.data
        filename = secure_filename('neural_img.png')
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        f.save(filepath)

        # Распознаем изображение
        recognized_class = neural.recognize(filepath)

        return render_template('start.html', form=form, img_filename=filename, neur=recognized_class)

    return render_template("start.html", form=form)


@app.route('/load', methods=['GET', 'POST'])
def upload_file():
    form = ImageTaskForm()
    if form.validate_on_submit():
        original_filename = "original_image.png"
        puzzled_filename = "puzzled_image.png"
        histogram_original_filename = "histogram_original.png"
        histogram_puzzled_filename = "histogram_puzzled.png"

        upload_folder = app.config['UPLOAD_FOLDER']
        original_path = os.path.join(upload_folder, original_filename)
        puzzled_path = os.path.join(upload_folder, puzzled_filename)
        histogram_original_path = os.path.join(upload_folder, histogram_original_filename)
        histogram_puzzled_path = os.path.join(upload_folder, histogram_puzzled_filename)

        f = form.upload_file.data
        f.save(original_path)

        defs.split_and_rotate_image(original_path, root=upload_folder + '/')
        defs.GRAPHS(original_path, histogram_original_path, name='Гистограмма исходного изображения')
        defs.GRAPHS(puzzled_path, histogram_puzzled_path, name='Гистограмма итогового изображения')

        return render_template(
            'form.html',
            form=form,
            original_img_fn=original_filename,
            puzzled_img_fn=puzzled_filename,
            histogram_original_fn=histogram_original_filename,
            histogram_puzzled_fn=histogram_puzzled_filename
        )

    return render_template('form.html', form=form)


if __name__ == "__main__":
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)