"""Integration tests for MiniMax provider – validates endpoint contract and
UI model list without requiring real external services."""
import os
import sys
import types
import unittest
from unittest.mock import MagicMock, patch

# ---------------------------------------------------------------------------
# Re-use the same stub setup as unit tests
# ---------------------------------------------------------------------------

def _make_stub_module(name):
    if name in sys.modules:
        return sys.modules[name]
    mod = types.ModuleType(name)
    sys.modules[name] = mod
    return mod


def _setup_stubs():
    pc = _make_stub_module("pinecone")
    pc.init = MagicMock()
    _make_stub_module("pinecone.core")
    _make_stub_module("pinecone.core.client")
    exc = _make_stub_module("pinecone.core.client.exceptions")
    exc.ApiException = Exception

    lo = _make_stub_module("langchain_openai")

    class _FakeChatOpenAI:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)

    em = _make_stub_module("langchain_openai.embeddings")
    em.OpenAIEmbeddings = MagicMock
    cm = _make_stub_module("langchain_openai.chat_models")
    cm.ChatOpenAI = _FakeChatOpenAI

    la = _make_stub_module("langchain_anthropic")
    la.ChatAnthropic = MagicMock

    lc = _make_stub_module("langchain")
    lc_chains = _make_stub_module("langchain.chains")
    lc_chains.ConversationalRetrievalChain = MagicMock
    lc_ts = _make_stub_module("langchain.text_splitter")
    for cls in [
        "TokenTextSplitter", "TextSplitter", "Tokenizer", "Language",
        "RecursiveCharacterTextSplitter", "RecursiveJsonSplitter",
        "LatexTextSplitter", "PythonCodeTextSplitter", "KonlpyTextSplitter",
        "SpacyTextSplitter", "NLTKTextSplitter",
        "SentenceTransformersTokenTextSplitter", "ElementType", "HeaderType",
        "LineType", "HTMLHeaderTextSplitter", "MarkdownHeaderTextSplitter",
        "MarkdownTextSplitter", "CharacterTextSplitter",
    ]:
        setattr(lc_ts, cls, MagicMock)

    lcc = _make_stub_module("langchain_community")
    vs = _make_stub_module("langchain_community.vectorstores")
    vsp = _make_stub_module("langchain_community.vectorstores.pinecone")
    vsp.Pinecone = MagicMock
    dl = _make_stub_module("langchain_community.document_loaders")
    dl.TextLoader = MagicMock
    dl.PyMuPDFLoader = MagicMock
    dl.Docx2txtLoader = MagicMock

    fa = _make_stub_module("fastapi")
    fa.UploadFile = MagicMock
    fa.HTTPException = Exception

    de = _make_stub_module("dotenv")
    de.load_dotenv = MagicMock

    _make_stub_module("utils")
    ua = _make_stub_module("utils.alerts")
    ua.alert_exception = MagicMock
    ua.alert_info = MagicMock


_setup_stubs()

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from handlers.base import BaseHandler  # noqa: E402

MINIMAX_MODELS = [
    "MiniMax-M2.7",
    "MiniMax-M2.7-highspeed",
    "MiniMax-M2.5",
    "MiniMax-M2.5-highspeed",
]

# The complete list that the /chat endpoint accepts
ENDPOINT_MODELS = [
    "gpt-3.5-turbo", "gpt-3.5-turbo-16k", "gpt-4", "gpt-4-32k",
    "gpt-4-1106-preview", "claude-3-sonnet-20240229", "claude-3-opus-20240229",
    "MiniMax-M2.7", "MiniMax-M2.7-highspeed",
    "MiniMax-M2.5", "MiniMax-M2.5-highspeed",
]

UI_MODELS = ENDPOINT_MODELS  # ui/main.py should match


