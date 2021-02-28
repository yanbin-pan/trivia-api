from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SelectField,
    SelectMultipleField,
    DateTimeField,
    TextAreaField,
    BooleanField,
)
from wtforms.validators import DataRequired, AnyOf, URL, Regexp, ValidationError, URL
import re
from enums import Genre, State


class ShowForm(FlaskForm):
    artist_id = StringField("artist_id")
    venue_id = StringField("venue_id")
    start_time = DateTimeField(
        "start_time", validators=[DataRequired()], default=datetime.today()
    )


class VenueForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    city = StringField("city", validators=[DataRequired()])
    state = SelectField("state", validators=[DataRequired()], choices=State.choices())
    address = StringField("address", validators=[DataRequired()])
    phone = StringField(
        "phone",
        validators=[
            DataRequired(),
            Regexp("^[0-9]*$", message="Phone number should only contain digits"),
        ],
    )
    image_link = StringField("image_link")
    genres = SelectMultipleField(
        "genres", validators=[DataRequired()], choices=Genre.choices()
    )
    facebook_link = StringField("facebook_link", validators=[URL()])
    website = StringField("website", validators=[URL()])
    seeking_talent = BooleanField("seeking_talent")
    seeking_description = StringField("seeking_description")

    def validate(self):
        """Define a custom validate method in your Form:"""
        rv = FlaskForm.validate(self)
        if not rv:
            return False
        if not set(self.genres.data).issubset(dict(Genre.choices()).keys()):
            self.genres.errors.append("Invalid genre.")
            return False
        if self.state.data not in dict(State.choices()).keys():
            self.state.errors.append("Invalid state.")
            return False
        # if pass validation
        return True


class ArtistForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    city = StringField("city", validators=[DataRequired()])
    state = SelectField("state", validators=[DataRequired()], choices=State.choices())

    phone = StringField(
        "phone",
        validators=[
            # DataRequired(),
            Regexp("^[0-9]*$", message="Phone number should only contain digits"),
        ],
    )

    image_link = StringField("image_link")
    genres = SelectMultipleField(
        "genres", validators=[DataRequired()], choices=Genre.choices()
    )
    facebook_link = StringField("facebook_link", validators=[URL()])

    website = StringField("website", validators=[URL()])

    seeking_venue = BooleanField("seeking_venue")

    seeking_description = StringField("seeking_description")

    def validate(self):
        """Define a custom validate method in your Form:"""
        rv = FlaskForm.validate(self)
        if not rv:
            return False
        if not set(self.genres.data).issubset(dict(Genre.choices()).keys()):
            self.genres.errors.append("Invalid genre.")
            return False
        if self.state.data not in dict(State.choices()).keys():
            self.state.errors.append("Invalid state.")
            return False
        # if pass validation
        return True
