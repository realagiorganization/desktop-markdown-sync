# DEVPLAN

- [x] Scaffold the standalone subproject with docs, Makefile, tests, `.deb` packaging, and GitHub Actions.
- [x] Keep the existing fixture/OCR workflow integrated instead of dropping it during standalone bootstrap.
- [x] Add two-way Markdown sync commands alongside snapshot/render-fixture commands.
- [x] Add a Kali Docker harness with a parent-style `/home/standart` mirror and fixture-pack sync.
- [x] Record a fixture-pack UI demo video and publish it from GitHub Actions artifacts.
- [ ] Exercise the daemon on a live Kali Plasma session and confirm Markdown edits safely rename/reselect desktops.
- [ ] Expand the reconstruction layer to move matching windows and relaunch richer app intents.
- [ ] Refresh the fixture set after material workspace changes and expand accessibility collection once AT-SPI is enabled.
- [ ] Tighten the runtime apply path to reconcile live windows more deterministically than launch-only replay.
- [ ] Raise unit coverage above the warning threshold so the warning path becomes exceptional instead of routine.
