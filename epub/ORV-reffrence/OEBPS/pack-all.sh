#!/usr/bin/env bash
set -euo pipefail

if [[ ${1-} == "CI" ]]; then
	./scripts/pack-kieran.sh CI
else
	./scripts/pack-kieran.sh
fi

cd RAWs/RIP-Webnovel
zip -X -r "../../Omniscient Reader's Viewpoint - Sing-shong (singsyong)-clean.epub" mimetype OEBPS META-INF
cd ../..

# Naver fix for Apple Books
if [[ ${1-} == "CI" ]]; then
	sed -i 's,&nbsp;, ,g' RAWs/RIP-Naver/Vol*/OEBPS/text/*.xhtml # Replace nbsp tags with a space
fi

for i in {1..8}; do
	# Copy shared files
	if [[ ${i} -ne 1 ]]; then
		cp -R RAWs/RIP-Naver/Vol1/META-INF RAWs/RIP-Naver/Vol${i}/
		cp -R RAWs/RIP-Naver/Vol1/OEBPS/css RAWs/RIP-Naver/Vol${i}/OEBPS/
		cp RAWs/RIP-Naver/Vol1/OEBPS/*.ttf RAWs/RIP-Naver/Vol${i}/OEBPS/
		cp RAWs/RIP-Naver/Vol1/OEBPS/images/icon.png RAWs/RIP-Naver/Vol1/OEBPS/images/list_title.png RAWs/RIP-Naver/Vol1/OEBPS/images/pattern.png \
			RAWs/RIP-Naver/Vol1/OEBPS/images/titlepage800.png RAWs/RIP-Naver/Vol1/OEBPS/images/munpia-logo.png RAWs/RIP-Naver/Vol${i}/OEBPS/images/
		cp RAWs/RIP-Naver/Vol1/mimetype RAWs/RIP-Naver/Vol${i}/
	fi
	cd RAWs/RIP-Naver/Vol${i}
	zip -X -r "../../../Omniscient Reader's Viewpoint - Sing-shong (singsyong)-NaverVol${i}.epub" mimetype OEBPS META-INF
	# Cleanup shared files
	if [[ ${i} -ne 1 ]]; then
		rm OEBPS/*.ttf
		rm -rf META-INF
		rm -rf OEBPS/css
		rm OEBPS/images/icon.png OEBPS/images/list_title.png OEBPS/images/pattern.png \
			OEBPS/images/titlepage800.png OEBPS/images/munpia-logo.png
		rm mimetype
	fi
	cd -
done
