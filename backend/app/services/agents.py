"""
Agent services: IntentAgent, FAQAgent (RAG), TicketAgent
These are modular placeholders to integrate LangChain/LangGraph.
"""
from collections import Counter
from functools import lru_cache
from math import log
from pathlib import Path
import re

from .. import crud
from ..core.config import settings

try:
    from openai import OpenAI
except Exception:
    OpenAI = None

try:
    import docx2txt
except ImportError:
    docx2txt = None

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None


_STOP_WORDS = {
    'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'company', 'for', 'from', 'how',
    'i', 'in', 'is', 'it', 'of', 'on', 'or', 'our', 'the', 'to', 'us',
    'policy', 'support', 'we', 'what', 'when', 'where', 'which', 'who', 'why', 'with', 'you',
}


def _tokenize(text: str) -> list[str]:
    tokens: list[str] = []
    for token in re.findall(r'[a-z0-9]+', text.lower()):
        if token.endswith('ies') and len(token) > 4:
            token = f'{token[:-3]}y'
        elif token.endswith(('ing', 'ed', 'es', 's')) and len(token) > 4:
            token = token[:-3] if token.endswith('ing') else token[:-2] if token.endswith(('ed', 'es')) else token[:-1]
            if token.endswith('e'):
                token = token[:-1]
        elif token.endswith('e') and len(token) > 4:
            token = token[:-1]
        if len(token) > 2 and token not in _STOP_WORDS:
            tokens.append(token)
    return tokens


def _split_into_chunks(text: str, max_chars: int = 400) -> list[str]:
    paragraphs = [re.sub(r'\s+', ' ', part).strip() for part in text.splitlines()]
    paragraphs = [part for part in paragraphs if part]
    chunks: list[str] = []
    current = ''

    for paragraph in paragraphs:
        while len(paragraph) > max_chars:
            if current:
                chunks.append(current)
                current = ''
            chunks.append(paragraph[:max_chars])
            paragraph = paragraph[max_chars:]
        candidate = f'{current}\n{paragraph}'.strip() if current else paragraph
        if len(candidate) > max_chars and current:
            chunks.append(current)
            current = paragraph
        else:
            current = candidate

    if current:
        chunks.append(current)
    return chunks


@lru_cache(maxsize=1)
def _knowledge_chunks() -> tuple[tuple[str, str], ...]:
    """Load local KB files into searchable text chunks once per server process."""
    knowledge_dir = Path(__file__).resolve().parents[2] / 'knowledge_base'
    loaded: list[tuple[str, str]] = []

    for path in sorted(knowledge_dir.rglob('*')):
        if not path.is_file() or path.name.lower() == 'readme.md':
            continue
        suffix = path.suffix.lower()
        try:
            if suffix == '.docx' and docx2txt is not None:
                text = docx2txt.process(str(path))
            elif suffix in {'.txt', '.md'}:
                text = path.read_text(encoding='utf-8', errors='replace')
            elif suffix == '.pdf' and PdfReader is not None:
                text = '\n'.join(page.extract_text() or '' for page in PdfReader(str(path)).pages)
            else:
                continue
        except Exception:
            continue

        loaded.extend((path.name, chunk) for chunk in _split_into_chunks(text))
    return tuple(loaded)


def _retrieve_context(query: str, limit: int = 3) -> list[tuple[str, str]]:
    chunks = _knowledge_chunks()
    query_terms = Counter(_tokenize(query))
    if not chunks or not query_terms:
        return []

    tokenized_chunks = [Counter(_tokenize(text)) for _, text in chunks]
    document_frequency = Counter(
        term for frequencies in tokenized_chunks for term in frequencies
    )
    total_chunks = len(chunks)
    scored: list[tuple[float, int]] = []

    for index, frequencies in enumerate(tokenized_chunks):
        matched_terms = query_terms.keys() & frequencies.keys()
        if len(matched_terms) < min(2, len(query_terms)):
            continue
        score = sum(
            query_count
            * log(1 + (total_chunks - document_frequency[term] + 0.5) / (document_frequency[term] + 0.5))
            * frequencies.get(term, 0)
            for term, query_count in query_terms.items()
        )
        if score > 0:
            scored.append((score, index))

    scored.sort(reverse=True)
    return [chunks[index] for _, index in scored[:limit]]


class IntentAgent:
    @staticmethod
    def route(message: str) -> str:
        text = message.lower()
        explicit_ticket_request = any(
            phrase in text
            for phrase in (
                'create a ticket', 'create ticket', 'open a ticket', 'open ticket',
                'raise a ticket', 'billing support ticket', 'support ticket',
            )
        )
        human_assistance_request = any(
            phrase in text
            for phrase in (
                'speak to a human', 'talk to a human', 'human agent', 'live agent',
                'real person', 'connect me to support', 'please connect me to',
                'have someone contact me', 'talk to an agent', 'speak with an agent',
            )
        )
        unresolved_problem = any(
            phrase in text
            for phrase in (
                "can't resolve", 'cannot resolve', 'unable to resolve',
                'still not working', 'still does not work', "still doesn't work",
                'still not fixed', 'not resolved', 'issue persists', 'problem persists',
                'tried everything', 'already tried', 'nothing has worked',
            )
        )
        billing_dispute = any(
            phrase in text
            for phrase in (
                'charged twice', 'charged me twice', 'double charged',
                'duplicate charge', 'charged two times', 'refund dispute',
                'disputed charge', 'unauthorized charge', 'wrong amount charged',
            )
        )
        if explicit_ticket_request or human_assistance_request or unresolved_problem or billing_dispute:
            return 'ticket'

        # Keep answerable questions with the FAQ agent; escalate when the local
        # knowledge base has no relevant passage to answer from.
        return 'faq' if _retrieve_context(message) else 'ticket'


class FAQAgent:
    def answer(self, query: str) -> str:
        passages = _retrieve_context(query)
        if not passages:
            return "I couldn't find that information in the company knowledge base. Please contact support for help."

        context = '\n\n'.join(content for _, content in passages)
        provider = settings.llm_provider
        api_key = settings.groq_api_key if provider == 'groq' else settings.openai_api_key
        if api_key and OpenAI is not None:
            try:
                client_kwargs = {'api_key': api_key}
                if provider == 'groq':
                    client_kwargs['base_url'] = settings.groq_base_url
                client = OpenAI(**client_kwargs)
                model_name = settings.groq_model if provider == 'groq' else 'gpt-4o-mini'
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {
                            'role': 'system',
                            'content': (
                                'You are a customer-support FAQ assistant. Answer only from the supplied '
                                'company knowledge-base excerpts. Do not use outside knowledge or invent '
                                'policy details. If the excerpts do not answer the question, say that the '
                                'knowledge base does not specify the answer. If an excerpt is labeled '
                                'sample or demo, clearly tell the user it is not official company policy. '
                                'Answer directly using the most relevant excerpts. Do not include source '
                                'filenames, citations, or a source section in the user-facing answer.'
                            ),
                        },
                        {
                            'role': 'user',
                            'content': f'Question: {query}\n\nKnowledge-base excerpts:\n{context}',
                        },
                    ],
                    temperature=0.2,
                )
                content = response.choices[0].message.content
                if content:
                    return content.strip()
            except Exception:
                pass

        excerpts = '\n'.join(content for _, content in passages)
        return f"According to the company knowledge base:\n{excerpts}"


class TicketAgent:
    def __init__(self, db_session):
        self.db = db_session

    def create_ticket(self, title: str, description: str | None = None):
        return crud.create_ticket(self.db, title=title, description=description)
