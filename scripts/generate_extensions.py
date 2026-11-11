import json
import os
import re
import sys
import urllib.error
import urllib.request

OWNER = 'synaptikcms'
SOURCES = {
    'plugins': 'synaptik-cms-plugins',
    'themes': 'synaptik-cms-themes',
}
TAG = re.compile(r'^(?P<slug>[a-z0-9_-]+)-v(?P<version>\d+(?:\.\d+)*)$')
TARGET = 'extensions.json'
MANIFESTS = {'plugins': 'plugin.json', 'themes': 'theme.json'}
META_FIELDS = ('name', 'description', 'author', 'author_url', 'info_url', 'demo_url', 'icon', 'color')
PREVIEWS = ('preview.jpg', 'preview.jpeg', 'preview.png', 'preview.webp')


def version_key(version):
    return tuple(int(part) for part in version.split('.'))


def api(url):
    request = urllib.request.Request(url, headers={
        'Accept': 'application/vnd.github+json',
        'User-Agent': 'synaptik-extensions-registry',
        'Authorization': 'Bearer ' + os.environ.get('GITHUB_TOKEN', ''),
    })
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def fetch_releases(repo):
    releases = []
    for page in range(1, 11):
        try:
            batch = api('https://api.github.com/repos/%s/%s/releases?per_page=100&page=%d' % (OWNER, repo, page))
        except urllib.error.HTTPError as error:
            if error.code == 404 and page == 1:
                return None
            raise
        releases.extend(batch)
        if len(batch) < 100:
            break
    return releases


def raw_url(repo, tag, path):
    return 'https://raw.githubusercontent.com/%s/%s/%s/%s' % (OWNER, repo, tag, path)


def raw_request(url, method):
    request = urllib.request.Request(url, method=method, headers={'User-Agent': 'synaptik-extensions-registry'})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.read() if method == 'GET' else b''
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return None
        raise


def fetch_meta(section, repo, slug, version):
    tag = '%s-v%s' % (slug, version)
    body = raw_request(raw_url(repo, tag, '%s/%s' % (slug, MANIFESTS[section])), 'GET')
    if body is None:
        return {}
    try:
        manifest = json.loads(body)
    except ValueError:
        return {}
    meta = {key: manifest[key] for key in META_FIELDS if isinstance(manifest.get(key), str) and manifest[key]}
    for name in PREVIEWS:
        url = raw_url(repo, tag, '%s/%s' % (slug, name))
        if raw_request(url, 'HEAD') is not None:
            meta['preview'] = url
            break
    return meta


def latest_by_slug(releases):
    best = {}
    for release in releases:
        if release.get('draft') or release.get('prerelease'):
            continue
        match = TAG.match(release.get('tag_name', ''))
        if not match:
            continue
        asset = next((a for a in release.get('assets', []) if a.get('name', '').endswith('.zip')), None)
        if asset is None:
            continue
        slug, version = match.group('slug'), match.group('version')
        if slug not in best or version_key(version) > version_key(best[slug][0]):
            best[slug] = (version, asset['browser_download_url'])
    return best


def main():
    with open(TARGET, encoding='utf-8') as handle:
        data = json.load(handle)
    before = json.dumps(data, sort_keys=True)

    for section, repo in SOURCES.items():
        releases = fetch_releases(repo)
        if releases is None:
            print('%s: repository not found, skipped' % repo)
            continue
        for slug, (version, url) in latest_by_slug(releases).items():
            entries = data.setdefault(section, {})
            current = entries.get(slug)
            if current and version_key(current.get('version', '0')) > version_key(version):
                continue
            if current and current.get('version') == version and 'name' in current:
                continue
            entry = dict(current or {})
            entry['version'] = version
            entry['download_url'] = url
            entry.update(fetch_meta(section, repo, slug, version))
            entries[slug] = entry
            print('%s/%s -> %s' % (section, slug, version))

    if json.dumps(data, sort_keys=True) == before:
        print('No change.')
        return 0

    with open(TARGET, 'w', encoding='utf-8') as handle:
        json.dump(data, handle, indent=4, ensure_ascii=False)
        handle.write('\n')
    return 0


if __name__ == '__main__':
    sys.exit(main())
