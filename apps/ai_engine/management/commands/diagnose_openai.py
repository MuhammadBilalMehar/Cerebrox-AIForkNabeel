from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from apps.ai_engine.openai_client import AIUnavailableError, chat_json


class Command(BaseCommand):
    help = 'Run a safe, backend-side OpenAI connectivity and response-parsing check.'

    def handle(self, *args, **options):
        key_detected = bool((settings.OPENAI_API_KEY or '').strip())
        self.stdout.write(f'OPENAI_API_KEY detected: {key_detected}')
        self.stdout.write(f'OPENAI_MODEL: {settings.OPENAI_MODEL}')
        if not key_detected:
            raise CommandError('OPENAI_API_KEY is missing. No OpenAI request was sent.')

        try:
            result = chat_json(
                'You are a concise assistant. Return a JSON object with one key: answer.',
                'Explain Machine Learning in exactly 3 sentences. Put the explanation in answer.',
            )
        except AIUnavailableError as exc:
            raise CommandError(str(exc)) from exc

        answer = result.get('answer')
        if not isinstance(answer, str) or not answer.strip():
            raise CommandError('OpenAI returned JSON, but the answer field was empty or invalid.')

        self.stdout.write(self.style.SUCCESS('OpenAI request succeeded and response parsing succeeded.'))
        self.stdout.write(answer)