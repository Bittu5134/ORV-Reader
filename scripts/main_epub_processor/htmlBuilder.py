import re
import os
import urllib.parse as urlparse


for file_index, file in enumerate(os.listdir("chapters/orv")):

    try:
        # if not file_index == 1:
        #     continue

        if not file.endswith(".txt"):
            continue
        file_index = int(file.replace(".txt", "").replace("chap_", "")) - 1
        with open(f"./chapters/orv/{file}", "r", encoding="utf-8") as f:
            textStr = f.read()
            # Temporarily replace special markers to preserve them during & escaping
            markers = {
                '<!>': '___MARKER_SYSTEM___',
                '<@>': '___MARKER_CONSTELLATION___',
                '<&>': '___MARKER_QUOTE___',
                '<#>': '___MARKER_OUTERGOD___',
                '<?>': '___MARKER_NOTICE___',
            }
            for marker, placeholder in markers.items():
                textStr = textStr.replace(marker, placeholder)
            
            # Escape ampersand characters that are not part of HTML entities
            # This regex matches & that are NOT followed by common HTML entity patterns
            textStr = re.sub(r'&(?!(?:lt|gt|amp|quot|apos|#\d+|#x[\da-fA-F]+);)', '&amp;', textStr)
            
            def replace_match(match):
                original_tag = match.group(0)
                return f"&lt;{original_tag[1:-1]}&gt;"

            pattern = r'<(?!img\b|title\b|cover\b|br\b)(?=[^\n>]{1,})(?=[^\n>]*\w)[^\n>]*?>'
            textStr = re.sub(pattern, replace_match, textStr)
            
            # Restore the special markers
            for marker, placeholder in markers.items():
                textStr = textStr.replace(placeholder, marker)
            
            text = textStr.split("\n")

        with open("website/stories/orv/read/template.html", "r", encoding="utf-8") as f:
            template = f.read()

        html = []

        skip_line = 0
        for index, line in enumerate(text):
            if skip_line > 0:
                skip_line -= 1
                continue

            if line == "+":
                window_text = []
                window_text.append('<div class="orv_window">')
                if index + 1 > len(text):
                    continue
                for window_line in text[index + 1 :]:
                    skip_line += 1
                    if window_line == "+":
                        break
                    if window_line.startswith("["):
                        window_line = f'<h3 class="orv_window_title">{window_line}</h3>'
                    else:
                        window_line = f"<p>{window_line}</p>"
                    window_text.append(window_line)
                window_text.append("</div>")
                html.extend(window_text)
                continue
            if line == "++":
                window_text = []
                window_text.append('<div class="orv_box">')
                if index + 1 > len(text):
                    continue
                for window_line in text[index + 1 :]:
                    skip_line += 1
                    if window_line == "++":
                        break
                    window_line = f"<p>{window_line}</p>"
                    window_text.append(window_line)
                window_text.append("</div>")
                html.extend(window_text)
                continue

            if line.startswith("<title>"):
                template = template.replace(r"{{TITLE}}", line.replace("<title>", ""))
                # print(file_index + 1, line.replace("<title>", ""))
                line = re.sub(r"<title>", '<div class="orv_title"><h1>', line)
                html.insert(0, f"{line}</h1></div>")
            elif line.startswith("<!>"):
                line = re.sub(r"<!>", '<div class="orv_system"><p>', line)
                html.append(f"{line}</p></div>")
            elif line.startswith("<@>"):
                line = re.sub(r"<@>", '<div class="orv_constellation"><p>', line)
                html.append(f"{line}</p></div>")
            elif line.startswith("<#>"):
                line = re.sub(r"<#>", '<div class="orv_outergod"><p>', line)
                html.append(f"{line}</p></div>")
            elif line.startswith("<&>"):
                line = re.sub(r"\s*「\s*", "「 ", line)
                line = re.sub(r"\s*」\s*", " 」", line)
                line = re.sub(r"<&>", '<div class="orv_quote"><p>', line)
                html.append(f"{line}</p></div>")
            elif line.startswith("<?>"):
                line = re.sub(r"<\?>", '<div class="orv_notice"><p>', line)
                html.append(f"{line}</p></div>")
            elif line.startswith("<img>"):
                line = re.findall(r"\[(.*?)\]", line)
                html.append(
                    f'<div class="orv_image"><img src="../../../assets/images/{line[0]}" alt="{line[1]}" loading="lazy"></div>'
                )
            elif line == "":
                html.append(f"<br>")
            elif line == "***":
                html.append(f"<hr>")
            elif line.startswith("<list>"):
                line = re.sub(r"<list>", "<ul>", line)
                html.append(f"{line}")
            elif line.startswith("<cover>"):
                line = re.findall(r"\[(.*?)\]", line)
                template = template.replace(
                    r"{{COVER}}",
                    f'<div class="orv_cover"><img src="../../../assets/images/{urlparse.quote(line[0])}" alt="{line[1]}"></div>',
                )
            else:
                html.append(f'<p class="orv_line">{line}</p>')

        # Get all chapter files to determine first and last
        chapter_files = sorted([f for f in os.listdir("chapters/orv") if f.endswith(".txt")])
        chapter_numbers = [int(f.replace(".txt", "").replace("chap_", "")) for f in chapter_files]
        first_chapter_index = min(chapter_numbers) - 1
        last_chapter_index = max(chapter_numbers) - 1
        
        # Handle Previous button
        if file_index == first_chapter_index:
            template = template.replace(r"{{PREV}}", "../")
            template = template.replace(r"{{PREV-TEXT}}", "Home")
            template = template.replace(
                r"{{PREV-SVG}}",
                '<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e3e3e3"><path d="M240-200h120v-240h240v240h120v-360L480-740 240-560v360Zm-80 80v-480l320-240 320 240v480H520v-240h-80v240H160Zm320-350Z" /></svg>',
            )
        else:
            template = template.replace(r"{{PREV}}", f"ch_{file_index}")
            template = template.replace(r"{{PREV-TEXT}}", "Previous")
            template = template.replace(
                r"{{PREV-SVG}}",
                '<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e3e3e3"><path d="M400-80 0-480l400-400 71 71-329 329 329 329-71 71Z" /></svg>',
            )

        # Handle Next button
        if file_index == last_chapter_index:
            template = template.replace(r"{{NEXT}}", "../")
            template = template.replace(r"{{NEXT-TEXT}}", "Home")
            template = template.replace(
                r"{{NEXT-SVG}}",
                '<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e3e3e3"><path d="M240-200h120v-240h240v240h120v-360L480-740 240-560v360Zm-80 80v-480l320-240 320 240v480H520v-240h-80v240H160Zm320-350Z" /></svg>',
            )
        else:
            template = template.replace(r"{{NEXT}}", f"ch_{file_index+2}")
            template = template.replace(r"{{NEXT-TEXT}}", "Next")
            template = template.replace(
                r"{{NEXT-SVG}}",
                '<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e3e3e3"><path d="m321-80-71-71 329-329-329-329 71-71 400 400L321-80Z" /></svg>',
            )

        while html and (html[-1] == "<br>" or html[-1] == "<hr>"):
            html.pop()

        html.append("<br>")
        html.append("<hr>")

        template = template.replace(r"{{CONTENT}}", str("\n".join(html)))
        template = template.replace(r"{{PATH}}", f"orv/{file}")
        template = template.replace(r"{{INDEX}}", str(file_index))

        # Banner logic: First 5 chapters = Discord, Last 5 chapters = Donation, Others = Random
        import random
        
        donation_banner = '''<div class="donation-banner" style="margin: 15px auto 0; padding: 12px 15px; background-color: var(--primary); border: 1px solid var(--text-secondary); border-radius: 8px; text-align: center; max-width: 800px; color: var(--text-primary);">
            <p style="margin: 0 0 6px 0; font-size: 0.95em; line-height: 1.5;">ORV-Reader will always be <strong>AD-Free</strong> for the community. If you're enjoying the story, please consider donating!</p>
            <p style="margin: 0 0 10px 0; font-size: 0.85em; opacity: 0.75;">Just 0.1% of readers contributing would be enough to help us reach our goal.</p>
            <a href="../../../donate.html" style="display: inline-block; padding: 7px 18px; background-color: #ff5e1f; color: #fff; text-decoration: none; border-radius: 5px; font-weight: bold; font-size: 0.9em; transition: background-color 0.3s;">Support ORV-Reader</a>
        </div>'''
        
        discord_banner = '''<div class="discord-banner" style="margin: 15px auto 0; padding: 12px 15px; background-color: var(--primary); border: 1px solid var(--text-secondary); border-radius: 8px; text-align: center; max-width: 800px; color: var(--text-primary);">
            <p style="margin: 0 0 6px 0; font-size: 0.95em; line-height: 1.5;">Report issues on our <strong>Discord Server</strong> or join for discussion and new chapters!</p>
            <p style="margin: 0 0 10px 0; font-size: 0.85em; opacity: 0.75;">Connect with the community, share theories, and stay updated!</p>
            <a href="https://discord.gg/CZdNvKaNNr" target="_blank" rel="noopener noreferrer" style="display: inline-block; padding: 7px 18px; background-color: #5865F2; color: #fff; text-decoration: none; border-radius: 5px; font-weight: bold; font-size: 0.9em; transition: background-color 0.3s;">Join Discord</a>
        </div>'''
        
        # Determine which banner to show
        if current_chapter <= first_chapter + 4:  # First 5 chapters
            banner_html = discord_banner
        elif current_chapter >= last_chapter - 4:  # Last 5 chapters
            banner_html = donation_banner
        else:  # Random for middle chapters
            banner_html = random.choice([donation_banner, discord_banner, ''])
        
        template = template.replace(r"{{BANNER}}", banner_html)

        template = template.replace(r"{{TITLE}}", "")
        template = template.replace(r"{{COVER}}", "")
        template = template.replace(r"{{BANNER}}", "")
        template = template.replace(r"{{PREV}}", "")
        template = template.replace(r"{{NEXT}}", "")
        template = template.replace(r"{{PREV-SVG}}", "")
        template = template.replace(r"{{NEXT-SVG}}", "")
        template = template.replace(r"{{PREV-TEXT}}", "")
        template = template.replace(r"{{NEXT-TEXT}}", "")
        template = template.replace(r"{{INDEX}}", "")

        with open(
            f"website/stories/orv/read/ch_{file_index+1}.html", "w", encoding="utf-8"
        ) as f:
            f.write(template)
    except Exception as e:
        print(e)
        print(f"""====================\nThere was an error in \n{file}\n{file_index}====================""")
