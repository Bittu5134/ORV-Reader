def get_chapter_banner(
    current_chapter, first_chapter, last_chapter, base_path="../../../"
):
    """
    Returns the placeholder banner HTML string to be injected and populated via JS at runtime.
    """
    return f'<div id="chapter-banner" data-current="{current_chapter}" data-first="{first_chapter}" data-last="{last_chapter}"></div>'

