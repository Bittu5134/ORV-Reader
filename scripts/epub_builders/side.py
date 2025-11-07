import datetime
import re
import os
import urllib.parse as urlparse


titles = []
for file_index, file in enumerate(os.listdir("chapters/side")):
    with open(f"./chapters/side/{file}", "r", encoding="utf-8") as f:
        titles.append(f.readline().strip()[7:])

print(len(titles))


with open("./epub/side/OEBPS/toc.ncx", "w", encoding="utf-8") as f:
    f.write(
        """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN" "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd"><ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <head>
    <meta name="dtb:uid" content="ZJMZQD0TZGYJ"/>
    <meta name="dtb:depth" content="1"/>
    <meta name="dtb:totalPageCount" content="0"/>
    <meta name="dtb:maxPageNumber" content="0"/>
  </head>
  <docTitle><text> orv</text></docTitle><navMap>"""
    )

    for index, title in enumerate(titles):
        f.write(
            f"""\n<navPoint id="{index}" playOrder="{index+1}"><navLabel><text>{title}</text></navLabel><content src="ch_{index+1}.xhtml"/></navPoint>"""
        )
    f.write("""\n</navMap></ncx>""")


with open("./epub/side/OEBPS/toc.html", "w", encoding="utf-8") as f:
    f.write(
        """<?xml version="1.0" encoding="utf-8" standalone="no"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  <title>Table of Contents</title>
</head>
<body>
  <h2>Table of Contents</h2>
  <hr class="line-index" />
  <div id="chapters">\n"""
    )
    for index, title in enumerate(titles):
        f.write(f"""<p>{index+1}. <a href="ch_{index+1}.xhtml">{title}</a></p>\n""")
    f.write("""</div></body></html>""")


with open("./epub/side/OEBPS/content.opf", "w", encoding="utf-8") as f:
    f.write(
        f"""<?xml version="1.0" encoding="UTF-8" ?> 
<package xmlns="http://www.idpf.org/2007/opf" version="2.0">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
    <dc:title>Omniscient Reader's Viewpoint [Side Stories]</dc:title>
    <dc:creator opf:role="aut">singNshong</dc:creator> 
    <dc:contributor opf:role="trl">Community Translators</dc:contributor> 
    <dc:language>en</dc:language>
    <dc:publisher>ORV-Reader Project</dc:publisher> 
    <dc:date>{datetime.datetime.now().strftime("%m-%d-%Y")}</dc:date>
    <dc:description>Collection of short stories released after the completion of the main novel, and can be read anytime after completing the main story.</dc:description>
    <meta name="cover" content="cover-img"/>
    <dc:subject>Korean Novel</dc:subject>
    <dc:subject>Fantasy</dc:subject>
    <dc:subject>Webnovel</dc:subject>
    <dc:subject>Apocalypse</dc:subject>
    <meta property="file-as" id="title-sort">Omniscient Reader's Viewpoint [Side Stories]</meta> 
    <meta property="file-as" id="author-sort">singNshong</meta>
  </metadata>
  <manifest>
    <item href="toc.ncx" id="ncx" media-type="application/x-dtbncx+xml"/>
    <item href="toc.html" id="toc" media-type="application/xhtml+xml"/>
    <item id="cover-img" href="cover.jpg" media-type="image/jpeg" properties="cover-image"/>
    <item id="stigma" href="stigma.png" media-type="image/png"/>
    <item href="intro.xhtml" id="intro" media-type="application/xhtml+xml"/>
    <item id="afterword" href="afterword.xhtml" media-type="application/xhtml+xml"/>\n"""
    )

    for index, title in enumerate(titles):
        f.write(
            f"""<item href="ch_{index+1}.xhtml" id="{index+1}" media-type="application/xhtml+xml"/>\n"""
        )

    # for file_index, file in enumerate(os.listdir("epub/side/OEBPS/images")):
    #     f.write(
    #         f"""<item id="img_{file_index}" href="{urlparse.quote(file)}" media-type="image/jpeg"/>\n"""
    #     )

    f.write("""</manifest><spine toc="ncx">\n""")
    f.write(f"""<itemref idref="intro"/><itemref idref="toc"/>\n""")

    for index, title in enumerate(titles):
        f.write(f"""<itemref idref="{index+1}"/>\n""")
    f.write(
        """<itemref idref="afterword"/>
</spine>
  <guide>
    <reference href="cover.jpg" title="Cover" type="cover"/>
    <reference type="toc" href="toc.html" title="Table of Contents"/>
  </guide>
</package>"""
    )

