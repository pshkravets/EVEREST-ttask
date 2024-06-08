from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Length
from wtforms_sqlalchemy.fields import QuerySelectField

from models import Country


class AddressForm(FlaskForm):
    country = QuerySelectField('Country', query_factory=lambda : Country.query.all(), allow_blank=True, get_label='name')
    city = QuerySelectField('City', get_label='name', allow_blank=True)
    address = StringField('Address', validators=[DataRequired(), Length(max=200)])
    amount = IntegerField('Amount', validators=[DataRequired()])