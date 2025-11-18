from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Import all models here for Alembic
from app.models.user import User  # noqa
from app.models.membership_plan import MembershipPlan  # noqa
from app.models.member import Member  # noqa
from app.models.check_in import CheckIn  # noqa
