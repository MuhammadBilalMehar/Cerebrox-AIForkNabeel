"""
Thin wrapper around the OpenAI API.

Kept isolated from the rest of the codebase (per the FYP scope's "keep AI
code modular so the provider can be swapped later" requirement) so that
notes_generator / mcq_generator / recommendation_generator never import the
`openai` package directly.
"""
import json
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


class AIUnavailableError(Exception):
    """Raised when no AI provider is configured or the call fails."""


def is_configured() -> bool:
    api_key = (settings.OPENAI_API_KEY or '').strip()
    return bool(api_key)


def _safe_error_details(exc: Exception) -> str:
    status_code = getattr(exc, 'status_code', None)
    request_id = getattr(exc, 'request_id', None)
    details = [f'type={type(exc).__name__}', f'message={exc}']
    if status_code is not None:
        details.append(f'http_status={status_code}')
    if request_id:
        details.append(f'request_id={request_id}')
    return ', '.join(details)


def chat_json(system_prompt: str, user_prompt: str) -> dict:
    """
    Send a prompt pair to the configured model and parse the JSON response.
    Raises AIUnavailableError when the backend is not configured or the API
    call returns an unusable result.
    """
    api_key = (settings.OPENAI_API_KEY or '').strip()
    if not api_key:
        logger.error(
            'OpenAI request not started: API key detected=False, model=%s. '
            'Set OPENAI_API_KEY in the backend .env file.',
            settings.OPENAI_MODEL,
        )
        raise AIUnavailableError('OpenAI API key is missing. Set OPENAI_API_KEY in the backend .env file.')

    try:
        from openai import OpenAI
        logger.info(
            'Initializing OpenAI client: API key detected=True, model=%s, sdk=1.30.5-compatible',
            settings.OPENAI_MODEL,
        )
        client = OpenAI(api_key=api_key)
        logger.info('Sending OpenAI chat completion request: model=%s', settings.OPENAI_MODEL)
        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_prompt},
            ],
            response_format={'type': 'json_object'},
            temperature=0.5,
        )
        logger.info(
            'OpenAI response received: model=%s, request_id=%s, choices=%s',
            getattr(response, 'model', settings.OPENAI_MODEL),
            getattr(response, '_request_id', 'unknown'),
            len(getattr(response, 'choices', []) or []),
        )
        if not getattr(response, 'choices', None):
            raise AIUnavailableError('OpenAI returned no choices in the response.')
        raw = response.choices[0].message.content
        if raw is None or not str(raw).strip():
            raise AIUnavailableError('OpenAI returned an empty response for the notes request.')
        parsed = json.loads(raw)
        if not isinstance(parsed, dict):
            raise AIUnavailableError('OpenAI returned a non-object payload for the notes request.')
        return parsed
    except AIUnavailableError:
        raise
    except Exception as exc:  # noqa: BLE001 - any provider/parsing failure funnels here
        logger.exception('OpenAI request failed: %s', _safe_error_details(exc))
        raise AIUnavailableError(f'OpenAI request failed: {_safe_error_details(exc)}') from exc
