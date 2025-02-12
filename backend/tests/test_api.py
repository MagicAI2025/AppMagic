def test_generate_project():
    """Test project generation"""
    response = client.post(
        "/api/generate",
        json={
            "description": "Create a todo app",
            "project_type": "web"
        }
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Project generated successfully"
