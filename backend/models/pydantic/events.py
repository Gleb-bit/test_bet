from decimal import Decimal

from pydantic import BaseModel, model_validator, Field

from models.sql.events import EventStatus


class EventCreate(BaseModel):
    number: str
    coefficient: Decimal = Field(gt=0, max_digits=5, decimal_places=2)

    deadline: int = Field(gt=0)
    status: EventStatus

    @model_validator(mode="before")
    def check_coefficient(cls, values):
        coefficient = values["coefficient"]
        if not isinstance(coefficient, float):
            raise ValueError(
                "coefficient must be a float value with 2 values after point"
            )

        return values
