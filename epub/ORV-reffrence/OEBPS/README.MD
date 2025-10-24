Repo for OMV EPUB files

This is based on webnovel.com[2021-02] and series.naver.com[2020-03-22].

For webnovel.com, there are a lot of consistency and some typo/grammar replacements, as per `word-replace.json` and `replace.sh`.

The replacements were based on the initial word-replace.txt list, but have been since very heavily modified.

Trying to use the word-replace.json used for this project against Webnovel.com or any other source may not work properly, as we heavily modify the sources.

For naver.com there are no replacements, it's as ripped.

CI builds the final EPUBs (clean source and replaces), if you are not doing edits, you can just build manually via:
```bash
./scripts/pack-all.sh
```

Cleanup, prepare and pack ripped Webnovel by Flameish/Novel-Grabber and Naver by walking around the DRM:
```bash
./scripts/prepare.sh
```

Notes:
* The brackets used throughout:『』「」[] () ⸨⸩</p>
