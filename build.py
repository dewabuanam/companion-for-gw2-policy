"""Builds index.html from policy.json.

policy.json is the policy: the date it last changed and its sections in each language.
The Companion for GW2 app reads that file directly, and this page is made from it, so
the two always say the same thing. Edit policy.json, run `python build.py`, and push.
"""
import html
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LANGUAGES = [("en", "English"), ("de", "Deutsch"), ("fr", "Français"), ("es", "Español")]
HEADINGS = {
    "en": ("Companion for GW2", "Policy and disclaimer", "Last updated"),
    "de": ("Begleiter für GW2", "Richtlinie und Haftungsausschluss", "Zuletzt aktualisiert"),
    "fr": ("Compagnon pour GW2", "Politique et avertissement", "Dernière mise à jour"),
    "es": ("Compañero para GW2", "Política y aviso legal", "Última actualización"),
}

policy = json.load(open(os.path.join(HERE, "policy.json"), encoding="utf-8"))


def block(tag, sections):
    name, subtitle, updated = HEADINGS[tag]
    parts = [f'<section class="lang" lang="{tag}" data-lang="{tag}"{" hidden" if tag != "en" else ""}>',
             f"<h1>{html.escape(name)}</h1>", f'<p class="sub">{html.escape(subtitle)}</p>']
    for s in sections:
        cls = "card highlight" if s.get("highlight") else "card"
        parts.append(f'<article class="{cls}"><h2>{html.escape(s["title"])}</h2><p>{html.escape(s["body"])}</p></article>')
    parts.append(f'<p class="updated">{html.escape(updated)}: <time datetime="{policy["updated"]}">{policy["updated"]}</time></p>')
    parts.append("</section>")
    return "\n".join(parts)


buttons = "".join(
    f'<button type="button" data-set="{tag}" aria-pressed="{str(tag == "en").lower()}">{label}</button>'
    for tag, label in LANGUAGES if tag in policy["languages"]
)
body = "\n".join(block(tag, policy["languages"][tag]) for tag, _ in LANGUAGES if tag in policy["languages"])

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Companion for GW2 – Policy</title>
<meta name="description" content="Policy, privacy and disclaimer for Companion for GW2, an unofficial Guild Wars 2 fan app.">
<style>
:root {{
  --bg: #f6f1e7; --panel: #fffaf0; --text: #2a2419; --muted: #6f6453; --trim: #a8781f; --rule: #e2d4b6;
}}
@media (prefers-color-scheme: dark) {{
  :root {{ --bg: #12100c; --panel: #1d1a14; --text: #efe6d4; --muted: #a99d86; --trim: #e3c47a; --rule: #3a3326; }}
}}
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: var(--bg); color: var(--text);
  font: 16px/1.6 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; }}
main {{ max-width: 760px; margin: 0 auto; padding: 24px 16px 48px; }}
nav {{ display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 16px; }}
nav button {{ font: inherit; font-size: 14px; padding: 6px 14px; border-radius: 999px; cursor: pointer;
  border: 1px solid var(--rule); background: var(--panel); color: var(--text); }}
nav button[aria-pressed="true"] {{ border-color: var(--trim); color: var(--trim); font-weight: 600; }}
h1 {{ margin: 8px 0 0; font-size: 28px; color: var(--trim); }}
.sub {{ margin: 0 0 20px; color: var(--muted); }}
.card {{ background: var(--panel); border: 1px solid var(--rule); border-radius: 12px; padding: 14px 16px; margin-bottom: 12px; }}
.card.highlight {{ border-color: var(--trim); }}
h2 {{ margin: 0 0 4px; font-size: 18px; color: var(--trim); }}
.card p {{ margin: 0; }}
.updated {{ color: var(--muted); font-size: 14px; }}
</style>
</head>
<body>
<main>
<nav aria-label="Language">{buttons}</nav>
{body}
</main>
<script>
// Opens in the reader's own language where the policy has it, and lets them switch.
const show = tag => {{
  document.querySelectorAll('[data-lang]').forEach(s => s.hidden = s.dataset.lang !== tag);
  document.querySelectorAll('[data-set]').forEach(b => b.setAttribute('aria-pressed', b.dataset.set === tag));
  document.documentElement.lang = tag;
}};
document.querySelectorAll('[data-set]').forEach(b => b.addEventListener('click', () => show(b.dataset.set)));
const wanted = (new URLSearchParams(location.search).get('lang') || navigator.language || 'en').slice(0, 2);
if (document.querySelector(`[data-lang="${{wanted}}"]`)) show(wanted);
</script>
</body>
</html>
"""
open(os.path.join(HERE, "index.html"), "w", encoding="utf-8", newline="\n").write(page)
print("index.html built,", sum(len(v) for v in policy["languages"].values()), "sections")
