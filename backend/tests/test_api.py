import os
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Dynamic path to sample video
BASE_DIR = os.path.dirname(__file__)
TEST_VIDEO_PATH = os.path.join(BASE_DIR, "samples", "sample_2.mp4")

# Check that the video exists before running tests
@pytest.fixture(scope="session", autouse=True)
def check_test_video():
    assert os.path.exists(TEST_VIDEO_PATH), f"Sample video not found at path: {TEST_VIDEO_PATH}"

# Run /analyze and return the video_id for other tests
@pytest.fixture(scope="module")
def analyzed_video_id():
    with open(TEST_VIDEO_PATH, "rb") as video_file:
        response = client.post(
            "/analyze",
            files={"file": ("sample_2.mp4", video_file, "video/mp4")}
        )
    print(f"\n[DEBUG] /analyze status: {response.status_code}")
    print(f"[DEBUG] /analyze response: {response.json()}")
    assert response.status_code == 200
    data = response.json()
    return data["video_id"]

# Test analyze endpoint (basic success)
def test_analyze_endpoint(analyzed_video_id):
    assert isinstance(analyzed_video_id, str)
    assert len(analyzed_video_id) > 0

# Test results retrieval
def test_results_endpoint(analyzed_video_id):
    response = client.get(f"/results/{analyzed_video_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["video_id"] == analyzed_video_id
    assert isinstance(data["data"], list)
    assert "text" in data["data"][0]

# Optional: test no file sent
def test_analyze_no_file():
    response = client.post("/analyze", files={})
    assert response.status_code == 422
    assert response.json()["status"] == "error"

# Optional: test wrong format
def test_analyze_invalid_format():
    from io import BytesIO
    fake_file = BytesIO(b"This is not a video.")
    response = client.post(
        "/analyze",
        files={"file": ("fake.txt", fake_file, "text/plain")}
    )
    assert response.status_code == 400
    assert "Unsupported" in response.json()["message"]
