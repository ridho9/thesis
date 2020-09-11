from pydantic import BaseModel, validator
from pydantic.class_validators import root_validator


class Model(BaseModel):
    id: str


class Mahasiswa(Model):
    name: str
    ipk: float
    sks: int
    have_paid: bool
    approved: bool

    @validator("ipk")
    def validate_ipk_range(cls, v):
        assert 0.0 <= v <= 4.0
        return v

    @validator("sks")
    def validate_sks_range(cls, v):
        assert 0 <= v <= 24
        return v

    @root_validator
    def validate_ambil_sks_menurut_ipk(cls, vs):
        ipk, sks = vs.get("ipk"), vs.get("sks")
        if ipk <= 2:
            assert sks <= 20
        return vs

    @root_validator
    def validate_approve_paid(cls, vs):
        paid, appr = vs.get("have_paid"), vs.get("approved")
        if appr:
            assert paid

        return vs