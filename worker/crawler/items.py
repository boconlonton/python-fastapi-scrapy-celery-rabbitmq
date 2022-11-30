from enum import Enum

from typing import Mapping, Union, List

from scrapy.item import Item
from scrapy.item import Field


class UserType(Enum):
    Recruiter = "Recruiter"
    HiringManager = "HiringManager"
    InterviewTeam = "InterviewTeam"


class User:

    def __init__(self,
                 user_type: UserType = UserType.Recruiter,
                 user_id: str = None,
                 email: str = None,
                 phone_number: str = None,
                 name: str = None):
        self.user_type = user_type
        self.user_id = user_id
        self.email = email
        self.phone_number = phone_number
        self.name = name

    def to_dict(self) -> Mapping[str, Union[str, None]]:
        return {
            'type': self.user_type.value,
            'id': self.user_id,
            'email': self.email,
            'phone_number': self.phone_number,
            'name': self.name
        }


def serialize_user(value: List[User]):
    return [user.to_dict() for user in value]


class Job(Item):
    rid = Field()
    apply_url = Field()
    detail_url = Field()
    title = Field()
    description = Field()
    requirements = Field()
    job_type = Field()
    job_status = Field()
    salary = Field()
    questionnaire_id = Field()
    job_code = Field()
    location = Field()
    street_address = Field()
    city = Field()
    state = Field()
    postal_code = Field()
    country = Field()
    latitude = Field()
    longitude = Field()
    language_status = Field()
    custom_categories = Field()
    department = Field()
    date_posted = Field()
    brand = Field()
    national_restaurant_number = Field()
    custom_fields = Field()
    is_internal = Field(serializer=bool)
    is_remote = Field(serializer=bool)
    company_name = Field()
    users = Field(serializer=serialize_user)
