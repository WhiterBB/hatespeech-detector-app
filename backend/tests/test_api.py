import os
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

BASE_DIR = os.path.dirname(__file__)
TEST_VIDEO_PATH = os.path.join(BASE_DIR, "samples", "sample_1.mp4")


@pytest.fixture(scope="session", autouse=True)
def check_test_video():
    assert os.path.exists(TEST_VIDEO_PATH), f"Sample video not found at path: {TEST_VIDEO_PATH}"

def test_analyze_endpoint():
    with open(TEST_VIDEO_PATH, "rb") as video_file:
        response = client.post(
            "/analyze",
            files={"file": ("sample_1.mp4", video_file, "video/mp4")}
        )
    assert response.status_code == 200
    data = response.json()
    assert "video_id" in data
    assert "data" in data
    assert isinstance(data["data"], list)
    assert all("text" in segment for segment in data["data"])

    # Save video_id to test GET
    global saved_video_id
    saved_video_id = data["video_id"]

def test_results_endpoint():
    global saved_video_id
    assert saved_video_id, "You must run test_analyze_endpoint first"

    response = client.get(f"/results/{saved_video_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["video_id"] == saved_video_id
