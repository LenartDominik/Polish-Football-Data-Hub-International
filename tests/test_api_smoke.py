def test_read_root(client):
    """Sprawdź czy główny endpoint działa"""
    response = client.get("/")
    assert response.status_code == 200

def test_health_check(client):
    """Sprawdź endpoint health check"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "timestamp" in data
