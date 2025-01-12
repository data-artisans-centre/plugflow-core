import json
from typing import Dict, Any, Union, Tuple
from core.base import AgentBase
from log import logger
import pypdf
import pyttsx3
import io

class PdfToAudioAgent(AgentBase):
    """Agent to convert PDF content to audio with direct playback."""

    def __init__(self):
        """Initialize the PdfToAudioAgent."""
        logger.info("PdfToAudioAgent initialized.")
        self.engine = pyttsx3.init()
        
    def read_pdf(self, pdf_path: str) -> str:
        """
        Extracts text from a PDF file.
        """
        try:
            with open(pdf_path, "rb") as file:
                reader = pypdf.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
                logger.info("PDF text successfully extracted.")
                return text
        except Exception as e:
            logger.error(f"Error reading PDF: {e}")
            raise

    def play_audio(self, text: str) -> None:
        """
        Converts text to speech and plays it directly.
        """
        try:
            # Configure voice settings
            voices = self.engine.getProperty('voices')
            self.engine.setProperty('voice', voices[1].id)  # Index 1 -> a female voice
            self.engine.setProperty('rate', 150)  # Speed of speech
            self.engine.setProperty('volume', 0.9)  # Volume level
            
            # Play the audio
            self.engine.say(text)
            self.engine.runAndWait()
            
            logger.info("Audio played successfully")
        except Exception as e:
            logger.error(f"Error playing audio: {e}")
            raise

    def execute(self, **kwargs) -> Dict[str, Any]:
        try:
            pdf_path = kwargs.get("pdf_path")
            if not pdf_path:
                raise ValueError("'pdf_path' must be provided.")

            # Extract text from PDF
            text = self.read_pdf(pdf_path)
            
            # Play the audio directly
            self.play_audio(text)
            
            return {
                "status": "success", 
                "message": "PDF text has been converted to speech and played",
                "full_text": text
            }
        except Exception as e:
            logger.error(f"Error during PDF to audio conversion: {e}")
            return {"status": "error", "message": str(e)}

    def health_check(self) -> Dict[str, str]:
        """
        Perform a health check on the PDF to audio conversion process.
        """
        try:
            logger.info("Performing health check...")
            test_text = "System is operational"
            self.engine.say(test_text)
            self.engine.runAndWait()
            
            logger.info("Health check passed.")
            return {
                "status": "healthy",
                "message": "PDF to audio conversion service is operational",
            }
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {
                "status": "unhealthy",
                "message": str(e),
            }