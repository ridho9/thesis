import sys
from timun import given, when, then


from fastapi.testclient import TestClient
from perwalian_api.model import Mahasiswa
from perwalian_api.main import app


@given("prepare mahasiswa {id}")
def prepare_mahasiswa(ctx, id):
    ctx[f"mahasiswa-{id}"] = {
        "id": id,
        "name": "Ridho Pratama",
        "ipk": 2.0,
        "sks": 10,
        "have_paid": False,
        "approved": False,
    }


@given("mahasiswa {id} have paid {value}")
def mahasiswa_have_paid(ctx, id, value):
    ctx[f"mahasiswa-{id}"]["have_paid"] = value


@given("mahasiswa {id} approve {value}")
def mahasiswa_approve(ctx, id, value):
    ctx[f"mahasiswa-{id}"]["approved"] = value


@given("mahasiswa {id} name is {name}")
def mahasiswa_name(ctx, id, name):
    ctx[f"mahasiswa-{id}"]["name"] = name


@given("mahasiswa {id} ipk is {value}")
def mahasiswa_ipk(ctx, id, value):
    ctx[f"mahasiswa-{id}"]["ipk"] = float(value)


@given("mahasiswa {id} ambil sks {value}")
def mahasiswa_sks(ctx, id, value):
    ctx[f"mahasiswa-{id}"]["sks"] = int(value)


@when("create mahasiswa {id}")
def create_mahasiswa(ctx, id):
    data = ctx[f"mahasiswa-{id}"]

    client: TestClient = ctx["client"]
    resp = client.post(f"/mahasiswa", json=data)
    assert resp.status_code == 201


@then("mahasiswa {id} exists")
def mahasiswa_exists(ctx, id):
    client: TestClient = ctx["client"]
    resp = client.get(f"/mahasiswa/{id}")
    assert resp.status_code == 200
    assert resp.json()["id"] == id