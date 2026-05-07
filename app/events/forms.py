from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeLocalField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


class EventForm(FlaskForm):
    title       = StringField('Title',
                              validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description', validators=[Optional()])
    location    = StringField('Location',
                              validators=[Optional(), Length(max=200)])
    starts_at   = DateTimeLocalField('Starts at', format='%Y-%m-%dT%H:%M',
                                     validators=[DataRequired()])
    ends_at     = DateTimeLocalField('Ends at', format='%Y-%m-%dT%H:%M',
                                     validators=[Optional()])
    submit      = SubmitField('Save event')
