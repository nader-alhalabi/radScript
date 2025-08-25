import streamlit as st
import json
import requests
import streamlit_js_eval
import streamlit.components.v1 as components

# Load config, templates, and macros
def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

config = load_json('config.json')
templates = load_json('templates.json')
macros = load_json('macros.json')

def generate_impression(findings, endpoint):
    prompt = f"Summarize these radiology findings as an impression: {findings}"
    data = {
        "model": "local-llm",
        "messages": [
            {"role": "system", "content": "You are a radiology report assistant."},
            {"role": "user", "content": prompt}
        ]
    }
    try:
        resp = requests.post(endpoint, json=data, timeout=10)
        resp.raise_for_status()
        return resp.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"[LLM error: {e}]"

st.title("Radiology Reporting MVP")

# Voice dictation for findings using HTML/JS
st.subheader("Voice Dictation (Findings)")
voice_script = """
<script>
let recognizing = false;
let finalTranscript = '';
if (!('webkitSpeechRecognition' in window)) {
  document.getElementById('voice_status').innerText = 'Speech recognition not supported.';
} else {
  var recognition = new webkitSpeechRecognition();
  recognition.continuous = false;
  recognition.interimResults = false;
  recognition.lang = 'en-US';
  recognition.onstart = function() {
    recognizing = true;
    document.getElementById('voice_status').innerText = 'Listening...';
  };
  recognition.onend = function() {
    recognizing = false;
    document.getElementById('voice_status').innerText = 'Click to start voice dictation.';
  };
  recognition.onresult = function(event) {
    finalTranscript = event.results[0][0].transcript;
    document.getElementById('findings_voice').value += finalTranscript + '\n';
    window.parent.postMessage({"type": "streamlit:setComponentValue", "value": finalTranscript}, "*");
  };
}
function startDictation() {
  if (recognizing) {
    recognition.stop();
    return;
  }
  recognition.start();
}
</script>
<div>
  <button onclick="startDictation()">Start Voice Dictation</button>
  <span id="voice_status">Click to start voice dictation.</span><br>
  <textarea id="findings_voice" style="display:none"></textarea>
</div>
"""
voice_text = components.html(voice_script, height=100)
if voice_text and isinstance(voice_text, str) and voice_text.strip():
    st.session_state.setdefault('findings', '')
    st.session_state['findings'] += voice_text + "\n"

# Template selection
selected_template = st.selectbox("Choose a template", [t['name'] for t in templates])
template = next(t for t in templates if t['name'] == selected_template)

# Macros
st.subheader("Insert Macro")
macro_key = st.selectbox("Macro", list(macros.keys()))
if st.button("Insert Macro"):
    st.session_state.setdefault('findings', '')
    st.session_state['findings'] += macros[macro_key] + "\n"

# Findings input
findings = st.text_area("Findings", value=st.session_state.get('findings', ''), height=150)
st.session_state['findings'] = findings

# Impression (AI or manual)
impression = ""
if config.get('llm_enabled'):
    if st.button("Generate Impression with LLM"):
        impression = generate_impression(findings, config['llm_endpoint'])
        st.session_state['impression'] = impression
impression = st.text_area("Impression", value=st.session_state.get('impression', ''), height=100)
st.session_state['impression'] = impression

# Final report
if st.button("Create Report"):
    report = template['template'].replace('[Findings]', findings).replace('[Impression]', impression)
    st.text_area("Final Report", value=report, height=200)
