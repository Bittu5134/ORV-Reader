import random

DONATION_TEMPLATE = """<div class="donation-banner" style="margin: 20px auto; padding: 15px 20px; background-color: var(--primary); border: 1px solid #ffb74d; border-radius: 8px; text-align: center; max-width: 800px; color: var(--text-primary); box-shadow: 0 4px 15px rgba(255, 183, 77, 0.08);">
    <p style="margin: 0 0 6px 0; font-size: 1em; line-height: 1.5;">💖 <strong>This site is maintained by Readers like you!</strong></p>
    <p style="margin: 0 0 12px 0; font-size: 0.85em; opacity: 0.8;">Hosting and domain costs are funded entirely through community donations.</p>
    <div style="display: flex; justify-content: center; gap: 12px; flex-wrap: wrap;">
        <a href="https://www.patreon.com/cw/LazyBittu" target="_blank" rel="noopener noreferrer" style="display: inline-block; padding: 8px 20px; background-color: #ffb74d; color: #1a1a2e; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 0.85em; text-transform: uppercase; letter-spacing: 0.5px; box-shadow: 0 2px 4px rgba(0,0,0,0.2); transition: opacity 0.3s;">Patreon</a>
        <a href="{base_path}donate" style="display: inline-block; padding: 8px 20px; background-color: #ff5e1f; color: #fff; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 0.85em; text-transform: uppercase; letter-spacing: 0.5px; box-shadow: 0 2px 4px rgba(0,0,0,0.2); transition: opacity 0.3s;">Donate</a>
        <a href="https://discord.gg/CZdNvKaNNr" target="_blank" rel="noopener noreferrer" style="display: inline-block; padding: 8px 20px; background-color: #5865F2; color: #fff; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 0.85em; text-transform: uppercase; letter-spacing: 0.5px; box-shadow: 0 2px 4px rgba(0,0,0,0.2); transition: opacity 0.3s;">Discord</a>
    </div>
</div>"""

DISCORD_TEMPLATE = """<div class="discord-banner" style="margin: 20px auto; padding: 15px 20px; background-color: var(--primary); border: 1px solid #5865F2; border-radius: 8px; text-align: center; max-width: 800px; color: var(--text-primary); box-shadow: 0 4px 15px rgba(88, 101, 242, 0.08);">
    <p style="margin: 0 0 6px 0; font-size: 1em; line-height: 1.5;">💬 <strong>Report issues on our Discord Server!</strong></p>
    <p style="margin: 0 0 12px 0; font-size: 0.85em; opacity: 0.8;">Connect with the community, share theories, and get notified about new chapters.</p>
    <div style="display: flex; justify-content: center; gap: 12px; flex-wrap: wrap;">
        <a href="https://discord.gg/CZdNvKaNNr" target="_blank" rel="noopener noreferrer" style="display: inline-block; padding: 8px 20px; background-color: #5865F2; color: #fff; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 0.85em; text-transform: uppercase; letter-spacing: 0.5px; box-shadow: 0 2px 4px rgba(0,0,0,0.2); transition: opacity 0.3s;">Join Discord</a>
        <a href="{base_path}donate" style="display: inline-block; padding: 8px 20px; background-color: #ff5e1f; color: #fff; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 0.85em; text-transform: uppercase; letter-spacing: 0.5px; box-shadow: 0 2px 4px rgba(0,0,0,0.2); transition: opacity 0.3s;">Donate</a>
    </div>
</div>"""

LOTM_TEMPLATE = """<div class="lotm-banner" style="margin: 20px auto; padding: 15px 20px; background-color: var(--primary); border: 1px solid #38bdf8; border-radius: 8px; text-align: center; max-width: 800px; color: var(--text-primary); box-shadow: 0 4px 15px rgba(56, 189, 248, 0.08);">
    <p style="margin: 0 0 6px 0; font-size: 1em; line-height: 1.5;">🧐 <strong>Looking for a change of pace? Read Lord of the Mysteries!</strong></p>
    <p style="margin: 0 0 12px 0; font-size: 0.85em; opacity: 0.8;">Experience the journey of Klein Moretti on our beautifully formatted sister site.</p>
    <div style="display: flex; justify-content: center; gap: 12px; flex-wrap: wrap;">
        <a href="https://beyonder.pages.dev" target="_blank" rel="noopener noreferrer" style="display: inline-block; padding: 8px 20px; background-color: #0284c7; color: #fff; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 0.85em; text-transform: uppercase; letter-spacing: 0.5px; box-shadow: 0 2px 4px rgba(0,0,0,0.2); transition: opacity 0.3s;">Read LOTM</a>
    </div>
</div>"""

