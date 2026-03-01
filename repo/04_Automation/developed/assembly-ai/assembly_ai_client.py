"""
Assembly AI API Client

AssemblyAI provides AI-powered speech-to-text and audio intelligence APIs.

API Actions (3):
1. Transcribe Audio
2. Upload Media File
3. Get Transcription Result

Triggers (0):

Authentication: API Key
Base URL: https://api.assemblyai.com/v2
Documentation: https://www.assemblyai.com/docs/
Rate Limiting: Varies by plan
"""

import aiohttp
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
import hashlib


@dataclass
class Transcript:
    """Transcript model"""
    id: str
    status: str
    text: str
    audio_url: str
    language_code: str
    created: str
    completed: Optional[str] = None
    confidence: float = 0.0
    words: List[Dict[str, Any]] = field(default_factory=list)
    utterances: List[Dict[str, Any]] = field(default_factory=list)
    speakers_expected: Optional[int] = None
    speakers: Optional[int] = None


@dataclass
class UploadResponse:
    """Upload response model"""
    upload_url: str
    audio_file_id: Optional[str] = None


@dataclass
class Word:
    """Word alignment model"""
    text: str
    start: float
    end: float
    confidence: float
    speaker: Optional[str] = None


@dataclass
class Utterance:
    """Utterance model (speaker diarization)"""
    speaker: str
    text: str
    start: float
    end: float
    confidence: float


