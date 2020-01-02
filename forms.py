from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
import phonenumbers

class PhoneForm(FlaskForm):
    phone = StringField('Mobile Phone Number', validators=[DataRequired()])
    submit = SubmitField('Send-SMS-LOLs')

    def validate_phone(self, phone):
        try:
            p = phonenumbers.parse(phone.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except phonenumbers.phonenumberutil.NumberParseException as e:
            raise ValidationError(e._msg) #using private method as there is no other way to access exception error message
        except (ValueError):
            raise ValidationError('Invalid phone number')