HSY_BDAY = """<div class="hsy-birthday-banner" style="margin: 20px auto; padding: 15px 20px; background-color: #1a1a2e; border: 2px solid #58248c; border-radius: 8px; text-align: center; max-width: 800px; color: #ffffff; box-shadow: 0 4px 15px rgba(138, 43, 226, 0.2);">
    <p style="margin: 0 0 6px 0; font-size: 1.1em; line-height: 1.5;">🖋️ <strong>Happy Birthday to the Greatest Plagiarist, Han Sooyoung!</strong></p>    
    <div style="margin: 15px auto; max-width: 700px;">
        <img src="/assets/misc/hsy-fanart1.jpg" alt="Han Sooyoung" style="width: auto; max-height: 50vh; border-radius: 6px; box-shadow: 0 0 20px rgba(138, 43, 226, 0.3); display: block; margin: 0 auto;">
    </div>

    <div style="display: flex; justify-content: center; gap: 12px; flex-wrap: wrap;">
        <a href="https://www.patreon.com/cw/LazyBittu" target="_blank" rel="noopener noreferrer" style="display: inline-block; padding: 8px 20px; background-color: #8a2be2; color: #fff; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 0.85em; text-transform: uppercase; letter-spacing: 0.5px; box-shadow: 0 2px 4px rgba(0,0,0,0.2); transition: opacity 0.3s;">Patreon</a>
        <a href="/donate" style="display: inline-block; padding: 8px 20px; background-color: #ff5e1f; color: #fff; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 0.85em; text-transform: uppercase; letter-spacing: 0.5px; box-shadow: 0 2px 4px rgba(0,0,0,0.2); transition: opacity 0.3s;">Donate</a>
        <a href="https://discord.gg/CZdNvKaNNr" target="_blank" rel="noopener noreferrer" style="display: inline-block; padding: 8px 20px; background-color: #5865F2; color: #fff; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 0.85em; text-transform: uppercase; letter-spacing: 0.5px; box-shadow: 0 2px 4px rgba(0,0,0,0.2); transition: opacity 0.3s;">Discord</a>
    </div>
</div>"""

EMPTY_TEMPLATE = ""

# Configuration weights (Donate: 40%, Discord: 30%, LOTM: 30%)
BANNER_WEIGHTS = {"donate": 4, "discord": 3, "lotm": 2, "empty": 0, "hsy_bday":0}


def get_chapter_banner(
    current_chapter, first_chapter, last_chapter, base_path="../../../"
):
    """
    Returns the appropriate banner HTML string based on chapter position and weights.
    """
    # 1. Logic for Start/End Chapters
    if current_chapter <= first_chapter + 4:
        selected_html = DISCORD_TEMPLATE
    elif current_chapter >= last_chapter - 4:
        selected_html = DONATION_TEMPLATE
    else:
        # 2. Weighted random rotation for middle chapters
        choices = ["donate", "discord", "lotm", "empty", "hsy_bday"]
        weights = [
            BANNER_WEIGHTS["donate"],
            BANNER_WEIGHTS["discord"],
            BANNER_WEIGHTS["lotm"],
            BANNER_WEIGHTS["empty"],
            BANNER_WEIGHTS["hsy_bday"]
        ]

        pick = random.choices(choices, weights=weights, k=1)[0]
        mapping = {
            "donate": DONATION_TEMPLATE,
            "discord": DISCORD_TEMPLATE,
            "lotm": LOTM_TEMPLATE,
            "hsy_bday": HSY_BDAY,
            "empty": "",
        }
        selected_html = mapping[pick]

    # 3. Inject the relative base_path into the HTML
    return selected_html.format(base_path=base_path)
