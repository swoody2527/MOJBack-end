from main import app
from fastapi.testclient import TestClient
import pytest



@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


def test_get_all_tasks(client):
    response = client.get('/tasks')

    data = response.json()
    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 3

    for task in data:
        assert 'id' in task and isinstance(task['id'], int)
        assert 'title' in task and isinstance(task['title'], str)
        assert 'status' in task and isinstance(task['status'], str)
        assert 'due' in task


def test_get_task_by_id(client):
    response = client.get('/task/1')

    data = response.json()
    assert response.status_code == 200
    assert isinstance(data, dict)
    assert data['id'] == 1
    assert data['title'] == 'Tesco Shop'
    assert data['desc'] == 'Milk, Bread, Eggs'
    assert data['status'] == 'todo'
    assert data['due'] == '2025-09-21'

def test_get_task_by_invalid_id(client):
    response = client.get('/task/1000')

    data = response.json()
    assert response.status_code == 404
    assert data['detail'] == 'No task with id: 1000.'



