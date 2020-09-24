import sys
from pydantic.main import validate_custom_root_type
from requests.api import get
from timun import given, when, then


from fastapi.testclient import TestClient
from perwalian_api.model import Mahasiswa
from perwalian_api.main import app


def get_mahasiswa(ctx, id):
    client: TestClient = ctx["client"]
    return client.get(f"/mahasiswa/{id}")


def update_mahasiswa(ctx, id, data):
    client: TestClient = ctx["client"]
    resp = client.post(f"/mahasiswa/{id}", json=data)
    return resp


def str_to_bool(s: str):
    return s.lower() not in ["false"]


@when("mahasiswa {id} ipk is {value}")
def when_mahasiswa_ipk(ctx, id, value):
    mhs = get_mahasiswa(ctx, id).json()
    mhs["ipk"] = float(value)
    resp = update_mahasiswa(ctx, id, mhs)


@then("mahasiswa {id} ipk is {value}")
def then_mahasiswa_ipk(ctx, id, value):
    mhs = get_mahasiswa(ctx, id).json()
    assert mhs["ipk"] == float(value)


@when("mahasiswa {id} ambil sks {value}")
def when_mahasiswa_sks(ctx, id, value):
    mhs = get_mahasiswa(ctx, id).json()
    mhs["sks"] = float(value)
    resp = update_mahasiswa(ctx, id, mhs)


@then("mahasiswa {id} ambil sks {value}")
def then_mahasiswa_sks(ctx, id, value):
    mhs = get_mahasiswa(ctx, id).json()
    assert mhs["sks"] == int(value)


@when("mahasiswa {id} have paid {value}")
def when_mahasiswa_have_paid(ctx, id, value):
    mhs = get_mahasiswa(ctx, id).json()
    mhs["have_paid"] = value
    resp = update_mahasiswa(ctx, id, mhs)


@then("mahasiswa {id} have paid {value}")
def then_mahasiswa_have_paid(ctx, id, value):
    mhs = get_mahasiswa(ctx, id).json()
    value = str_to_bool(value)
    assert mhs["have_paid"] == value


@when("mahasiswa {id} approve {value}")
def when_mahasiswa_approve(ctx, id, value):
    mhs = get_mahasiswa(ctx, id).json()
    mhs["approved"] = value
    resp = update_mahasiswa(ctx, id, mhs)


# ===========================


# @then("mahasiswa {id} approve true")
# def then_mahasiswa_approve_true(ctx, id):
#     mhs = get_mahasiswa(ctx, id).json()
#     assert mhs["approved"] == True


# @then("mahasiswa {id} approve false")
# def then_mahasiswa_approve_false(ctx, id):
#     mhs = get_mahasiswa(ctx, id).json()
#     assert mhs["approved"] != True


# ===========================


@then("mahasiswa {id} approve {value}")
def then_mahasiswa_approve(ctx, id, value):
    mhs = get_mahasiswa(ctx, id).json()
    value = str_to_bool(value)
    assert mhs["approved"] == value


@given("provided mahasiswa {id}")
def create_mahasiswa(ctx, id):
    data = {
        "id": id,
        "name": f"Mahasiswa {id}",
        "ipk": 0,
        "sks": 0,
        "have_paid": False,
        "approved": False,
    }

    client: TestClient = ctx["client"]
    resp = client.post(f"/mahasiswa", json=data)
    assert resp.status_code == 201


@then("mahasiswa {id} exists")
def mahasiswa_exists(ctx, id):
    resp = get_mahasiswa(ctx, id)
    assert resp.status_code == 200
    assert resp.json()["id"] == id


@then("mahasiswa {id} not exists")
def mahasiswa_not_exists(ctx, id):
    resp = get_mahasiswa(ctx, id)
    assert resp.status_code != 200
    assert resp.json() == None