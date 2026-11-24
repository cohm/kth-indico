# kth-indico

Tools and material for running [Indico](https://getindico.io) at KTH: an importer for KTH
Gruppwebben meeting series, bulk local accounts, KTH branding, and decks describing the project.
Written against Indico **v3.3.14**.

| Path | What |
| --- | --- |
| `gruppwebb/` | Gruppwebben export → Indico events: `gw-schema.py`, `gw-probe.py` (structure and counts only, run locally), `gw-import.py` (runs in `indico shell`). See its README. |
| `accounts/make-accounts.py` | Local Indico accounts from a `first_name,last_name,email` CSV, plus a local group. Dry run unless `--commit`; sends no mail. Usage in its docstring. |
| `branding/00-kth.css` | KTH colours, Figtree font and white header logo for Indico's site, category, meeting, lecture and conference pages. Goes to `/opt/indico/custom/css/`. Selectors from the v3.3.14 source; see the file header. |
| `docs/` | Draft privacy policy template (Swedish and English) for a university Indico service; fill the `{{…}}` placeholders. |
| `slides/` | Decks describing the service and its integration: `indico-kth-sv/` (Swedish, for KTH). Screenshots in `slides/img/`. Open `index.html` in a browser; `?print-pdf` for PDF. |
| `kth-doc-templates/` | Git submodule: the KTH reveal.js theme and the KTH logo used by the decks. After cloning: `git submodule update --init`. |
| `AGENTS.md` | Conventions and hard rules for contributors and AI agents. |

Not included: server configuration (kept with the deployment), the KTH logo (KTH's asset; the
decks take it from the submodule), and any personal data. CSV files and Gruppwebben exports must never be committed.

Licence: to be decided (planned: MIT for code, CC BY 4.0 for documentation and decks).
