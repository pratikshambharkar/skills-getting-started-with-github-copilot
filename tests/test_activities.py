import urllib.parse

from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    # expect known activity keys
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    activity = "Chess Club"
    email = "testuser@mergington.edu"

    # ensure email not already present
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # signup
    signup_url = f"/activities/{urllib.parse.quote(activity)}/signup?email={urllib.parse.quote(email)}"
    resp = client.post(signup_url)
    assert resp.status_code == 200
    assert email in activities[activity]["participants"]

    # try duplicate signup -> should 400
    resp_dup = client.post(signup_url)
    assert resp_dup.status_code == 400

    # unregister
    delete_url = f"/activities/{urllib.parse.quote(activity)}/participants?email={urllib.parse.quote(email)}"
    resp_del = client.delete(delete_url)
    assert resp_del.status_code == 200
    assert email not in activities[activity]["participants"]

    # unregister non-existing -> 404
    resp_del2 = client.delete(delete_url)
    assert resp_del2.status_code == 404