class AssemblyAIClient:
    """
    AssemblyAI API client for audio transcription.

    Supports: Audio upload, transcription, speaker diarization
    Rate limit: Varies by plan (typically generous)
    """

    BASE_URL = "https://api.assemblyai.com/v2"

    def __init__(self, api_key: str):
        """
        Initialize AssemblyAI client.

        Args:
            api_key: AssemblyAI API key
        """
        self.api_key = api_key
        self.session = None
        self._headers = {
            "authorization": api_key,
            "content-type": "application/json"
        }

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        json_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make API request.

        Args:
            method: HTTP method
            endpoint: API endpoint
            data: Form data
            params: Query parameters
            headers: Additional headers
            json_data: JSON data

        Returns:
            Response JSON

        Raises:
            Exception: If request fails
        """
        url = f"{self.BASE_URL}{endpoint}"
        request_headers = self._headers.copy()
        if headers:
            request_headers.update(headers)

        async with self.session.request(
            method,
            url,
            headers=request_headers,
            data=data,
            params=params,
            json=json_data
        ) as response:
            try:
                result = await response.json()
            except:
                result = {}

            if response.status not in [200, 201]:
                error = result.get("error", str(result))
                raise Exception(
                    f"AssemblyAI API error: {response.status} - {error}"
                )

            return result

    # ==================== Upload Operations ====================

    async def upload_media_file(
        self,
        file_url: Optional[str] = None,
        file_path: Optional[str] = None,
        file_content: Optional[bytes] = None
    ) -> UploadResponse:
        """
        Upload a media file for transcription.

        Args:
            file_url: URL of the media file
            file_path: Local path to the media file
            file_content: Raw file content as bytes

        Returns:
            UploadResponse with upload_url

        Raises:
            Exception: If upload fails
        """
        if file_url:
            # For URLs, we don't need to upload - AssemblyAI can transcribe directly
            return UploadResponse(upload_url=file_url)

        elif file_path:
            # Upload local file
            with open(file_path, "rb") as f:
                file_content = f.read()

            return await self._upload_content(file_content)

        elif file_content:
            # Upload content directly
            return await self._upload_content(file_content)

        else:
            raise ValueError("Either file_url, file_path, or file_content must be provided")

    async def _upload_content(self, content: bytes) -> UploadResponse:
        """
        Upload content bytes.

        Args:
            content: File content as bytes

        Returns:
            UploadResponse
        """
        headers = {
            "authorization": self.api_key,
            "content-type": "application/octet-stream"
        }

        async with self.session.post(
            f"{self.BASE_URL}/upload",
            headers=headers,
            data=content
        ) as response:
            result = await response.json()

            if response.status != 200:
                error = result.get("error", str(result))
                raise Exception(f"Upload failed: {error}")

            return UploadResponse(
                upload_url=result.get("upload_url", ""),
                audio_file_id=result.get("audio_file_id")
            )

    # ==================== Transcription Operations ====================

    async def transcribe_audio(
        self,
        audio_url: str,
        language_code: str = "en_us",
        enable_speaker_diarization: bool = False,
        speakers_expected: Optional[int] = None,
        enable_auto_highlights: bool = False,
        enable_entity_detection: bool = False,
        enable_sentiment_analysis: bool = False,
        enable_summarization: bool = False,
        summary_model: str = "conversational",
        summary_type: str = "bullets",
        poll: bool = True,
        poll_interval: float = 1.0,
        timeout: int = 300
    ) -> Transcript:
        """
        Transcribe audio file.

        Args:
            audio_url: URL of the audio file (or from upload response)
            language_code: Language code (e.g., "en_us", "ja", "ko")
            enable_speaker_diarization: Enable speaker identification
            speakers_expected: Number of speakers to detect
            enable_auto_highlights: Enable key phrase detection
            enable_entity_detection: Enable entity detection
            enable_sentiment_analysis: Enable sentiment analysis
            enable_summarization: Enable summarization
            summary_model: Summary model ("conversational", "generic")
            summary_type: Summary type ("bullets", "paragraph", "headline")
            poll: Whether to poll for completion
            poll_interval: Seconds between polls
            timeout: Maximum seconds to wait

        Returns:
            Transcript object

        Raises:
            Exception: If transcription fails
        """
        data = {
            "audio_url": audio_url,
            "language_code": language_code
        }

        if enable_speaker_diarization:
            data["speaker_labels"] = True
            if speakers_expected:
                data["speakers_expected"] = speakers_expected

        if enable_auto_highlights:
            data["auto_highlights"] = True

        if enable_entity_detection:
            data["entity_detection"] = True

        if enable_sentiment_analysis:
            data["sentiment_analysis"] = True

        if enable_summarization:
            data["summarization"] = True
            data["summary_model"] = summary_model
            data["summary_type"] = summary_type

        response = await self._make_request("POST", "/transcript", json_data=data)
        transcript = Transcript(**response)

        if poll:
            transcript = await self._poll_transcription(
                transcript.id,
                poll_interval=poll_interval,
                timeout=timeout
            )

        return transcript

    async def get_transcription_result(
        self,
        transcript_id: str
    ) -> Transcript:
        """
        Get transcription result by ID.

        Args:
            transcript_id: Transcript ID from transcribe_audio

        Returns:
            Transcript object

        Raises:
            Exception: If retrieval fails
        """
        response = await self._make_request("GET", f"/transcript/{transcript_id}")
        return Transcript(**response)

    async def _poll_transcription(
        self,
        transcript_id: str,
        poll_interval: float = 1.0,
        timeout: int = 300
    ) -> Transcript:
        """
        Poll for transcription completion.

        Args:
            transcript_id: Transcript ID
            poll_interval: Seconds between polls
            timeout: Maximum seconds to wait

        Returns:
            Completed Transcript object

        Raises:
            Exception: If timeout or error occurs
        """
        start_time = asyncio.get_event_loop().time()

        while True:
            transcript = await self.get_transcription_result(transcript_id)

            if transcript.status == "completed":
                return transcript
            elif transcript.status == "error":
                raise Exception(f"Transcription failed: {transcript.status}")

            elapsed = asyncio.get_event_loop().time() - start_time
            if elapsed >= timeout:
                raise Exception(f"Transcription timeout after {timeout} seconds")

            await asyncio.sleep(poll_interval)

    async def delete_transcript(self, transcript_id: str) -> bool:
        """
        Delete a transcript.

        Args:
            transcript_id: Transcript ID

        Returns:
            True if deleted successfully
        """
        await self._make_request("DELETE", f"/transcript/{transcript_id}")
        return True


# ==================== Example Usage ====================

async def main():
    """Example usage of AssemblyAI client"""

    # Replace with your actual API key
    api_key = "your_assemblyai_api_key"

    async with AssemblyAIClient(api_key) as client:
        # Upload a local file
        # upload_result = await client.upload_media_file(file_path="audio.mp3")
        # print(f"Uploaded: {upload_result.upload_url}")

        # Or use a public URL
        audio_url = "https://example.com/audio.mp3"

        # Transcribe with speaker diarization
        transcript = await client.transcribe_audio(
            audio_url=audio_url,
            language_code="en_us",
            enable_speaker_diarization=True,
            speakers_expected=2,
            enable_auto_highlights=True,
            enable_summarization=True,
            poll=True
        )

        print(f"Transcription status: {transcript.status}")
        print(f"Language: {transcript.language_code}")
        print(f"Confidence: {transcript.confidence:.2f}")
        print(f"\nTranscript:\n{transcript.text}")

        if transcript.utterances:
            print(f"\nSpeakers detected: {transcript.speakers}")
            for utterance in transcript.utterances[:5]:  # Show first 5
                print(f"{utterance['speaker']}: {utterance['text'][:50]}...")


if __name__ == "__main__":
    asyncio.run(main())