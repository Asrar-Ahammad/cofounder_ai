"""Landing page template generation node for Web Agent."""

from packages.agents.web.state import WebAgentState


def generate_landing_page_html(state: WebAgentState) -> WebAgentState:
    """Generate responsive MVP landing page HTML with Tailwind styling and lead capture.

    Args:
        state: Active Web agent state.

    Returns:
        WebAgentState: State updated with raw generated HTML.
    """
    feat_cards = ""
    for f in state.features or [{"title": "Autonomous Speed", "desc": "Launch in minutes."}]:
        title = f.get("title", "Feature")
        desc = f.get("desc", "")
        feat_cards += (
            f'<div class="p-6 bg-slate-900/60 rounded-xl border border-slate-800">'
            f'<h3 class="text-xl font-semibold text-white mb-2">{title}</h3>'
            f'<p class="text-slate-400">{desc}</p></div>'
        )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{state.venture_name} — {state.tagline}</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
  <style>body {{ font-family: 'Inter', sans-serif; }}</style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen">
  <main class="max-w-5xl mx-auto px-6 py-20 text-center">
    <span class="text-sm font-semibold tracking-wider text-indigo-400 uppercase">Introducing {state.venture_name}</span>
    <h1 class="text-5xl font-extrabold text-white mt-4 mb-6 tracking-tight">{state.tagline}</h1>
    <p class="text-xl text-slate-400 max-w-2xl mx-auto mb-10">{state.value_proposition}</p>
    <form class="max-w-md mx-auto flex gap-3 mb-16" action="#" method="POST">
      <input type="email" placeholder="Enter your email" required class="flex-1 px-4 py-3 rounded-lg bg-slate-900 border border-slate-800 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500">
      <button type="submit" class="px-6 py-3 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold rounded-lg transition-colors">{state.call_to_action}</button>
    </form>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 text-left">{feat_cards}</div>
  </main>
</body>
</html>"""

    state.generated_html = html.strip()
    return state
