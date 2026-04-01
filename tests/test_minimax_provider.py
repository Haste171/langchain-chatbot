"""Unit tests for MiniMax provider integration in BaseHandler."""
import os
import sys
import types
import unittest
from unittest.mock import MagicMock, patch

# ---------------------------------------------------------------------------
# Minimal stubs so we can import handlers.base without real dependencies
# ---------------------------------------------------------------------------

def _make_stub_module(name):
    mod = types.ModuleType(name)
    sys.modules[name] = mod
    return mod


def _setup_stubs():
    # pinecone
    pc = _make_stub_module("pinecone")
    pc.init = MagicMock()
    exc_mod = _make_stub_module("pinecone.core")
    exc_mod2 = _make_stub_module("pinecone.core.client")
    exc_mod3 = _make_stub_module("pinecone.core.client.exceptions")
    exc_mod3.ApiException = Exception

    # langchain_openai
    lo = _make_stub_module("langchain_openai")
    lo.embeddings = _make_stub_module("langchain_openai.embeddings")
    lo.chat_models = _make_stub_module("langchain_openai.chat_models")

    class _FakeChatOpenAI:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)

    lo.chat_models.ChatOpenAI = _FakeChatOpenAI
    _make_stub_module("langchain_openai.embeddings").OpenAIEmbeddings = MagicMock

    sys.modules["langchain_openai"] = lo
    sys.modules["langchain_openai.embeddings"] = lo.embeddings
    sys.modules["langchain_openai.chat_models"] = lo.chat_models

    # langchain_anthropic
    la = _make_stub_module("langchain_anthropic")
    la.ChatAnthropic = MagicMock

    # langchain.chains / text_splitter
    lc = _make_stub_module("langchain")
    lc.chains = _make_stub_module("langchain.chains")
    lc.chains.ConversationalRetrievalChain = MagicMock
    lc.text_splitter = _make_stub_module("langchain.text_splitter")
    for cls in [
        "TokenTextSplitter", "TextSplitter", "Tokenizer", "Language",
        "RecursiveCharacterTextSplitter", "RecursiveJsonSplitter",
        "LatexTextSplitter", "PythonCodeTextSplitter", "KonlpyTextSplitter",
        "SpacyTextSplitter", "NLTKTextSplitter",
        "SentenceTransformersTokenTextSplitter", "ElementType", "HeaderType",
        "LineType", "HTMLHeaderTextSplitter", "MarkdownHeaderTextSplitter",
        "MarkdownTextSplitter", "CharacterTextSplitter",
    ]:
        setattr(lc.text_splitter, cls, MagicMock)

    # langchain_community
    lcc = _make_stub_module("langchain_community")
    lcc.vectorstores = _make_stub_module("langchain_community.vectorstores")
    lcc.vectorstores.pinecone = _make_stub_module("langchain_community.vectorstores.pinecone")
    lcc.vectorstores.pinecone.Pinecone = MagicMock
    lcc.document_loaders = _make_stub_module("langchain_community.document_loaders")
    lcc.document_loaders.TextLoader = MagicMock
    lcc.document_loaders.PyMuPDFLoader = MagicMock
    lcc.document_loaders.Docx2txtLoader = MagicMock

    # fastapi
    fa = _make_stub_module("fastapi")
    fa.UploadFile = MagicMock
    fa.HTTPException = Exception

    # dotenv
    de = _make_stub_module("dotenv")
    de.load_dotenv = MagicMock

    # utils.alerts
    ua = _make_stub_module("utils")
    ua_alerts = _make_stub_module("utils.alerts")
    ua_alerts.alert_exception = MagicMock
    ua_alerts.alert_info = MagicMock


_setup_stubs()

# Now safe to import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from handlers.base import BaseHandler  # noqa: E402


MINIMAX_MODELS = [
    "MiniMax-M2.7",
    "MiniMax-M2.7-highspeed",
    "MiniMax-M2.5",
    "MiniMax-M2.5-highspeed",
]


class TestMinimaxInLlmMap(unittest.TestCase):
    """All MiniMax models are present in llm_map."""

    @patch.dict(os.environ, {"MINIMAX_API_KEY": "test-key", "OPENAI_API_KEY": "oai-key"})
    def setUp(self):
        self.handler = BaseHandler(chat_model="MiniMax-M2.7", temperature=0.7)

    def test_all_minimax_models_registered(self):
        for model in MINIMAX_MODELS:
            self.assertIn(model, self.handler.llm_map, f"{model} missing from llm_map")

    def test_minimax_factory_returns_callable(self):
        for model in MINIMAX_MODELS:
            self.assertTrue(callable(self.handler.llm_map[model]))


