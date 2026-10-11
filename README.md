# ⚡ Leech Dot Bot

<div align="center">

<img src="assets/codedots-leechdot.svg" alt="Leech Dot Bot — CodeDots" width="100%"/>

**A Telegram leech/mirror bot project**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Made by](https://img.shields.io/badge/Made%20by-%40Code__Dots-7c5cff?style=flat-square)](https://t.me/Code_Dots)
[![Partner](https://img.shields.io/badge/Partner-%40CodeRips-22c7d6?style=flat-square)](https://t.me/CodeRips)

**Made by [@Code_Dots](https://t.me/Code_Dots) · Partner: [@CodeRips](https://t.me/CodeRips)**

</div>

---

## About

Leech Dot Bot is a Code_Dots-branded Telegram automation project for transferring user-authorized files, with a focus on a consistent interface, maintainable code, and reliable task handling.

> **Status:** Branding and documentation have been refreshed. Runtime behavior and bug fixes still require source-level review and test results; this page does not claim every bug has already been fixed.

## Project goals

- Consistent Leech Dot / CodeDots branding and assets.
- Clear configuration and deployment instructions.
- Reliable task lifecycle, progress updates, cancellation, and actionable error reporting.
- Keep tokens, API hashes, session strings, and database credentials in private environment variables.
- Profile bottlenecks before changing concurrency or upload/download behavior.
- Add regression tests for configuration, task state, batch processing, and file naming.

## Source and attribution

The intended upstream reference is [abhinai2244/CBML](https://github.com/abhinai2244/CBML). This rebrand credits **[@Code_Dots](https://t.me/Code_Dots)** as maker and **[@CodeRips](https://t.me/CodeRips)** as partner.

Before redistributing imported source, preserve upstream copyright/license notices and verify that the license permits your intended use. Do not remove third-party attribution. The upstream authors are not represented as endorsing this rebrand.

## Configuration safety

Use the repository's configuration template and private hosting secrets. Never commit bot tokens, Telegram API hashes, user session strings, database URLs, cloud keys, or cookies. When startup fails, inspect the complete traceback and verify required setting names before changing code.

## Validation checklist

- [ ] Review modules and map commands to implementations.
- [ ] Clean-install dependencies and run syntax/import checks.
- [ ] Validate required configuration and startup/shutdown behavior.
- [ ] Test single-file and batch tasks, cancellation, retries, and progress.
- [ ] Test large-file handling against the actual Telegram account/API limits.
- [ ] Profile slow stages and verify improvements with repeatable tests.
- [ ] Validate Docker/hosting startup commands and health checks.
- [ ] Document each confirmed fix with reproducible evidence.

## Credits

- **Made by:** [@Code_Dots](https://t.me/Code_Dots)
- **Partner:** [@CodeRips](https://t.me/CodeRips)
- **Upstream reference:** [abhinai2244/CBML](https://github.com/abhinai2244/CBML)

---

<div align="center">**LEECH DOT · CODEDOTS**<br/>Redesigned with care. Fixes should be backed by tests.</div>
