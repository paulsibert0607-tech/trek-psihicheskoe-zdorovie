from flask import Flask, request, render_template_string
import os

BASE = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)

# Состояния психики: ключ, вопрос, [специалисты], [тревожные рекомендации], примечание
STATES = [
    {
        "key": "anxiety",
        "question": "Часто чувствуете тревогу, беспокойство, напряжение?",
        "specialists": ["Когнитивно-поведенческий терапевт (КПТ)", "Гештальт-терапевт"],
        "urgent": [],
        "hint": "С КПТ хорошо работается с тревожными состояниями и навязчивыми мыслями.",
    },
    {
        "key": "depression",
        "question": "Ощущаете подавленность, упадок сил, потерю интереса?",
        "specialists": ["Когнитивно-поведенческий терапевт (КПТ)", "Терапевт транзактного анализа"],
        "urgent": ["Если состояние длится более 2 недель или есть мысли о самоповреждении — психиатр"],
        "hint": "Длительное снижение настроения важно не откладывать.",
    },
    {
        "key": "relationships",
        "question": "Есть трудности в отношениях, конфликты, обиды?",
        "specialists": ["Гештальт-терапевт", "Терапевт транзактного анализа"],
        "urgent": [],
        "hint": "Гештальт и транзактный анализ хорошо работают с отношениями и сценариями общения.",
    },
    {
        "key": "habits",
        "question": "Хотите изменить привычки, поведение, достичь цели?",
        "specialists": ["НЛП-практик", "Когнитивно-поведенческий терапевт (КПТ)"],
        "urgent": [],
        "hint": "НЛП и КПТ подходят для работы с привычками и целевыми изменениями.",
    },
    {
        "key": "sleep",
        "question": "Нарушен сон, бессонница, трудности с засыпанием?",
        "specialists": ["Сомнолог", "Когнитивно-поведенческий терапевт (КПТ)"],
        "urgent": ["Если бессонница сочетается с тревогой/подавленностью — психиатр"],
        "hint": "Сон часто связан и с физическим, и с психическим состоянием.",
    },
    {
        "key": "stress",
        "question": "Постоянный стресс, выгорание, усталость от работы?",
        "specialists": ["Гештальт-терапевт", "НЛП-практик"],
        "urgent": ["Эндокринолог — проверить щитовидную железу и гормоны стресса"],
        "hint": "Выгорание бывает и физическим, поэтому иногда нужен и эндокринолог.",
    },
    {
        "key": "selfharm",
        "question": "Бывают мысли о самоповреждении или что не хочется жить?",
        "specialists": [],
        "urgent": ["СРОЧНО: психиатр", "СРОЧНО: кризисная линия 8-800-2000-122 (Россия)"],
        "hint": "Это состояние нельзя оставлять без помощи. Обратитесь за поддержкой прямо сейчас.",
    },
    {
        "key": "ok",
        "question": "В целом справляетесь, но хочется разобраться в себе?",
        "specialists": ["Гештальт-терапевт"],
        "urgent": [],
        "hint": "Работа с психологом полезна и без острого кризиса.",
    },
]

IDX = """
<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<title>Трек психического здоровья</title>
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
  <h1>Трек психического здоровья</h1>
  <div class="sub">По вашему состоянию — подбор подходящего специалиста для первого обращения.</div>
  <div class="note">⚠️ Приложение учебное и НЕ ставит диагноз. Отметьте то, что откликается.
    Ответы не заменяют консультацию специалиста. При острых состояниях — немедленно к врачу.</div>

  <form method="post">
    {% for s in states %}
    <div class="q">
      <label>{{ s.question }}</label>
      <div class="opts">
        <input type="radio" id="{{ s.key }}_y" name="{{ s.key }}" value="yes" {% if entered.get(s.key)=="yes" %}checked{% endif %}>
        <label for="{{ s.key }}_y">Да</label>
        <input type="radio" id="{{ s.key }}_n" name="{{ s.key }}" value="no" {% if entered.get(s.key)=="no" %}checked{% endif %}>
        <label for="{{ s.key }}_n">Нет</label>
      </div>
    </div>
    {% endfor %}
    <button type="submit">Показать, к какому специалисту обратиться</button>
  </form>

  {% if result is not none %}
  <div class="result">
    <h2>Рекомендации</h2>
    {% if result.urgent %}
      <div class="card urgency">
        <h3>Требуется срочное внимание</h3>
        {% for u in result.urgent %}<span class="specialist urgent">{{ u }}</span>{% endfor %}
      </div>
    {% endif %}
    {% if result.specialists %}
      <div class="card">
        <h3>Подходящие специалисты</h3>
        {% for s in result.specialists %}<span class="specialist">{{ s }}</span>{% endfor %}
      </div>
    {% endif %}
    {% if not result.specialists and not result.urgent %}
      <div class="card">
        <h3>Ничего не выбрано</h3>
        <p>Отметьте хотя бы одно состояние — тогда сможем подобрать специалиста.</p>
      </div>
    {% endif %}
    {% if result.hints %}
      <div class="card">
        <h3>Почему так</h3>
        {% for h in result.hints %}<p>• {{ h }}</p>{% endfor %}
      </div>
    {% endif %}
    <div class="note">Напоминаем: результаты не являются медицинским заключением.
      Выбор специалиста — первый шаг, а диагноз и лечение определяет только врач.</div>
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
app.run(host="0.0.0.0", port=port)