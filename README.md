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
| `slides/` | Decks: `indico-kth-sv/` (Swedish, for KTH: design and integration) and `indico-tutorial-en/` (English: a user tutorial for meetings, lectures and conferences). Screenshots in `slides/img/` (tutorial: `slides/img/tutorial/`). Open `index.html` in a browser; `?print-pdf` for PDF. |
| `kth-doc-templates/` | Git submodule: the KTH reveal.js theme and the KTH logo used by the decks. After cloning: `git submodule update --init`. |
| `AGENTS.md` | Conventions and hard rules for contributors and AI agents. |

Not included: server configuration (kept with the deployment), the KTH logo (KTH's asset; the
decks take it from the submodule), and any personal data. CSV files and Gruppwebben exports must never be committed.

## Licence

© 2026 Christian Ohm.

- **Code** (`gruppwebb/`, `accounts/`, `branding/`, `.github/`): [MIT](LICENSE).
- **Documentation and decks** (`docs/`, `slides/`, the READMEs and `AGENTS.md`):
  [CC BY 4.0](LICENSE-docs). Credit "Christian Ohm, KTH" with a link to this repository.

Not covered by either licence:
- the KTH name, logo and visual identity, which are KTH's trademarks;
- the `kth-doc-templates` submodule, which has its own licence;
- Indico itself (MIT, CERN), which shows in the screenshots;
- the screenshots of public events in `slides/img/tutorial/public-*.png` (ESA, ETH Zürich on
  indico.global, European XFEL). The content belongs to those organisers; the screenshots are
  included with credit and a link on each slide, to illustrate how Indico is used.

The slides are published at <https://cohm.github.io/kth-indico/>.
