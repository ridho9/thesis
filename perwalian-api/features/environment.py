from fastapi.testclient import TestClient
from perwalian_api.main import app


def before_scenario(ctx):
    # print("before_scenario")
    ctx["client"] = TestClient(app)
    client: TestClient = ctx["client"]
    resp = client.post("/store/_clear")
    assert resp.status_code == 200
    assert resp.text == '"ok"'
