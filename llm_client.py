"""
LLM Client — Smart Model Routing
Routes high-volume simulation calls to the default (cheap) model
and intelligence-heavy tasks (ontology, reports) to the smart model.
"""

from openai import OpenAI
from ..config import config
from .logger import setup_logger

logger = setup_logger(__name__)

# Task types that use the smart model when configured
SMART_TASKS = {"ontology_extraction", "report_generation", "graph_reasoning"}


def get_client(use_smart: bool = False) -> tuple[OpenAI, str]:
    """
    Returns (client, model_name) for the appropriate tier.
    Falls back to default model if smart model is not configured.
    """
    if use_smart and config.SMART_MODEL_NAME:
        client = OpenAI(
            api_key=config.SMART_API_KEY or config.LLM_API_KEY,
            base_url=config.SMART_BASE_URL or config.LLM_BASE_URL,
        )
        return client, config.SMART_MODEL_NAME

    client = OpenAI(
        api_key=config.LLM_API_KEY,
        base_url=config.LLM_BASE_URL,
    )
    return client, config.LLM_MODEL_NAME


def complete(
    messages: list[dict],
    task_type: str = "default",
    temperature: float = 0.7,
    max_tokens: int = 2000,
) -> str:
    """
    Send a chat completion request.
    Automatically routes to smart model for designated task types.

    Args:
        messages: OpenAI-format message list
        task_type: Used to determine model routing (see SMART_TASKS)
        temperature: Sampling temperature
        max_tokens: Maximum response tokens

    Returns:
        Response text as a string
    """
    use_smart = task_type in SMART_TASKS
    client, model = get_client(use_smart=use_smart)

    logger.debug(f"LLM call: task={task_type} model={model} messages={len(messages)}")

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    return response.choices[0].message.content


def complete_json(
    messages: list[dict],
    task_type: str = "default",
    temperature: float = 0.2,
    max_tokens: int = 2000,
) -> str:
    """
    Like complete() but requests JSON output mode.
    Use for structured data extraction (ontology, profiles, etc.)
    """
    use_smart = task_type in SMART_TASKS
    client, model = get_client(use_smart=use_smart)

    logger.debug(f"LLM JSON call: task={task_type} model={model}")

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        response_format={"type": "json_object"},
    )

    return response.choices[0].message.content
