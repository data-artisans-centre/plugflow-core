import json
from typing import Optional, Dict, Any
from googletrans import Translator
from log import logger
from core.base import AgentBase

class TranslatorAgent(AgentBase):
    """Agent to translate text between languages."""
    def __init__(self):
        """
        Initialize the TranslatorAgent.
        """
        super().__init__()
        self.translator = Translator()

    def execute(self, **kwargs):
        """
        Translate text to the target language.

        Args:
            **kwargs: Keyword arguments including 'text' and 'target_language'.

        Returns:
            dict: A dictionary containing translation details.

        Raises:
            ValueError: If translation fails or invalid input is provided.
        """
        try:
            # Extract parameters
            text = kwargs.get('text', '')
            target_language = kwargs.get('target_language', 'en')

            # Validate input
            if not text:
                raise ValueError("Text cannot be empty.")

            # Perform translation
            translation = self.translator.translate(text, dest=target_language)

            # Prepare translation result
            translation_result = {
                'original_text': text,
                'translated_text': translation.text,
                'source_language': translation.src,
                'target_language': translation.dest
            }

            # Convert to JSON for logging/display
            translation_json = json.dumps(translation_result)
            print(translation_json)

            return translation_result

        except Exception as e:
            # Log and raise error
            print(f"Translation error: {e}")
            raise ValueError(f"Failed to translate text. {str(e)}") from e

    def health_check(self) -> Dict[str, str]:
        """
        Perform a health check on the translation service.

        Returns:
            Dict with service health status.
        """
        try:
            logger.info("Performing translator health check...")
            
            # Test translation with a simple string
            test_translation = self.translator.translate("hello", dest='es')
            
            if test_translation and test_translation.text:
                logger.info("Translation service health check passed.")
                return {
                    "status": "healthy", 
                    "message": "Translation service is operational"
                }
            
            raise Exception("Translation test failed")
        
        except Exception as e:
            logger.error(f"Translator health check failed: {e}")
            return {
                "status": "unhealthy", 
                "message": str(e)
            }

    def list_supported_languages(self) -> Dict[str, str]:
        """
        List supported languages with their codes.

        Returns:
            Dict of language names and their corresponding codes.
        """
        return {
            'English': 'en',
            'Spanish': 'es',
            'French': 'fr',
            'German': 'de',
            'Chinese': 'zh-cn',
            'Japanese': 'ja',
            'Arabic': 'ar',
            'Russian': 'ru',
            'Portuguese': 'pt',
            'Italian': 'it'
        }