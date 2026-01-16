import telegramify_markdown

def render_report_md2(text: str) -> str:
    return telegramify_markdown.markdownify(text or "")
