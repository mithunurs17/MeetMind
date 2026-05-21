import requests
import streamlit as st
import os

API_URL = os.getenv("API_URL", "http://backend:8000")


class APIClient:
    """Client for interacting with MeetMind AI Backend API."""
    
    def __init__(self, base_url: str = API_URL):
        self.base_url = base_url
    
    def health_check(self) -> dict:
        """Check API health status."""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            return response.json()
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def get_meetings(self, skip: int = 0, limit: int = 10) -> dict:
        """Get all meetings."""
        try:
            response = requests.get(
                f"{self.base_url}/meetings",
                params={"skip": skip, "limit": limit},
                timeout=10
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def create_meeting(self, title: str, description: str = None, 
                      participants: list = None) -> dict:
        """Create a new meeting."""
        try:
            payload = {
                "title": title,
                "description": description,
                "participants": participants or []
            }
            response = requests.post(
                f"{self.base_url}/meetings",
                json=payload,
                timeout=10
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}


# Initialize API client
api_client = APIClient()
