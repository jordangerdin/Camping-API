from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class LocationInputForm(FlaskForm):
    city = StringField('City', validators=[DataRequired(), Length(max=50)])
    state = StringField('State', validators=[DataRequired(), Length(max=2)])
    
    submit=SubmitField('Find Trails')
