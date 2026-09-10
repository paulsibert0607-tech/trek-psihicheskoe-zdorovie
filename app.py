from flask import Flask, request, render_template_string
import os

BASE = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)

# ╨б╨╛╤Б╤В╨╛╤П╨╜╨╕╤П ╨┐╤Б╨╕╤Е╨╕╨║╨╕: ╨║╨╗╤О╤З, ╨▓╨╛╨┐╤А╨╛╤Б, [╤Б╨┐╨╡╤Ж╨╕╨░╨╗╨╕╤Б╤В╤Л], [╤В╤А╨╡╨▓╨╛╨╢╨╜╤Л╨╡ ╤А╨╡╨║╨╛╨╝╨╡╨╜╨┤╨░╤Ж╨╕╨╕], ╨┐╤А╨╕╨╝╨╡╤З╨░╨╜╨╕╨╡
STATES = [
    {
        "key": "anxiety",
        "question": "╨з╨░╤Б╤В╨╛ ╤З╤Г╨▓╤Б╤В╨▓╤Г╨╡╤В╨╡ ╤В╤А╨╡╨▓╨╛╨│╤Г, ╨▒╨╡╤Б╨┐╨╛╨║╨╛╨╣╤Б╤В╨▓╨╛, ╨╜╨░╨┐╤А╤П╨╢╨╡╨╜╨╕╨╡?",
        "specialists": ["╨Ъ╨╛╨│╨╜╨╕╤В╨╕╨▓╨╜╨╛-╨┐╨╛╨▓╨╡╨┤╨╡╨╜╤З╨╡╤Б╨║╨╕╨╣ ╤В╨╡╤А╨░╨┐╨╡╨▓╤В (╨Ъ╨Я╨в)", "╨У╨╡╤И╤В╨░╨╗╤М╤В-╤В╨╡╤А╨░╨┐╨╡╨▓╤В"],
        "urgent": [],
        "hint": "╨б ╨Ъ╨Я╨в ╤Е╨╛╤А╨╛╤И╨╛ ╤А╨░╨▒╨╛╤В╨░╨╡╤В╤Б╤П ╤Б ╤В╤А╨╡╨▓╨╛╨╢╨╜╤Л╨╝╨╕ ╤Б╨╛╤Б╤В╨╛╤П╨╜╨╕╤П╨╝╨╕ ╨╕ ╨╜╨░╨▓╤П╨╖╤З╨╕╨▓╤Л╨╝╨╕ ╨╝╤Л╤Б╨╗╤П╨╝╨╕.",
    },
    {
        "key": "depression",
        "question": "╨Ю╤Й╤Г╤Й╨░╨╡╤В╨╡ ╨┐╨╛╨┤╨░╨▓╨╗╨╡╨╜╨╜╨╛╤Б╤В╤М, ╤Г╨┐╨░╨┤╨╛╨║ ╤Б╨╕╨╗, ╨┐╨╛╤В╨╡╤А╤О ╨╕╨╜╤В╨╡╤А╨╡╤Б╨░?",
        "specialists": ["╨Ъ╨╛╨│╨╜╨╕╤В╨╕╨▓╨╜╨╛-╨┐╨╛╨▓╨╡╨┤╨╡╨╜╤З╨╡╤Б╨║╨╕╨╣ ╤В╨╡╤А╨░╨┐╨╡╨▓╤В (╨Ъ╨Я╨в)", "╨в╨╡╤А╨░╨┐╨╡╨▓╤В ╤В╤А╨░╨╜╨╖╨░╨║╤В╨╜╨╛╨│╨╛ ╨░╨╜╨░╨╗╨╕╨╖╨░"],
        "urgent": ["╨Х╤Б╨╗╨╕ ╤Б╨╛╤Б╤В╨╛╤П╨╜╨╕╨╡ ╨┤╨╗╨╕╤В╤Б╤П ╨▒╨╛╨╗╨╡╨╡ 2 ╨╜╨╡╨┤╨╡╨╗╤М ╨╕╨╗╨╕ ╨╡╤Б╤В╤М ╨╝╤Л╤Б╨╗╨╕ ╨╛ ╤Б╨░╨╝╨╛╨┐╨╛╨▓╤А╨╡╨╢╨┤╨╡╨╜╨╕╨╕ тАФ ╨┐╤Б╨╕╤Е╨╕╨░╤В╤А"],
        "hint": "╨Ф╨╗╨╕╤В╨╡╨╗╤М╨╜╨╛╨╡ ╤Б╨╜╨╕╨╢╨╡╨╜╨╕╨╡ ╨╜╨░╤Б╤В╤А╨╛╨╡╨╜╨╕╤П ╨▓╨░╨╢╨╜╨╛ ╨╜╨╡ ╨╛╤В╨║╨╗╨░╨┤╤Л╨▓╨░╤В╤М.",
    },
    {
        "key": "relationships",
        "question": "╨Х╤Б╤В╤М ╤В╤А╤Г╨┤╨╜╨╛╤Б╤В╨╕ ╨▓ ╨╛╤В╨╜╨╛╤И╨╡╨╜╨╕╤П╤Е, ╨║╨╛╨╜╤Д╨╗╨╕╨║╤В╤Л, ╨╛╨▒╨╕╨┤╤Л?",
        "specialists": ["╨У╨╡╤И╤В╨░╨╗╤М╤В-╤В╨╡╤А╨░╨┐╨╡╨▓╤В", "╨в╨╡╤А╨░╨┐╨╡╨▓╤В ╤В╤А╨░╨╜╨╖╨░╨║╤В╨╜╨╛╨│╨╛ ╨░╨╜╨░╨╗╨╕╨╖╨░"],
        "urgent": [],
        "hint": "╨У╨╡╤И╤В╨░╨╗╤М╤В ╨╕ ╤В╤А╨░╨╜╨╖╨░╨║╤В╨╜╤Л╨╣ ╨░╨╜╨░╨╗╨╕╨╖ ╤Е╨╛╤А╨╛╤И╨╛ ╤А╨░╨▒╨╛╤В╨░╤О╤В ╤Б ╨╛╤В╨╜╨╛╤И╨╡╨╜╨╕╤П╨╝╨╕ ╨╕ ╤Б╤Ж╨╡╨╜╨░╤А╨╕╤П╨╝╨╕ ╨╛╨▒╤Й╨╡╨╜╨╕╤П.",
    },
    {
        "key": "habits",
        "question": "╨е╨╛╤В╨╕╤В╨╡ ╨╕╨╖╨╝╨╡╨╜╨╕╤В╤М ╨┐╤А╨╕╨▓╤Л╤З╨║╨╕, ╨┐╨╛╨▓╨╡╨┤╨╡╨╜╨╕╨╡, ╨┤╨╛╤Б╤В╨╕╤З╤М ╤Ж╨╡╨╗╨╕?",
        "specialists": ["╨Э╨Ы╨Я-╨┐╤А╨░╨║╤В╨╕╨║", "╨Ъ╨╛╨│╨╜╨╕╤В╨╕╨▓╨╜╨╛-╨┐╨╛╨▓╨╡╨┤╨╡╨╜╤З╨╡╤Б╨║╨╕╨╣ ╤В╨╡╤А╨░╨┐╨╡╨▓╤В (╨Ъ╨Я╨в)"],
        "urgent": [],
        "hint": "╨Э╨Ы╨Я ╨╕ ╨Ъ╨Я╨в ╨┐╨╛╨┤╤Е╨╛╨┤╤П╤В ╨┤╨╗╤П ╤А╨░╨▒╨╛╤В╤Л ╤Б ╨┐╤А╨╕╨▓╤Л╤З╨║╨░╨╝╨╕ ╨╕ ╤Ж╨╡╨╗╨╡╨▓╤Л╨╝╨╕ ╨╕╨╖╨╝╨╡╨╜╨╡╨╜╨╕╤П╨╝╨╕.",
    },
    {
        "key": "sleep",
        "question": "╨Э╨░╤А╤Г╤И╨╡╨╜ ╤Б╨╛╨╜, ╨▒╨╡╤Б╤Б╨╛╨╜╨╜╨╕╤Ж╨░, ╤В╤А╤Г╨┤╨╜╨╛╤Б╤В╨╕ ╤Б ╨╖╨░╤Б╤Л╨┐╨░╨╜╨╕╨╡╨╝?",
        "specialists": ["╨б╨╛╨╝╨╜╨╛╨╗╨╛╨│", "╨Ъ╨╛╨│╨╜╨╕╤В╨╕╨▓╨╜╨╛-╨┐╨╛╨▓╨╡╨┤╨╡╨╜╤З╨╡╤Б╨║╨╕╨╣ ╤В╨╡╤А╨░╨┐╨╡╨▓╤В (╨Ъ╨Я╨в)"],
        "urgent": ["╨Х╤Б╨╗╨╕ ╨▒╨╡╤Б╤Б╨╛╨╜╨╜╨╕╤Ж╨░ ╤Б╨╛╤З╨╡╤В╨░╨╡╤В╤Б╤П ╤Б ╤В╤А╨╡╨▓╨╛╨│╨╛╨╣/╨┐╨╛╨┤╨░╨▓╨╗╨╡╨╜╨╜╨╛╤Б╤В╤М╤О тАФ ╨┐╤Б╨╕╤Е╨╕╨░╤В╤А"],
        "hint": "╨б╨╛╨╜ ╤З╨░╤Б╤В╨╛ ╤Б╨▓╤П╨╖╨░╨╜ ╨╕ ╤Б ╤Д╨╕╨╖╨╕╤З╨╡╤Б╨║╨╕╨╝, ╨╕ ╤Б ╨┐╤Б╨╕╤Е╨╕╤З╨╡╤Б╨║╨╕╨╝ ╤Б╨╛╤Б╤В╨╛╤П╨╜╨╕╨╡╨╝.",
    },
    {
        "key": "stress",
        "question": "╨Я╨╛╤Б╤В╨╛╤П╨╜╨╜╤Л╨╣ ╤Б╤В╤А╨╡╤Б╤Б, ╨▓╤Л╨│╨╛╤А╨░╨╜╨╕╨╡, ╤Г╤Б╤В╨░╨╗╨╛╤Б╤В╤М ╨╛╤В ╤А╨░╨▒╨╛╤В╤Л?",
        "specialists": ["╨У╨╡╤И╤В╨░╨╗╤М╤В-╤В╨╡╤А╨░╨┐╨╡╨▓╤В", "╨Э╨Ы╨Я-╨┐╤А╨░╨║╤В╨╕╨║"],
        "urgent": ["╨н╨╜╨┤╨╛╨║╤А╨╕╨╜╨╛╨╗╨╛╨│ тАФ ╨┐╤А╨╛╨▓╨╡╤А╨╕╤В╤М ╤Й╨╕╤В╨╛╨▓╨╕╨┤╨╜╤Г╤О ╨╢╨╡╨╗╨╡╨╖╤Г ╨╕ ╨│╨╛╤А╨╝╨╛╨╜╤Л ╤Б╤В╤А╨╡╤Б╤Б╨░"],
        "hint": "╨Т╤Л╨│╨╛╤А╨░╨╜╨╕╨╡ ╨▒╤Л╨▓╨░╨╡╤В ╨╕ ╤Д╨╕╨╖╨╕╤З╨╡╤Б╨║╨╕╨╝, ╨┐╨╛╤Н╤В╨╛╨╝╤Г ╨╕╨╜╨╛╨│╨┤╨░ ╨╜╤Г╨╢╨╡╨╜ ╨╕ ╤Н╨╜╨┤╨╛╨║╤А╨╕╨╜╨╛╨╗╨╛╨│.",
    },
    {
        "key": "selfharm",
        "question": "╨С╤Л╨▓╨░╤О╤В ╨╝╤Л╤Б╨╗╨╕ ╨╛ ╤Б╨░╨╝╨╛╨┐╨╛╨▓╤А╨╡╨╢╨┤╨╡╨╜╨╕╨╕ ╨╕╨╗╨╕ ╤З╤В╨╛ ╨╜╨╡ ╤Е╨╛╤З╨╡╤В╤Б╤П ╨╢╨╕╤В╤М?",
        "specialists": [],
        "urgent": ["╨б╨а╨Ю╨з╨Э╨Ю: ╨┐╤Б╨╕╤Е╨╕╨░╤В╤А", "╨б╨а╨Ю╨з╨Э╨Ю: ╨║╤А╨╕╨╖╨╕╤Б╨╜╨░╤П ╨╗╨╕╨╜╨╕╤П 8-800-2000-122 (╨а╨╛╤Б╤Б╨╕╤П)"],
        "hint": "╨н╤В╨╛ ╤Б╨╛╤Б╤В╨╛╤П╨╜╨╕╨╡ ╨╜╨╡╨╗╤М╨╖╤П ╨╛╤Б╤В╨░╨▓╨╗╤П╤В╤М ╨▒╨╡╨╖ ╨┐╨╛╨╝╨╛╤Й╨╕. ╨Ю╨▒╤А╨░╤В╨╕╤В╨╡╤Б╤М ╨╖╨░ ╨┐╨╛╨┤╨┤╨╡╤А╨╢╨║╨╛╨╣ ╨┐╤А╤П╨╝╨╛ ╤Б╨╡╨╣╤З╨░╤Б.",
    },
    {
        "key": "ok",
        "question": "╨Т ╤Ж╨╡╨╗╨╛╨╝ ╤Б╨┐╤А╨░╨▓╨╗╤П╨╡╤В╨╡╤Б╤М, ╨╜╨╛ ╤Е╨╛╤З╨╡╤В╤Б╤П ╤А╨░╨╖╨╛╨▒╤А╨░╤В╤М╤Б╤П ╨▓ ╤Б╨╡╨▒╨╡?",
        "specialists": ["╨У╨╡╤И╤В╨░╨╗╤М╤В-╤В╨╡╤А╨░╨┐╨╡╨▓╤В"],
        "urgent": [],
        "hint": "╨а╨░╨▒╨╛╤В╨░ ╤Б ╨┐╤Б╨╕╤Е╨╛╨╗╨╛╨│╨╛╨╝ ╨┐╨╛╨╗╨╡╨╖╨╜╨░ ╨╕ ╨▒╨╡╨╖ ╨╛╤Б╤В╤А╨╛╨│╨╛ ╨║╤А╨╕╨╖╨╕╤Б╨░.",
    },
]

