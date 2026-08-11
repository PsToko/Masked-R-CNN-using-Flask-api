from main import app


def test_predict():
    client = app.test_client()

    with open("aura.png", "rb") as image:
        response = client.post(
            "/predict",
            data={
                "image": image
            },
            content_type="multipart/form-data"
        )

    assert response.status_code == 200

    data = response.get_json()

    assert "predictions" in data
    assert "image" in data