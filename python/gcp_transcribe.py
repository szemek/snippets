from google.cloud import storage
from google.cloud import speech_v1p1beta1 as speech

storage_client = storage.Client()
bucket = "bucket-name"
blobs = list(storage_client.list_blobs(bucket_or_name=bucket, prefix="prefix/"))

operations = []

for blob in blobs:
    season, episode = blob.name.split("/")
    gcs_uri = f"gs://{bucket}/{blob.name}"

    speech_client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=gcs_uri)

    output_config = speech.TranscriptOutputConfig(gcs_uri=f"gs://{bucket}/transcripts/{episode}.json")

    config = speech.RecognitionConfig(
        encoding="MP3",
        sample_rate_hertz=44100,
        language_code="pl-PL",
        enable_word_time_offsets = True,
    )

    request = speech.LongRunningRecognizeRequest(
        audio=audio, config=config, output_config=output_config
    )
    operation = speech_client.long_running_recognize(request=request)

    operations.append(operation)
