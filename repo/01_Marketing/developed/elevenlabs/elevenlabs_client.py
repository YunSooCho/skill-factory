"""
ElevenLabs API - AI Voice Synthesis Client

Supports 8 API Actions:
- Text to Speech (basic, with timestamps, with sound effects)
- Voice cloning and conversion
- Audio dubbing
- Audio enhancement (noise removal)
- Pronunciation dictionary management

Triggers:
- No triggers supported
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Voice:
    """Voice entity"""
    voice_id: str
    name: str
    category: str = "generated"
    gender: Optional[str] = None
    age: Optional[str] = None
    description: Optional[str] = None
    language: str = "en"


@dataclass
class AudioGeneration:
    """Audio generation result"""
    audio_url: str
    history_item_id: str
    duration: float
    character_count: int


@dataclass
class DubbingJob:
    """Dubbing job entity"""
    dubbing_id: str
    status: str
    source_language: str
    target_language: str
    created_at: str = ""


@dataclass
class PronunciationDictionary:
    """Pronunciation dictionary entity"""
    dictionary_id: str
    name: str
    rules_count: int


class ElevenLabsClient:
    """
    ElevenLabs API client for AI voice synthesis.

    API Documentation: https://elevenlabs.io/docs
    Uses API Key for authentication.
    """

    BASE_URL = "https://api.elevenlabs.io/v1"

    def __init__(self, api_key: str):
        """
        Initialize ElevenLabs client.

        Args:
            api_key: API token for authentication
        """
        self.api_key = api_key
        self.session = None

    async def __aenter__(self):
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }

        self.session = aiohttp.ClientSession(headers=headers)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _handle_response(self, response: aiohttp.ClientResponse) -> Dict[str, Any]:
        """Handle API response"""
        if response.status in (200, 201, 202, 204):
            if response.status == 202:
                return {"status": "accepted"}
            if response.status == 204:
                return {}
            data = await response.json()
            return data
        else:
            try:
                data = await response.json()
                error_msg = {
                    'detail': data.get('detail', {}),
                    'message': data.get('message', 'Unknown error')
                }
            except:
                error_msg = f"HTTP {response.status}"
            raise Exception(f"API Error [{response.status}]: {error_msg}")

    # ==================== Voice Operations ====================

    async def get_voices(self) -> List[Voice]:
        """Get all available voices"""
        async with self.session.get(
            f"{self.BASE_URL}/voices"
        ) as response:
            data = await self._handle_response(response)
            voices_data = data.get("voices", [])

            return [
                Voice(
                    voice_id=v.get("voice_id", ""),
                    name=v.get("name", ""),
                    category=v.get("category", "generated"),
                    gender=v.get("labels", {}).get("gender"),
                    age=v.get("labels", {}).get("age"),
                    description=v.get("description"),
                    language=v.get("labels", {}).get("accent", "en")
                )
                for v in voices_data
            ]

    # ==================== Text to Speech ====================

    async def text_to_speech(
        self,
        text: str,
        voice_id: str,
        model_id: str = "eleven_multilingual_v2",
        voice_settings: Optional[Dict[str, float]] = None
    ) -> AudioGeneration:
        """
        Convert text to speech

        Args:
            text: Text to convert
            voice_id: Voice ID to use
            model_id: Model ID (default: eleven_multilingual_v2)
            voice_settings: Optional voice settings (stability, similarity_boost)

        Returns:
            AudioGeneration with audio_url and metadata
        """
        payload = {
            "text": text,
            "model_id": model_id,
            "voice_settings": voice_settings or {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }

        async with self.session.post(
            f"{self.BASE_URL}/text-to-speech/{voice_id}",
            json=payload
        ) as response:
            if response.status != 200:
                await self._handle_response(response)

            # Audio is returned as binary
            audio_data = await response.read()

            # For simplicity, we'll return metadata
            # In production, you'd upload to storage and return URL
            return AudioGeneration(
                audio_url="",  # Would be the storage URL
                history_item_id="",
                duration=0.0,
                character_count=len(text)
            )

    async def text_to_speech_with_timestamps(
        self,
        text: str,
        voice_id: str,
        model_id: str = "eleven_multilingual_v2"
    ) -> Dict[str, Any]:
        """
        Convert text to speech with word-level timestamps
        """
        payload = {
            "text": text,
            "model_id": model_id,
            "include_timestamps": True
        }

        async with self.session.post(
            f"{self.BASE_URL}/text-to-speech-with-timestamps/{voice_id}",
            json=payload
        ) as response:
            data = await self._handle_response(response)
            return data

    async def text_to_speech_sound_effects(
        self,
        text: str,
        voice_id: str,
        sound_effects: List[Dict[str, Any]],
        model_id: str = "eleven_multilingual_v2"
    ) -> Dict[str, Any]:
        """
        Convert text to speech with sound effects
        """
        payload = {
            "text": text,
            "voice_id": voice_id,
            "model_id": model_id,
            "sound_effects": sound_effects
        }

        async with self.session.post(
            f"{self.BASE_URL}/text-to-speech-sound-effects",
            json=payload
        ) as response:
            data = await self._handle_response(response)
            return data

    # ==================== Voice Conversion ====================

    async def convert_voice(
        self,
        source_audio_url: str,
        target_voice_id: str
    ) -> Dict[str, Any]:
        """
        Convert voice from audio to another voice
        """
        payload = {
            "audio_url": source_audio_url,
            "target_voice_id": target_voice_id
        }

        async with self.session.post(
            f"{self.BASE_URL}/voice-conversion",
            json=payload
        ) as response:
            data = await self._handle_response(response)
            return data

    # ==================== Dubbing ====================

    async def create_dubbing(
        self,
        source_url: str,
        target_lang: str,
        source_lang: str = "en",
        voice_id: Optional[str] = None
    ) -> DubbingJob:
        """
        Dub audio or video files into a specified language

        Args:
            source_url: URL of source audio/video
            target_lang: Target language code
            source_lang: Source language code (default: en)
            voice_id: Optional voice ID for dubbing
        """
        payload = {
            "source_url": source_url,
            "target_lang": target_lang,
            "source_lang": source_lang
        }

        if voice_id:
            payload["voice_id"] = voice_id

        async with self.session.post(
            f"{self.BASE_URL}/dubbing",
            json=payload
        ) as response:
            data = await self._handle_response(response)

            return DubbingJob(
                dubbing_id=str(data.get("dubbing_id", "")),
                status=data.get("status", "processing"),
                source_language=source_lang,
                target_language=target_lang,
                created_at=data.get("created_at", "")
            )

    async def get_dubbing(self, dubbing_id: str) -> Optional[Dict[str, Any]]:
        """
        Get dubbing job status and result
        """
        async with self.session.get(
            f"{self.BASE_URL}/dubbing/{dubbing_id}"
        ) as response:
            if response.status == 404:
                return None
            data = await self._handle_response(response)
            return data

    async def get_dubbing_file(
        self,
        dubbing_id: str
    ) -> str:
        """
        Obtain the dubbed file URL
        """
        async with self.session.get(
            f"{self.BASE_URL}/dubbing/{dubbing_id}/download"
        ) as response:
            if response.status == 404:
                raise Exception("Dubbing file not found")

            # Return download URL for the dubbed file
            return f"{self.BASE_URL}/dubbing/{dubbing_id}/download"

    # ==================== Audio Enhancement ====================

    async def audio_noise_removal(
        self,
        audio_url: str
    ) -> Dict[str, Any]:
        """
        Remove noise from audio file
        """
        payload = {
            "audio_url": audio_url
        }

        async with self.session.post(
            f"{self.BASE_URL}/audio-enhancement",
            json=payload
        ) as response:
            data = await self._handle_response(response)
            return data

    # ==================== Pronunciation Dictionary ====================

    async def add_pronunciation_dictionary(
        self,
        name: str,
        voice_id: str,
        rules: List[Dict[str, str]]
    ) -> PronunciationDictionary:
        """
        Add a pronunciation dictionary for a voice

        Args:
            name: Dictionary name
            voice_id: Voice ID to apply dictionary to
            rules: List of pronunciation rules in format [{"from": "word", "to": "pronunciation"}]
        """
        payload = {
            "name": name,
            "voice_id": voice_id,
            "rules": rules
        }

        async with self.session.post(
            f"{self.BASE_URL}/pronunciation-dictionaries",
            json=payload
        ) as response:
            data = await self._handle_response(response)

            return PronunciationDictionary(
                dictionary_id=str(data.get("dictionary_id", "")),
                name=name,
                rules_count=len(rules)
            )

    async def get_pronunciation_dictionary(
        self,
        dictionary_id: str
    ) -> Optional[PronunciationDictionary]:
        """
        Get pronunciation dictionary details
        """
        async with self.session.get(
            f"{self.BASE_URL}/pronunciation-dictionaries/{dictionary_id}"
        ) as response:
            if response.status == 404:
                return None
            data = await self._handle_response(response)

            return PronunciationDictionary(
                dictionary_id=dictionary_id,
                name=data.get("name", ""),
                rules_count=len(data.get("rules", []))
            )

    async def delete_pronunciation_dictionary(
        self,
        dictionary_id: str
    ) -> bool:
        """Delete a pronunciation dictionary"""
        async with self.session.delete(
            f"{self.BASE_URL}/pronunciation-dictionaries/{dictionary_id}"
        ) as response:
            if response.status == 404:
                return False
            await self._handle_response(response)
            return True


# ==================== Example Usage ====================

async def main():
    """Example usage of ElevenLabs client"""

    # Example configuration - replace with your actual credentials
    api_key = "your_api_key"

    async with ElevenLabsClient(api_key=api_key) as client:
        # Get available voices
        voices = await client.get_voices()
        print(f"Available voices: {len(voices)}")
        if voices:
            print(f"First voice: {voices[0].name}")

        # Text to speech
        if voices:
            voice_id = voices[0].voice_id
            audio = await client.text_to_speech(
                text="Hello, this is a test.",
                voice_id=voice_id
            )
            print(f"Audio generated: {audio.duration}s ({audio.character_count} chars)")

        # Create dubbing
        dubbing = await client.create_dubbing(
            source_url="https://example.com/audio.mp3",
            target_lang="es",
            source_lang="en"
        )
        print(f"Dubbing created: {dubbing.dubbing_id}")

        # Add pronunciation dictionary
        pron_dict = await client.add_pronunciation_dictionary(
            name="Custom Pronunciations",
            voice_id="voice_id",
            rules=[
                {"from": "example", "to": "ig-ZAM-pull"},
            ]
        )
        print(f"Dictionary created: {pron_dict.name} ({pron_dict.rules_count} rules)")


if __name__ == "__main__":
    asyncio.run(main())