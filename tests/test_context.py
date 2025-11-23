# tests/test_context.py
import sys
import os
sys.path.append(os.path.abspath("src"))

from main import get_relevant_context

def test_get_relevant_context():
    # Fake in-memory knowledge
    fake_knowledge = {
        "pedri": "Pedri is a midfielder for FC Barcelona.",
        "gavi": "Gavi is known for his aggressive playstyle."
    }

    # Inject fake knowledge into the module
    import main
    main.knowledge = fake_knowledge

    # Test keyword search
    message = "Tell me about Pedri"

    ctx = get_relevant_context(message)

    assert len(ctx) == 1
    assert "Pedri is a midfielder" in ctx[0]

def test_no_context():
    import main
    main.knowledge = {"pedri": "some info"}

    message = "What time is it?"

    ctx = get_relevant_context(message)

    assert ctx == []