for file_index, file in enumerate(os.listdir("chapters/side")):
    with open(f"./chapters/side/{file}", "r", encoding="utf-8") as f:
        xhtml = """<?xml version="1.0" encoding="utf-8"?><!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops"><head><title></title></head><body>\n"""
        notes = []
        note_index = 0
        isWindow = False
        isWindowTitle = False
        lines = f.read()
        lines = lines.replace("<!>", "")
        lines = lines.replace("<#>", "")
        lines = lines.replace("<@>", "")
        lines = lines.replace("<&>", "")

        lines = lines.splitlines()
        lines.reverse()
        while lines[0] == "" or lines[0] == "***":
            lines.pop(0)
        lines.reverse()

        for line_index, line in enumerate(lines):

            if line.startswith("<title>"):
                if lines[line_index + 1].startswith("<cover>"):
                    cover_img = re.findall(r"\[(.*?)\]", lines[line_index + 1])
                    xhtml += f"""<img style="display:block;margin:auto;height:100%;width:auto;page-break-after: always; break-after: page;" alt="cover" src="images/{urlparse.quote(cover_img[0])}"/><br/><br/>\n"""

                xhtml += '<img style="display:block;margin:auto" alt="icon" src="stigma.png"/>'
                xhtml += f'<h2 style="text-align:center;">{line[7:].strip()}</h2>\n'
                xhtml += "<hr/>\n"

            elif line.startswith("<cover>"):
                pass

            elif line == "***":
                xhtml += "<hr/>\n"
            elif line == "":
                xhtml += "<br/>\n"
            elif line.startswith("<img>"):
                line = re.findall(r"\[(.*?)\]", line)
                xhtml += f"""<img style="display:block;margin:auto;height:100%;width:auto" src="images/{urlparse.quote(line[0])}"/><br/><br/>\n"""
            elif line.startswith("<?>"):
                line = line.replace("<?>", "").strip()
                if line.startswith("["):
                    line = line[4:]
                note_index += 1
                xhtml += f"""<a href="#note{note_index}" epub:type="noteref">[NOTE {note_index}]</a>"""
                notes.append(
                    f"""<aside id="note{note_index}" epub:type="footnote"><p>Note [{note_index}]: {line}</p></aside>"""
                )

            elif line == "+":
                if isWindow == False:
                    xhtml += "<fieldset>\n"
                    isWindow = True
                    isWindowTitle = True
                elif isWindow == True:
                    xhtml += "</fieldset>\n"
                    isWindow = False
            
            elif isWindow == True and isWindowTitle == True:
                if line.startswith("[") or line.startswith("<"):
                    xhtml += f'<h3 style="text-align:center;">{line.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")}</h3>\n'
                else:
                    xhtml += f"<p>{line.strip().replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")}</p>\n"
                isWindowTitle = False

            else:
                xhtml += f"<p>{line.strip().replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")}</p>\n"
        xhtml += f"""<hr/><p style="text-align: center;"><a href="https://orv.pages.dev/stories/side/read/ch_{file_index+1}#comments" target="_blank" style="font-weight: bold; text-decoration: none;">[CLICK TO READ CHAPTER COMMENTS]</a></p>\n"""
        xhtml += (
            "<hr/><section epub:type='endnotes' role='doc-endnotes'>\n"
            + "\n".join(notes)
            + "\n</section>\n"
        )
        xhtml += """</body></html>"""
        with open(
            f"./epub/side/OEBPS/ch_{file_index+1}.xhtml", "w", encoding="utf-8"
        ) as outf:
            outf.write(xhtml)
