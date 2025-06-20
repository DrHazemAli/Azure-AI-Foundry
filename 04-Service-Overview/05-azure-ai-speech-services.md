# 04-5: Azure AI Speech Services

## Overview

Azure AI Speech Services provides comprehensive speech-to-text, text-to-speech, and speech translation capabilities. These services enable applications to understand spoken language, generate natural-sounding speech, and translate speech across multiple languages in real-time.

## Learning Objectives

- Understand Azure AI Speech Services capabilities
- Implement speech-to-text and text-to-speech functionality
- Use real-time speech translation
- Build custom speech models for specific domains
- Integrate speech services with Azure AI Foundry projects

## What is Azure AI Speech Services?

Azure AI Speech Services includes:

- **Speech-to-Text**: Convert spoken language to written text
- **Text-to-Speech**: Generate natural-sounding speech from text
- **Speech Translation**: Real-time translation of spoken language
- **Speaker Recognition**: Identify and verify speakers by voice
- **Custom Speech**: Domain-specific speech recognition models

## Key Components

### Speech-to-Text
- Real-time speech recognition
- Batch transcription for audio files
- Custom speech models
- Multi-language support

### Text-to-Speech
- Neural voice synthesis
- Custom voice creation
- SSML support for speech control
- Multiple voice options and styles

### Speech Translation
- Real-time translation
- Multi-language support
- Conversation translation
- Audio output in target language

## Getting Started

### Basic Setup

```python
import azure.cognitiveservices.speech as speechsdk

# Initialize speech config
speech_config = speechsdk.SpeechConfig(
    subscription=speech_key,
    region=service_region
)

# Speech-to-Text
def recognize_speech():
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config,
        audio_config=audio_config
    )
    
    result = speech_recognizer.recognize_once_async().get()
    return result.text

# Text-to-Speech
def synthesize_speech(text):
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config,
        audio_config=audio_config
    )
    
    result = synthesizer.speak_text_async(text).get()
    return result
```

### Real-time Speech Translation

```python
def translate_speech():
    translation_config = speechsdk.translation.SpeechTranslationConfig(
        subscription=speech_key,
        region=service_region
    )
    
    # Set source and target languages
    translation_config.speech_recognition_language = "en-US"
    translation_config.add_target_language("es")
    translation_config.add_target_language("fr")
    
    recognizer = speechsdk.translation.TranslationRecognizer(
        translation_config=translation_config
    )
    
    result = recognizer.recognize_once_async().get()
    
    print(f"Original: {result.text}")
    for language, translation in result.translations.items():
        print(f"{language}: {translation}")
```

## Integration with Azure AI Foundry

```python
from azure.ai.projects import AIProjectClient

# Create speech-enabled agent
project_client = AIProjectClient(
    endpoint="your_project_endpoint",
    credential=DefaultAzureCredential()
)

agent = project_client.agents.create_agent(
    model="gpt-4o",
    name="Voice Assistant",
    instructions="You can process speech input and provide voice responses.",
    tools=[
        {
            "type": "function",
            "function": {
                "name": "process_speech",
                "description": "Process speech input and generate voice response"
            }
        }
    ]
)
```

## Common Use Cases

### Voice Assistants and Chatbots
- Voice-enabled customer service
- Interactive voice response (IVR) systems
- Smart home integration
- Virtual assistant applications

### Accessibility Solutions
- Text-to-speech for visually impaired users
- Speech-to-text for hearing impaired users
- Voice navigation systems
- Audio content accessibility

### Content Creation
- Podcast and audiobook narration
- Multi-language content localization
- Voice-over generation
- Interactive learning applications

### Business Applications
- Meeting transcription and analysis
- Call center automation
- Voice-controlled applications
- Multilingual customer support

## Custom Speech Models

### Training Custom Models

```python
from azure.cognitiveservices.speech import SpeechConfig, AudioConfig
from azure.cognitiveservices.speech.audio import AudioStreamFormat

# Create custom speech config
speech_config = SpeechConfig(
    subscription=speech_key,
    region=service_region
)

# Set custom model endpoint
speech_config.endpoint_id = "your-custom-model-id"

# Use custom model for recognition
recognizer = speechsdk.SpeechRecognizer(
    speech_config=speech_config,
    audio_config=AudioConfig(use_default_microphone=True)
)
```

