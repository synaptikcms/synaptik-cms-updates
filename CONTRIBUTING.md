# Contributing a Language Pack

Thank you for taking the time to translate SynaptikCMS. This guide explains everything you need to do to get your language listed on the [Language Packs page](https://synaptikcms.com/language-packs/).

---

## Before you start

- Check [`translations.json`](./translations.json) to make sure your language is not already listed.
- If it is listed but outdated or broken, you can still open a PR to update it.
- SynaptikCMS already ships with **English (`en`)**, **French (`fr`)** and **Spanish (`es`)** — those don't need to be contributed here.

---

## Step 1 — Get the source files

The English files are the reference. Copy them from the main CMS repository:

```
lang/front/en.json   →  public site strings
lang/admin/en.json   →  admin panel strings
```

You can browse them here:  
[github.com/synaptikcms/synaptik-cms/tree/main/lang](https://github.com/synaptikcms/synaptik-cms/tree/main/lang)

---

## Step 2 — Translate

Rename the files to your locale code (e.g. `de.json`, `pt_BR.json`, `ja.json`) and translate the values. Do not change the keys.

```json
{
    "read_more": "Weiterlesen",
    "published_on": "Veröffentlicht am",
    ...
}
```

A few rules:

- Keep every key that exists in `en.json` — missing keys fall back to English at runtime, but complete translations are preferred.
- If a string contains a placeholder like `%s` or `%d`, keep it in your translation.
- Do not translate the `_meta` block (language code, display name) — leave that to step 3.

---

## Step 3 — Package the ZIP

Create a ZIP with this exact structure:

```
lang-{locale}.zip
├── front/
│   └── {locale}.json
└── admin/
    └── {locale}.json
```

Example for German:

```
lang-de.zip
├── front/
│   └── de.json
└── admin/
    └── de.json
```

Both files are required. A ZIP containing only one of the two will not be listed.

---

## Step 4 — Host the ZIP

The ZIP must be publicly downloadable. The simplest option is to attach it to a release in this repository:

1. Go to [Releases](https://github.com/synaptikcms/synaptik-cms-updates/releases) → **Draft a new release**
2. Tag: `lang-{locale}-{version}` (e.g. `lang-de-1.0.0`)
3. Title: `German language pack 1.0.0`
4. Attach your ZIP
5. Publish the release
6. Copy the direct download URL of the ZIP asset

You can also host it anywhere else (your own server, another GitHub repo, etc.) as long as the URL is stable and publicly accessible without authentication.

---

## Step 5 — Add your entry to `translations.json`

Fork this repository, open `translations.json`, and add your language:

```json
{
    "de": {
        "name": "German",
        "native": "Deutsch",
        "author": "YourGitHubUsername",
        "author_url": "https://github.com/YourGitHubUsername",
        "version": "1.0.0",
        "download_url": "https://github.com/synaptikcms/synaptik-cms-updates/releases/download/lang-de-1.0.0/lang-de-1.0.0.zip"
    }
}
```

| Field | Required | Description |
|---|---|---|
| `name` | Yes | Language name in English (e.g. `"German"`) |
| `native` | No | Language name in the language itself (e.g. `"Deutsch"`) — shown as a subtitle on the card |
| `author` | Yes | Your name or GitHub username |
| `author_url` | No | Link to your GitHub profile or website |
| `version` | Yes | Your pack version, starting at `1.0.0` |
| `download_url` | Yes | Direct URL to the ZIP file |

The locale key (e.g. `"de"`) must match the filename you used for the JSON files. Use the standard ISO 639-1 two-letter code, or a regional variant like `pt_BR` for Brazilian Portuguese.

---

## Step 6 — Open a pull request

Open a PR against the `main` branch of this repository. The title should be:

```
Add {Language} translation — {locale}
```

Example: `Add German translation — de`

In the PR description, mention:

- Which locale code you used
- Whether both `front` and `admin` files are included
- Anything the reviewer should know (partial translation, dialect, etc.)

---

## Updating an existing translation

If you are updating a translation that already exists (fixing strings, adding missing keys after a CMS update), follow the same steps. Increment the `version` field in your `translations.json` entry and attach the new ZIP to a new release.

---

## Questions

Open a discussion on the main CMS repo: [github.com/synaptikcms/synaptik-cms/discussions](https://github.com/synaptikcms/synaptik-cms/discussions)