IDX = """
<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<title>╨в╤А╨╡╨║ ╨┐╤Б╨╕╤Е╨╕╤З╨╡╤Б╨║╨╛╨│╨╛ ╨╖╨┤╨╛╤А╨╛╨▓╤М╤П</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'Segoe UI', Arial, sans-serif; background: #0f172a; color: #e2e8f0; min-height: 100vh; }
  .wrap { max-width: 860px; margin: 0 auto; padding: 28px 20px 60px; }
  h1 { font-size: 26px; margin-bottom: 6px; }
  .sub { color: #94a3b8; font-size: 14px; margin-bottom: 20px; }
  .note { background: #1e293b; border: 1px dashed #334155; border-radius: 12px; padding: 12px 16px;
    color: #94a3b8; font-size: 13px; margin-bottom: 22px; }
  form { background: #1e293b; border-radius: 16px; padding: 20px; }
  .q { margin-bottom: 14px; padding: 12px 14px; border: 1px solid #334155; border-radius: 12px; }
  .q label { display: block; font-size: 15px; margin-bottom: 8px; }
  .opts { display: flex; gap: 10px; flex-wrap: wrap; }
  .opts input { display: none; }
  .opts label { border: 1px solid #334155; border-radius: 999px; padding: 7px 16px; cursor: pointer; font-size: 14px;
    background: #0f172a; color: #94a3b8; margin-bottom: 0; }
  .opts input:checked + label { background: #2563eb; color: #fff; border-color: #2563eb; }
  button { margin-top: 14px; padding: 13px 26px; border-radius: 12px; border: none; cursor: pointer;
    background: linear-gradient(135deg,#2563eb,#0ea5e9); color: #fff; font-weight: 700; font-size: 15px; }
  .result { margin-top: 22px; }
  .card { background: #1e293b; border-radius: 14px; padding: 16px 20px; margin-bottom: 12px; border-left: 5px solid #4ade80; }
  .card.warn { border-left-color: #f87171; }
  .card.urgency { border-left-color: #f87171; }
  .card h3 { font-size: 16px; margin-bottom: 4px; }
  .card p { color: #94a3b8; font-size: 14px; }
  .specialist { display: inline-block; margin-top: 8px; margin-right: 6px; padding: 5px 14px; border-radius: 999px;
    background: rgba(56,189,248,.12); color: #38bdf8; font-size: 13px; }
  .specialist.urgent { background: rgba(248,113,113,.12); color: #f87171; }
  h2 { font-size: 19px; margin-bottom: 10px; }
</style>
</head>
<body>
<div class="wrap">
  <h1>╨в╤А╨╡╨║ ╨┐╤Б╨╕╤Е╨╕╤З╨╡╤Б╨║╨╛╨│╨╛ ╨╖╨┤╨╛╤А╨╛╨▓╤М╤П</h1>
  <div class="sub">╨Я╨╛ ╨▓╨░╤И╨╡╨╝╤Г ╤Б╨╛╤Б╤В╨╛╤П╨╜╨╕╤О тАФ ╨┐╨╛╨┤╨▒╨╛╤А ╨┐╨╛╨┤╤Е╨╛╨┤╤П╤Й╨╡╨│╨╛ ╤Б╨┐╨╡╤Ж╨╕╨░╨╗╨╕╤Б╤В╨░ ╨┤╨╗╤П ╨┐╨╡╤А╨▓╨╛╨│╨╛ ╨╛╨▒╤А╨░╤Й╨╡╨╜╨╕╤П.</div>
  <div class="note">тЪая╕П ╨Я╤А╨╕╨╗╨╛╨╢╨╡╨╜╨╕╨╡ ╤Г╤З╨╡╨▒╨╜╨╛╨╡ ╨╕ ╨Э╨Х ╤Б╤В╨░╨▓╨╕╤В ╨┤╨╕╨░╨│╨╜╨╛╨╖. ╨Ю╤В╨╝╨╡╤В╤М╤В╨╡ ╤В╨╛, ╤З╤В╨╛ ╨╛╤В╨║╨╗╨╕╨║╨░╨╡╤В╤Б╤П.
    ╨Ю╤В╨▓╨╡╤В╤Л ╨╜╨╡ ╨╖╨░╨╝╨╡╨╜╤П╤О╤В ╨║╨╛╨╜╤Б╤Г╨╗╤М╤В╨░╤Ж╨╕╤О ╤Б╨┐╨╡╤Ж╨╕╨░╨╗╨╕╤Б╤В╨░. ╨Я╤А╨╕ ╨╛╤Б╤В╤А╤Л╤Е ╤Б╨╛╤Б╤В╨╛╤П╨╜╨╕╤П╤Е тАФ ╨╜╨╡╨╝╨╡╨┤╨╗╨╡╨╜╨╜╨╛ ╨║ ╨▓╤А╨░╤З╤Г.</div>

  <form method="post">
    {% for s in states %}
    <div class="q">
      <label>{{ s.question }}</label>
      <div class="opts">
        <input type="radio" id="{{ s.key }}_y" name="{{ s.key }}" value="yes" {% if entered.get(s.key)=="yes" %}checked{% endif %}>
        <label for="{{ s.key }}_y">╨Ф╨░</label>
        <input type="radio" id="{{ s.key }}_n" name="{{ s.key }}" value="no" {% if entered.get(s.key)=="no" %}checked{% endif %}>
        <label for="{{ s.key }}_n">╨Э╨╡╤В</label>
      </div>
    </div>
    {% endfor %}
    <button type="submit">╨Я╨╛╨║╨░╨╖╨░╤В╤М, ╨║ ╨║╨░╨║╨╛╨╝╤Г ╤Б╨┐╨╡╤Ж╨╕╨░╨╗╨╕╤Б╤В╤Г ╨╛╨▒╤А╨░╤В╨╕╤В╤М╤Б╤П</button>
  </form>

  {% if result is not none %}
  <div class="result">
    <h2>╨а╨╡╨║╨╛╨╝╨╡╨╜╨┤╨░╤Ж╨╕╨╕</h2>
    {% if result.urgent %}
      <div class="card urgency">
        <h3>╨в╤А╨╡╨▒╤Г╨╡╤В╤Б╤П ╤Б╤А╨╛╤З╨╜╨╛╨╡ ╨▓╨╜╨╕╨╝╨░╨╜╨╕╨╡</h3>
        {% for u in result.urgent %}<span class="specialist urgent">{{ u }}</span>{% endfor %}
      </div>
    {% endif %}
    {% if result.specialists %}
      <div class="card">
        <h3>╨Я╨╛╨┤╤Е╨╛╨┤╤П╤Й╨╕╨╡ ╤Б╨┐╨╡╤Ж╨╕╨░╨╗╨╕╤Б╤В╤Л</h3>
        {% for s in result.specialists %}<span class="specialist">{{ s }}</span>{% endfor %}
      </div>
    {% endif %}
    {% if not result.specialists and not result.urgent %}
      <div class="card">
        <h3>╨Э╨╕╤З╨╡╨│╨╛ ╨╜╨╡ ╨▓╤Л╨▒╤А╨░╨╜╨╛</h3>
        <p>╨Ю╤В╨╝╨╡╤В╤М╤В╨╡ ╤Е╨╛╤В╤П ╨▒╤Л ╨╛╨┤╨╜╨╛ ╤Б╨╛╤Б╤В╨╛╤П╨╜╨╕╨╡ тАФ ╤В╨╛╨│╨┤╨░ ╤Б╨╝╨╛╨╢╨╡╨╝ ╨┐╨╛╨┤╨╛╨▒╤А╨░╤В╤М ╤Б╨┐╨╡╤Ж╨╕╨░╨╗╨╕╤Б╤В╨░.</p>
      </div>
    {% endif %}
    {% if result.hints %}
      <div class="card">
        <h3>╨Я╨╛╤З╨╡╨╝╤Г ╤В╨░╨║</h3>
        {% for h in result.hints %}<p>тАв {{ h }}</p>{% endfor %}
      </div>
    {% endif %}
    <div class="note">╨Э╨░╨┐╨╛╨╝╨╕╨╜╨░╨╡╨╝: ╤А╨╡╨╖╤Г╨╗╤М╤В╨░╤В╤Л ╨╜╨╡ ╤П╨▓╨╗╤П╤О╤В╤Б╤П ╨╝╨╡╨┤╨╕╤Ж╨╕╨╜╤Б╨║╨╕╨╝ ╨╖╨░╨║╨╗╤О╤З╨╡╨╜╨╕╨╡╨╝.
      ╨Т╤Л╨▒╨╛╤А ╤Б╨┐╨╡╤Ж╨╕╨░╨╗╨╕╤Б╤В╨░ тАФ ╨┐╨╡╤А╨▓╤Л╨╣ ╤И╨░╨│, ╨░ ╨┤╨╕╨░╨│╨╜╨╛╨╖ ╨╕ ╨╗╨╡╤З╨╡╨╜╨╕╨╡ ╨╛╨┐╤А╨╡╨┤╨╡╨╗╤П╨╡╤В ╤В╨╛╨╗╤М╨║╨╛ ╨▓╤А╨░╤З.</div>
  </div>
  {% endif %}
</div>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def index():
    entered = {}
    result = None
    if request.method == "POST":
        specialists = []
        urgent = []
        hints = []
        for s in STATES:
            key = s["key"]
            val = request.form.get(key, "")
            entered[key] = val
            if val == "yes":
                if s["urgent"]:
                    for u in s["urgent"]:
                        if u not in urgent:
                            urgent.append(u)
                for sp in s["specialists"]:
                    if sp not in specialists:
                        specialists.append(sp)
                if s["hint"]:
                    hints.append(s["hint"])
        result = {"specialists": specialists, "urgent": urgent, "hints": hints}
    return render_template_string(IDX, states=STATES, entered=entered, result=result)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
