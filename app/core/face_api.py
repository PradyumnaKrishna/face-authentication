import requests
from fastapi import status
from requests import Response

from .exceptions import BadRequest, InternalError
from .settings import get_settings, Settings


class FaceAPI:
    def __init__(self, settings: Settings = get_settings()) -> None:
        self.endpoint = settings.FACE_API_ENDPOINT
        self.key = settings.FACE_API_KEY
        self.group = settings.FACE_API_GROUP

        self.headers = {
            "Content-Type": "application/json",
            "Ocp-Apim-Subscription-Key": self.key,
        }

    @staticmethod
    def _extract(response: Response) -> dict:
        if response.ok:
            return response.json()
        if response.status_code == status.HTTP_400_BAD_REQUEST:
            raise BadRequest(detail=response.json())
        raise InternalError(f"Face API failed with response {response.json()}")

    def add_face(self, person_id: str, file_url: str) -> bool:
        url = f"{self.endpoint}/face/v1.0/persongroups/{self.group}/persons/{person_id}/persistedFaces"

        payload = {"url": file_url}

        response = requests.post(url, headers=self.headers, json=payload)

        self._extract(response)
        return True

    def create_person(self, name: str) -> str:
        url = f"{self.endpoint}/face/v1.0/persongroups/{self.group}/persons"

        payload = {"name": name}

        response = requests.post(url, headers=self.headers, json=payload)

        json_response = self._extract(response)
        return json_response["personId"]

    def detect(self, file_url: str) -> str:
        url = f"{self.endpoint}/face/v1.0/detect?returnFaceId=true&recognitionModel=recognition_04"

        payload = {"url": file_url}

        response = requests.post(url, headers=self.headers, json=payload)

        json_response = self._extract(response)
        if json_response:
            return json_response[0]["faceId"]
        raise BadRequest(detail="Face not found")

    def verify(self, person_id: str, face_id: str) -> bool:
        url = f"{self.endpoint}/face/v1.0/verify"

        payload = {
            "faceId": face_id,
            "personId": person_id,
            "personGroupId": self.group,
        }

        response = requests.post(url, headers=self.headers, json=payload)

        json_response = self._extract(response)
        return json_response["isIdentical"]
