# AGENTS.md

Guidance for AI coding agents (and humans) working in this repository.

## What this project is

Tools and material for running **[Indico](https://getindico.io)** (CERN's event and agenda
system, MIT licence) as a university service at KTH: an importer for KTH Gruppwebben meeting
series, a bulk local-account script, KTH branding for Indico's pages, and slide decks describing
how the service is designed and integrated (federated login via SWAMID/eduGAIN, organisation
structure and groups, mail, privacy). Written against Indico **v3.3.14**.

A pilot runs at `https://indico.physics.kth.se`. The goal is a central KTH service.

## Layout

| Path | What |
| --- | --- |
| `gruppwebb/` | Gruppwebben export → Indico events (`gw-schema.py`, `gw-probe.py`, `gw-import.py`); see its README |
| `accounts/make-accounts.py` | local accounts from a CSV plus a local group |
| `branding/00-kth.css` | KTH colours, Figtree, header logo for Indico's pages |
| `slides/` | reveal.js decks; shared screenshots in `slides/img/` |
| `kth-doc-templates/` | git submodule ([cohm/kth-doc-templates](https://github.com/cohm/kth-doc-templates)): the KTH reveal theme and the KTH logo, used by the decks |

## Hard rules

- **No personal data, ever.** Gruppwebben exports, attendee CSVs and Indico user lists are never
  committed, and an agent never reads them. Scripts are written from *structure* only:
  `gw-schema.py` and `gw-probe.py` reduce an export to value classes and counts, and a human
  reviews that report before sharing it. `.gitignore` blocks the obvious file types; that is a
  net, not the rule.
- **No deployment specifics.** No host IPs, internal hostnames, VPN/tailnet names, internal
  Indico category IDs, usernames, import logs, or secrets. Server configuration lives with the
  deployment, not here.
- **No secrets.** Indico's `SECRET_KEY` and SMTP credentials stay on the server. Never ask for
  them or read them.
- **The KTH logo is KTH's asset** and is not committed here. Decks take it from the
  `kth-doc-templates` submodule (each deck folder has a symlink `KTH_logo_RGB_bla.svg` into it).

## Conventions

- **Indico internals:** cite the source file and version (v3.3.14) for every selector, model or
  API used, and re-check after every Indico upgrade.
- **Server-side scripts** run inside `indico shell -r` as the `indico` user
  (`%run /opt/indico/tmp/<script> …`) and are **dry runs unless `--commit`**.
- **Commands for operators:** short (~60 characters) and paste-safe; avoid long heredocs.
- **Language:** code, comments and READMEs in English. Decks: Swedish for KTH-internal
  audiences, English for the public/general ones.
- **Decks:** one folder per deck under `slides/`, loading `kth-reveal.css`/`kth-reveal.js` from
  `../../kth-doc-templates/reveal/`. Mark the status of every integration honestly (live / agreed /
  planned / under investigation).

## Useful facts (Indico v3.3.14)

- Users created with `create_user` get no mail; people set their password via "forgot password".
- Each user's `lang` setting overrides `DEFAULT_LOCALE` (en_US shows AM/PM; use en_GB or sv).
- Import meeting series into **protected** categories only: meeting notes carry colleagues' names.
- nginx: `systemctl reload` cannot move a listener from 127.0.0.1:80 to *:80 and still exits 0;
  restart instead.
