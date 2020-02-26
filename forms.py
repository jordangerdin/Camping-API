from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField
from wtforms.validators import DataRequired, Length, Email

# The sole form of this app, used to get the city and state and builds in some validation.
class LocationInputForm(FlaskForm):
    city = StringField('City', validators=[DataRequired(), Length(max=50)])
    state = StringField('State', validators=[DataRequired(), Length(max=2)])
    
    submit=SubmitField('Find Trails')
