#!/usr/bin/env bash
set -euo pipefail

rm -rf FIN-Kieran
rm -rf ./*.epub
cp -r RAWs/Kieran-backup/ FIN-Kieran/
for i in $(seq -w 1 551); do
	# Copy the ripped source to the final OEBPS folder
	cp RAWs/RIP-Webnovel/OEBPS/00${i}-*.html FIN-Kieran/OEBPS/chap_00${i}.xhtml
	# Make sure files have a final EOL
	[[ -n "$(tail -c1 FIN-Kieran/OEBPS/chap_00${i}.xhtml)" ]] && echo >> FIN-Kieran/OEBPS/chap_00${i}.xhtml;
done

rm -rf FIN-Kieran-illustr
cp -r ./FIN-Kieran ./FIN-Kieran-illustr

# Remove .opf entries for the images that will not be used
sed -i '/[1-3]\.jpg/d' ./FIN-Kieran/OEBPS/content.opf

./scripts/replace.sh "FIN-Kieran"
./scripts/replace.sh "FIN-Kieran-illustr" "illustrated"

if [[ ${1:-default} != "nopack" ]] && [[ ${1:-default} != "packKieran" ]]; then
	./scripts/pack-all.sh
fi
if [[ ${1:-default} == "packKieran" ]]; then
	./scripts/pack-kieran.sh
fi
