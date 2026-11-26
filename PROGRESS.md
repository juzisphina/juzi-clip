# Progress — 橘子存片 JuziClip (juzisphina edition of ClipSaver)

Copied from apps/clip-saver at v0.7.2 (2026-11-26). Same engine; different look, language and names.
Keep skot-chen/clip-saver untouched — changes here do not go back there.

## What differs from ClipSaver
- Name 橘子存片 / JuziClip, repo juzisphina/juzi-clip, Pages juzisphina.github.io/juzi-clip, bundle io.github.juzisphina.juziclip.
- Port 8796 and ping id 'juziclip', so it can run next to ClipSaver on one computer.
- Look: light and warm (cream, white cards, warm-brown text), orange gradient buttons; themes 甜橙 (default) / 蜜桃 / 薰衣草. Colors follow the juzisphina profile (#FFD7A8 → #FFB074 → #FF8A65, #FF8C42).
- Language: 繁體 (default) / 简体, no English. Messages are written in 简体; clipsaver/hant.py makes 繁體 with Taiwan wording (影片, 網路, 連結, 設定, 連接埠, 逾時…). Add new phrases there when new text appears.
- Icon: the user's X+loop logo in white on a peach→coral tile (tools/build_icon.py a --final). Option b (an orange) was drawn and not chosen.

## Release
Push a new `v*` tag. Push as juzisphina: `GH_TOKEN=$(gh auth token --user juzisphina)`; commit author `juzisphina <358831323+juzisphina@users.noreply.github.com>`.

## Released
- v1.0.1 (2026-11-26): first public release. v1.0.0 build failed (smoke test still looked for "ClipSaver"; Mac job never got a runner and was cancelled after 15 min) - fixed and re-tagged.
