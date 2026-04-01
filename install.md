# install

## Local development

```bash
cd /home/standart/subprojects/desktop_markdown_sync
python3 -m venv .venv
. .venv/bin/activate
make install-dev
make verify
make act-run-yellow
```

## Kali package build

```bash
cd /home/standart/subprojects/desktop_markdown_sync
make build-deb
sudo apt install ./dist/desktop-markdown-sync_0.1.0_all.deb
systemctl --user daemon-reload
systemctl --user enable --now desktop-markdown-sync.service
```

## Live sync and fixture refresh

```bash
desktop-markdown-sync export
desktop-markdown-sync daemon
desktop-markdown-sync snapshot --output .cache/live-desktop-snapshot.json
desktop-markdown-sync render-fixtures \
  --snapshot .cache/live-desktop-snapshot.json \
  --fixtures-dir fixtures
```

Rendered fixture markdown now includes source-attribution lines for layout and visible-content summaries so manual screenshot review, OCR output, and accessibility follow-up can be compared against the original KWin metadata.

## Optional smoke paths

```bash
make docker-test
make docker-harness-test
make act-run
make act-run-yellow
```

`make docker-harness-test` writes a parent-style `/home/standart` mirror, fixture-pack
sync manifest, and recorded UI demo under `artifacts/outputs/kali-harness/`.
