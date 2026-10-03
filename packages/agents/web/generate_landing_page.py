"""Landing page template generation node for Web Agent."""

import html

from packages.agents.web.state import WebAgentState


def generate_landing_page_html(state: WebAgentState) -> WebAgentState:
    """Generate responsive MVP landing page HTML with stylesheet styling and escaped inputs.

    Args:
        state: Active Web agent state.

    Returns:
        WebAgentState: State updated with raw generated HTML.
    """
    v_name = html.escape(state.venture_name)
    tagline = html.escape(state.tagline)
    val_prop = html.escape(state.value_proposition)
    cta = html.escape(state.call_to_action)

    feat_cards = ""
    features = state.features or [{"title": "Autonomous Speed", "desc": "Launch in minutes."}]
    for f in features:
        title = html.escape(f.get("title", "Feature"))
        desc = html.escape(f.get("desc", ""))
        feat_cards += (
            f'<div class="p-6 bg-slate-900/60 rounded-xl border border-slate-800">'
            f'<h3 class="text-xl font-semibold text-white mb-2">{title}</h3>'
            f'<p class="text-slate-400">{desc}</p></div>'
        )

    page_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{v_name} — {tagline}</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/2.2.19/tailwind.min.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
  <style>body {{ font-family: 'Inter', sans-serif; }}</style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen">
  <main class="max-w-5xl mx-auto px-6 py-20 text-center">
    <span class="text-sm font-semibold tracking-wider text-indigo-400 uppercase">Introducing {v_name}</span>
    <h1 class="text-5xl font-extrabold text-white mt-4 mb-6 tracking-tight">{tagline}</h1>
    <p class="text-xl text-slate-400 max-w-2xl mx-auto mb-10">{val_prop}</p>
    <form class="max-w-md mx-auto mb-16" action="#" method="POST">
      <div class="flex gap-3">
        <input type="email" placeholder="Enter your email" required class="flex-1 px-4 py-3 rounded-lg bg-slate-900 border border-slate-800 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500">
        <button type="submit" class="px-6 py-3 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold rounded-lg transition-colors">{cta}</button>
      </div>
      <p class="text-xs text-slate-500 mt-2">By subscribing, you agree to our terms of service and privacy policy.</p>
    </form>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 text-left">{feat_cards}</div>
  </main>
</body>
</html>"""

    state.generated_html = page_html.strip()
    return state
