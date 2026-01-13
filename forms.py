from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField
from wtforms.validators import DataRequired

choices = [("5", "ძალიან"), ("3", "საშუალოდ"), ("1", "არა")]

class TestForm(FlaskForm):

    q1 = RadioField(
        "გიყვარს ლოგიკური და მათემატიკური ამოცანები?",
        choices=choices,
        validators=[DataRequired()]
    )
    q2 = RadioField(
        "გიყვარს მონაცემების ანალიზება და გამოთვლა?",
        choices=choices,
        validators=[DataRequired()]
    )

    q3 = RadioField(
        "გაინტერესებს ტექნოლოგიები და კომპიუტერები?",
        choices=choices,
        validators=[DataRequired()]
    )
    q4 = RadioField(
        "ხშირად მუშაობ კომპიუტერებთან?",
        choices=choices,
        validators=[DataRequired()]
    )

    q5 = RadioField(
        "გიყვარს ხატვა, დიზაინების მოფიქრება ან კრეატიული საქმიანობა?",
        choices=choices,
        validators=[DataRequired()]
    )
    q6 = RadioField(
        "თავი კრეატიულად მიგაჩნია?",
        choices=choices,
        validators=[DataRequired()]
    )

    q7 = RadioField(
        "გიყვარს ადამიანებთან კომუნიკაცია?",
        choices=choices,
        validators=[DataRequired()]
    )
    q8 = RadioField(
        "ხალხთან კომუნიკაცია და გართობა ენერგიას გმატებს?",
        choices=choices,
        validators=[DataRequired()]
    )


    q9 = RadioField(
        "მარტო მუშაობას ჯგუფთან ერთად მუშაობა გირჩევნია?",
        choices=choices,
        validators=[DataRequired()]
    )
    q10 = RadioField(
        "ახალ მასალას ადვილად ითვისებ?",
        choices=choices,
        validators=[DataRequired()]
    )

    submit = SubmitField("შედეგის ნახვა")