class TestMinimaxApiConfig(unittest.TestCase):
    """MiniMax entries use the correct base URL and API key env var."""

    @patch.dict(os.environ, {"MINIMAX_API_KEY": "mm-secret", "OPENAI_API_KEY": ""})
    def _get_llm(self, model, temperature=0.5):
        handler = BaseHandler(chat_model=model, temperature=temperature)
        return handler.llm_map[model]()

    def test_base_url(self):
        for model in MINIMAX_MODELS:
            llm = self._get_llm(model)
            self.assertEqual(
                llm.openai_api_base,
                "https://api.minimax.io/v1",
                f"{model}: wrong base URL",
            )

    def test_api_key_from_env(self):
        for model in MINIMAX_MODELS:
            llm = self._get_llm(model)
            self.assertEqual(llm.openai_api_key, "mm-secret")

    def test_model_name_preserved(self):
        for model in MINIMAX_MODELS:
            llm = self._get_llm(model)
            self.assertEqual(llm.model, model)


class TestTemperatureClamping(unittest.TestCase):
    """Temperature must be clamped to (0.0, 1.0] for MiniMax."""

    @patch.dict(os.environ, {"MINIMAX_API_KEY": "k", "OPENAI_API_KEY": ""})
    def _get_temp(self, model, temperature):
        handler = BaseHandler(chat_model=model, temperature=temperature)
        return handler.llm_map[model]().temperature

    def test_temperature_within_bounds_unchanged(self):
        for model in MINIMAX_MODELS:
            t = self._get_temp(model, 0.7)
            self.assertAlmostEqual(t, 0.7, places=5, msg=f"{model}: temp 0.7 should be unchanged")

    def test_temperature_above_1_clamped(self):
        for model in MINIMAX_MODELS:
            t = self._get_temp(model, 1.5)
            self.assertLessEqual(t, 1.0, f"{model}: temp > 1.0 not clamped")

    def test_temperature_zero_raised_to_min(self):
        for model in MINIMAX_MODELS:
            t = self._get_temp(model, 0.0)
            self.assertGreater(t, 0.0, f"{model}: temp=0.0 must be raised above 0")

    def test_temperature_exactly_one(self):
        for model in MINIMAX_MODELS:
            t = self._get_temp(model, 1.0)
            self.assertAlmostEqual(t, 1.0, places=5)


class TestOpenAIModelsUnaffected(unittest.TestCase):
    """Temperature clamping must NOT affect OpenAI or Anthropic entries."""

    @patch.dict(os.environ, {"OPENAI_API_KEY": "oai", "MINIMAX_API_KEY": "mm"})
    def test_openai_high_temp_unaffected(self):
        handler = BaseHandler(chat_model="gpt-3.5-turbo", temperature=1.8)
        llm = handler.llm_map["gpt-3.5-turbo"]()
        self.assertAlmostEqual(llm.temperature, 1.8, places=5)


class TestDefaultModel(unittest.TestCase):
    """BaseHandler defaults to gpt-3.5-turbo (existing behaviour unchanged)."""

    @patch.dict(os.environ, {"OPENAI_API_KEY": "k", "MINIMAX_API_KEY": "mm"})
    def test_default_chat_model(self):
        handler = BaseHandler()
        self.assertEqual(handler.chat_model, "gpt-3.5-turbo")


class TestAllModelsInMap(unittest.TestCase):
    """Both legacy and new MiniMax models are present."""

    @patch.dict(os.environ, {"OPENAI_API_KEY": "k", "MINIMAX_API_KEY": "mm"})
    def test_legacy_models_still_present(self):
        handler = BaseHandler()
        for model in ["gpt-3.5-turbo", "gpt-4", "claude-3-sonnet-20240229"]:
            self.assertIn(model, handler.llm_map)

    @patch.dict(os.environ, {"OPENAI_API_KEY": "k", "MINIMAX_API_KEY": "mm"})
    def test_total_model_count(self):
        handler = BaseHandler()
        # 5 GPT + 2 Claude + 4 MiniMax = 11
        self.assertEqual(len(handler.llm_map), 11)


if __name__ == "__main__":
    unittest.main()
