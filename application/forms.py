from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SubmitField
from wtforms.validators import DataRequired

class BlogForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    description = TextAreaField('description',validators=[DataRequired()])
    image = FileField('image',validators=[DataRequired()])
    submit = SubmitField("Add blogs")