"""
MiroOrca Backend Entry Point
Run with: python run.py  (or via uv: uv run python run.py)
"""

from app import create_app
from app.config import config

app = create_app()

if __name__ == "__main__":
    try:
        config.validate()
    except ValueError as e:
        print(f"\n❌ Configuration error: {e}\n")
        exit(1)

    print("\n🌊 MiroOrca backend starting...")
    print(f"   LLM:    {config.LLM_MODEL_NAME} @ {config.LLM_BASE_URL}")
    print(f"   Neo4j:  {config.NEO4J_URI}")
    if config.SMART_MODEL_NAME:
        print(f"   Smart:  {config.SMART_MODEL_NAME}")
    print(f"   Debug:  {config.DEBUG}")
    print(f"\n   API running at http://localhost:5001\n")

    app.run(host="0.0.0.0", port=5001, debug=config.DEBUG)
