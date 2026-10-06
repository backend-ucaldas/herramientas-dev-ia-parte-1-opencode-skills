def test_user_profile_skill_and_post_flow(client):
    user = client.post("/users", json={"name": "Ada", "email": "ada@example.com"})
    assert user.status_code == 201
    user_id = user.get_json()["id"]

    profile = client.put(f"/users/{user_id}/profile", json={"bio": "Engineer"})
    assert profile.status_code == 200
    assert profile.get_json()["user_id"] == user_id

    skill = client.post("/skills", json={"name": "Python"})
    assert skill.status_code == 201
    skill_id = skill.get_json()["id"]

    assigned = client.post(f"/users/{user_id}/skills/{skill_id}")
    assert assigned.status_code == 200
    assert assigned.get_json()["skills"] == [{"id": skill_id, "name": "Python"}]

    post = client.post(f"/users/{user_id}/posts", json={"title": "Hello", "content": "World"})
    assert post.status_code == 201
    post_id = post.get_json()["id"]

    updated = client.put(f"/posts/{post_id}", json={"content": "Updated"})
    assert updated.status_code == 200
    assert updated.get_json()["content"] == "Updated"

    assert client.delete(f"/users/{user_id}/skills/{skill_id}").status_code == 204
    assert client.delete(f"/posts/{post_id}").status_code == 204
    assert client.delete(f"/users/{user_id}").status_code == 204


def test_validation_conflicts_and_missing_resources(client):
    assert client.post("/users", json={"name": "Ada"}).status_code == 400

    first = client.post("/users", json={"name": "Ada", "email": "ada@example.com"})
    assert first.status_code == 201
    assert client.post("/users", json={"name": "Other", "email": "ada@example.com"}).status_code == 409
    assert client.get("/users/999").status_code == 404
    assert client.post("/users/999/posts", json={"title": "Title", "content": "Body"}).status_code == 404

    user_id = first.get_json()["id"]
    skill = client.post("/skills", json={"name": "Flask"})
    skill_id = skill.get_json()["id"]
    assert client.post(f"/users/{user_id}/skills/{skill_id}").status_code == 200
    assert client.post(f"/users/{user_id}/skills/{skill_id}").status_code == 409
    assert client.delete(f"/users/{user_id}/skills/999").status_code == 404
