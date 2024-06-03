from typing import Optional

from pydantic import BaseModel, validator


class SecretList(BaseModel):
    name: str
    secret_name: Optional[str] = None

    @validator('secret_name', always=True)
    def set_secret_name(cls, value, values):
        return '{{secret.%s}}' % values['name']


class SecretCreate(BaseModel):
    name: str
    value: Optional[str] = None


class SecretUpdate(SecretCreate):
    ...


class SecretDetail(SecretList, SecretCreate):
    is_hidden: Optional[bool] = False
