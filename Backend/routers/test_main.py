from fastapi.testclient import TestClient
from starlette import status
import main


test_clinet=TestClient(main.app)


def test_check_healthy():
    response = test_clinet("/healthy")
    assert response.staus_code==status.HTTP_200_OK