### Custom Voice Creation

```python
# Custom voice synthesis
speech_config.speech_synthesis_voice_name = "your-custom-voice"

synthesizer = speechsdk.SpeechSynthesizer(
    speech_config=speech_config,
    audio_config=AudioConfig(use_default_speaker=True)
)

# Use SSML for advanced control
ssml_text = """
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
    <voice name="your-custom-voice">
        <prosody rate="0.9" pitch="high">
            Welcome to our application!
        </prosody>
    </voice>
</speak>
"""

result = synthesizer.speak_ssml_async(ssml_text).get()
```

## Advanced Features

### Conversation Transcription

```python
def transcribe_conversation():
    # Multi-speaker conversation transcription
    conversation_transcriber = speechsdk.transcription.ConversationTranscriber(
        speech_config=speech_config
    )
    
    # Subscribe to events
    def conversation_transcriber_recognition_canceled_cb(evt):
        print(f'Canceled: {evt}')
    
    def conversation_transcriber_session_started_cb(evt):
        print(f'Session started: {evt}')
    
    def conversation_transcriber_transcribed_cb(evt):
        print(f'Speaker {evt.result.speaker_id}: {evt.result.text}')
    
    conversation_transcriber.transcribed.connect(conversation_transcriber_transcribed_cb)
    conversation_transcriber.session_started.connect(conversation_transcriber_session_started_cb)
    conversation_transcriber.canceled.connect(conversation_transcriber_recognition_canceled_cb)
    
    conversation_transcriber.start_transcribing_async()
```

### Batch Transcription

```python
import requests
import json

def submit_batch_transcription(audio_url):
    transcription_definition = {
        "contentUrls": [audio_url],
        "properties": {
            "diarizationEnabled": True,
            "wordLevelTimestampsEnabled": True,
            "punctuationMode": "DictatedAndAutomatic"
        },
        "locale": "en-US",
        "displayName": "Batch Transcription"
    }
    
    headers = {
        'Ocp-Apim-Subscription-Key': speech_key,
        'Content-Type': 'application/json'
    }
    
    response = requests.post(
        f"https://{service_region}.api.cognitive.microsoft.com/speechtotext/v3.0/transcriptions",
        headers=headers,
        json=transcription_definition
    )
    
    return response.json()
```

## Best Practices

1. **Audio Quality Optimization**
   - Use high-quality audio input
   - Minimize background noise
   - Ensure proper microphone positioning

2. **Performance Optimization**
   - Implement audio buffering for real-time scenarios
   - Use batch processing for large audio files
   - Optimize sampling rates and formats

3. **Language and Localization**
   - Choose appropriate language models
   - Consider regional dialects and accents
   - Test with diverse speaker populations

4. **Security and Privacy**
   - Implement proper audio data handling
   - Follow data retention policies
   - Ensure compliance with privacy regulations

## Monitoring and Analytics

```python
import logging

# Set up logging for speech services
logging.basicConfig(level=logging.DEBUG)

def speech_recognition_with_logging():
    def recognized_cb(evt):
        logging.info(f"Recognition result: {evt.result.text}")
    
    def recognizing_cb(evt):
        logging.debug(f"Recognizing: {evt.result.text}")
    
    recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config,
        audio_config=AudioConfig(use_default_microphone=True)
    )
    
    recognizer.recognized.connect(recognized_cb)
    recognizer.recognizing.connect(recognizing_cb)
    
    recognizer.start_continuous_recognition()
```

## Conclusion

Azure AI Speech Services provides comprehensive speech processing capabilities that enable natural voice interactions in applications. Integration with Azure AI Foundry allows for seamless incorporation of speech capabilities into AI solutions.

Key takeaways:
- **Comprehensive Speech**: Full range of speech processing capabilities
- **Real-time Processing**: Low-latency speech recognition and synthesis
- **Custom Models**: Train domain-specific speech models
- **Multi-language Support**: Global language coverage
- **Enterprise Ready**: Scalable and secure speech services

---

*This lesson is part of the Azure AI Foundry Zero-to-Hero Guide.* 