from pydantic import BaseModel


class Fixrequest(BaseModel):
    language: str
    cwe: str
    code: str
