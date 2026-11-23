def create_equipment(client, serial="CMP-001"):
    return client.post(
        "/api/v1/equipment",
        json={
            "name": "Компрессор К-14",
            "location": "Цех №2",
            "status": "active",
            "serial_number": serial,
        },
    )


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_and_get_equipment(client):
    created = create_equipment(client)
    assert created.status_code == 201
    equipment_id = created.json()["id"]
    response = client.get(f"/api/v1/equipment/{equipment_id}")
    assert response.status_code == 200
    assert response.json()["serial_number"] == "CMP-001"


def test_list_equipment(client):
    create_equipment(client, "CMP-001")
    create_equipment(client, "CMP-002")
    response = client.get("/api/v1/equipment")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_update_equipment(client):
    equipment_id = create_equipment(client).json()["id"]
    response = client.patch(
        f"/api/v1/equipment/{equipment_id}",
        json={"status": "maintenance"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "maintenance"


def test_delete_equipment(client):
    equipment_id = create_equipment(client).json()["id"]
    response = client.delete(f"/api/v1/equipment/{equipment_id}")
    assert response.status_code == 204
    assert client.get(f"/api/v1/equipment/{equipment_id}").status_code == 404


def test_unknown_equipment_returns_404(client):
    assert client.get("/api/v1/equipment/999").status_code == 404


def test_duplicate_serial_number_returns_409(client):
    create_equipment(client, "DUP-001")
    response = create_equipment(client, "DUP-001")
    assert response.status_code == 409


def test_create_and_list_measurements(client):
    equipment_id = create_equipment(client).json()["id"]
    created = client.post(
        f"/api/v1/equipment/{equipment_id}/measurements",
        json={"temperature": 72.5, "pressure": 4.8},
    )
    assert created.status_code == 201
    assert created.json()["equipment_id"] == equipment_id
    history = client.get(f"/api/v1/equipment/{equipment_id}/measurements")
    assert history.status_code == 200
    assert len(history.json()) == 1


def test_measurement_for_unknown_equipment_returns_404(client):
    response = client.post(
        "/api/v1/equipment/999/measurements",
        json={"temperature": 72.5, "pressure": 4.8},
    )
    assert response.status_code == 404


def test_invalid_measurement_is_rejected(client):
    equipment_id = create_equipment(client).json()["id"]
    response = client.post(
        f"/api/v1/equipment/{equipment_id}/measurements",
        json={"temperature": 72.5, "pressure": -1},
    )
    assert response.status_code == 422