class TestEndpointModelList(unittest.TestCase):
    """Validate that endpoints/chat.py contains all MiniMax models."""

    def _get_available_models(self):
        """Parse available_models from the chat endpoint source."""
        chat_path = os.path.join(os.path.dirname(__file__), "..", "endpoints", "chat.py")
        with open(chat_path) as fh:
            source = fh.read()
        # Extract the list literal after 'available_models = '
        import ast, re
        m = re.search(r"available_models\s*=\s*(\[[^\]]+\])", source)
        self.assertIsNotNone(m, "Could not find available_models in chat.py")
        return ast.literal_eval(m.group(1))

    def test_minimax_models_in_endpoint(self):
        models = self._get_available_models()
        for model in MINIMAX_MODELS:
            self.assertIn(model, models, f"{model} missing from endpoint available_models")

    def test_legacy_models_retained(self):
        models = self._get_available_models()
        for model in ["gpt-3.5-turbo", "gpt-4", "claude-3-sonnet-20240229"]:
            self.assertIn(model, models)


class TestUIModelList(unittest.TestCase):
    """Validate that ui/main.py selectbox contains all MiniMax models."""

    def _get_ui_models(self):
        ui_path = os.path.join(os.path.dirname(__file__), "..", "ui", "main.py")
        with open(ui_path) as fh:
            source = fh.read()
        import ast, re
        m = re.search(r"model_selector\s*=\s*st\.selectbox\([^,]+,\s*(\[[^\]]+\])", source, re.DOTALL)
        self.assertIsNotNone(m, "Could not find model_selector list in ui/main.py")
        return ast.literal_eval(m.group(1))

    def test_minimax_models_in_ui(self):
        models = self._get_ui_models()
        for model in MINIMAX_MODELS:
            self.assertIn(model, models, f"{model} missing from UI selectbox")


class TestEnvFileUpdated(unittest.TestCase):
    """example.env must include MINIMAX_API_KEY."""

    def test_minimax_key_in_example_env(self):
        env_path = os.path.join(os.path.dirname(__file__), "..", "example.env")
        with open(env_path) as fh:
            content = fh.read()
        self.assertIn("MINIMAX_API_KEY", content)


class TestHandlerInstantiatesAllModels(unittest.TestCase):
    """BaseHandler can be created for each MiniMax model name."""

    @patch.dict(os.environ, {"MINIMAX_API_KEY": "mm-test", "OPENAI_API_KEY": "oai"})
    def test_handler_creation_per_model(self):
        for model in MINIMAX_MODELS:
            handler = BaseHandler(chat_model=model, temperature=0.5)
            self.assertEqual(handler.chat_model, model)

    @patch.dict(os.environ, {"MINIMAX_API_KEY": "mm-test", "OPENAI_API_KEY": "oai"})
    def test_llm_instantiation_per_model(self):
        for model in MINIMAX_MODELS:
            handler = BaseHandler(chat_model=model, temperature=0.8)
            llm = handler.llm_map[model]()
            self.assertEqual(llm.openai_api_base, "https://api.minimax.io/v1")
            self.assertLessEqual(llm.temperature, 1.0)
            self.assertGreater(llm.temperature, 0.0)


class TestTemperatureEdgeCases(unittest.TestCase):
    """Verify temperature clamping edge cases for MiniMax models."""

    @patch.dict(os.environ, {"MINIMAX_API_KEY": "k", "OPENAI_API_KEY": "oai"})
    def test_temperature_2_clamped_to_1(self):
        handler = BaseHandler(chat_model="MiniMax-M2.7", temperature=2.0)
        llm = handler.llm_map["MiniMax-M2.7"]()
        self.assertAlmostEqual(llm.temperature, 1.0, places=5)

    @patch.dict(os.environ, {"MINIMAX_API_KEY": "k", "OPENAI_API_KEY": "oai"})
    def test_temperature_negative_raised(self):
        handler = BaseHandler(chat_model="MiniMax-M2.5", temperature=-0.5)
        llm = handler.llm_map["MiniMax-M2.5"]()
        self.assertGreater(llm.temperature, 0.0)

    @patch.dict(os.environ, {"MINIMAX_API_KEY": "k", "OPENAI_API_KEY": "oai"})
    def test_temperature_0_01_unchanged(self):
        handler = BaseHandler(chat_model="MiniMax-M2.5-highspeed", temperature=0.01)
        llm = handler.llm_map["MiniMax-M2.5-highspeed"]()
        self.assertAlmostEqual(llm.temperature, 0.01, places=5)


if __name__ == "__main__":
    unittest.main()
