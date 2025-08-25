# Radiology Reporting MVP (Streamlit)

This is a minimal viable product for a radiology reporting tool, built with Python and Streamlit. Features:
- Report creation UI
- Customizable templates/macros (JSON)
- Optional LLM integration (local LM Studio)

## How to run
1. Install requirements: `pip install -r requirements.txt`
2. Start the app: `streamlit run app.py`

## LLM Integration
- Configure the LM Studio endpoint in `config.json`.
- Impression generation uses the local LLM if enabled.

## Next steps
- Add more templates/macros in `templates.json` and `macros.json`.
- Expand the UI and features as needed.

# Build an executable
- `pip install pyinstaller`
- `pyinstaller --onefile --windowed macro_expander.py`
