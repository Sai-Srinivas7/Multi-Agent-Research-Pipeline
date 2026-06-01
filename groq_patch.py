"""Compatibility shim for running CrewAI against Groq.

CrewAI injects a ``cache_breakpoint`` field into the outgoing message
dictionaries. Groq's API strictly rejects any unknown keys, which raises an
error before the request completes. This module wraps ``LLM.call`` and strips
that key from each message just before the request is sent.

Import this module once, before any ``LLM`` instance makes a call.
"""
from crewai import LLM

_original_call = LLM.call


def _patched_call(self, messages, *args, **kwargs):
    if isinstance(messages, list):
        for msg in messages:
            if isinstance(msg, dict):
                msg.pop("cache_breakpoint", None)
    return _original_call(self, messages, *args, **kwargs)


LLM.call = _patched_call
