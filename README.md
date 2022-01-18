# nowplaypadgen

DAB+ now playing PAD (DLS+ and MOT SLS) generator

## Usage

### DL+

You can use this to generate some DLPlus Tags.

```python
>>> from nowplaypadgen.dlplus import *
>>> message = DLPlusMessage()
>>> message.add_dlp_object(DLPlusObject("STATIONNAME.LONG", "Radio Bern RaBe"))
>>> message.add_dlp_object(DLPlusObject("STATIONNAME.SHORT", "RaBe"))
>>> message.add_dlp_object(DLPlusObject("ITEM.TITLE", "Radio Bern"))
>>> message.build("$STATIONNAME.LONG")
>>> message.message
'Radio Bern RaBe'
>>> tags = message.get_dlp_tags()
>>> long = tags['STATIONNAME.LONG']
>>> f"{long}: {long.code} {long.start} {long.length}"
'STATIONNAME.LONG: 32 0 15'
>>> short = tags['STATIONNAME.SHORT']
>>> f"{short}: {short.code} {short.start} {short.length}"
'STATIONNAME.SHORT: 31 11 4'
>>> title = tags['ITEM.TITLE']
>>> f"{title}: {title.code} {title.start} {title.length}"
'ITEM.TITLE: 1 0 10'

```

Later on you might want to generate DL+ that deletes an item tag.

```python
>>> message = DLPlusMessage()
>>> message.add_dlp_object(DLPlusObject("STATIONNAME.LONG", "Radio Bern RaBe"))
>>> message.add_dlp_object(DLPlusObject("ITEM.TITLE", delete=True))
>>> message.build("$STATIONNAME.LONG")
>>> message.message
'Radio Bern RaBe'
>>> tags = message.get_dlp_tags()
>>> title = tags['ITEM.TITLE']
>>> f"{title}: {title.code} {title.start} {title.length}"
'ITEM.TITLE: 1 5 0'

```

Finally, you can render it as an [ODR-PadEnc](https://github.com/opendigitalradio/ODR-PadEnc) style string.

```python
>>> from nowplaypadgen.dlplus import *
>>> message = DLPlusMessage()
>>> message.add_dlp_object(DLPlusObject("ITEM.TITLE", "Radio Bern"))
>>> message.add_dlp_object(DLPlusObject("STATIONNAME.SHORT", "RaBe"))
>>> message.add_dlp_object(DLPlusObject("STATIONNAME.LONG", "Radio Bern RaBe"))
>>> message.build("$STATIONNAME.LONG")
>>> from nowplaypadgen.renderer.odr import ODRPadEncRenderer
>>> renderer = ODRPadEncRenderer(message)

```

This will generate the following ODR-PadEnc style DLS string when rendered with `print(renderer)`:

```
##### parameters { #####
DL_PLUS=1
DL_PLUS_TAG=1 0 10
DL_PLUS_TAG=31 11 4
DL_PLUS_TAG=32 0 15
##### parameters } #####
Radio Bern RaBe
```

## Release Management

The CI/CD setup uses semantic commit messages following the [conventional commits standard](https://www.conventionalcommits.org/en/v1.0.0/).
There is a GitHub Action in [.github/workflows/semantic-release.yaml](./.github/workflows/semantic-release.yaml)
that uses [go-semantic-commit](https://go-semantic-release.xyz/) to create new
releases.

The commit message should be structured as follows:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

The commit contains the following structural elements, to communicate intent to the consumers of your library:

1. **fix:** a commit of the type `fix` patches gets released with a PATCH version bump
1. **feat:** a commit of the type `feat` gets released as a MINOR version bump
1. **BREAKING CHANGE:** a commit that has a footer `BREAKING CHANGE:` gets released as a MAJOR version bump
1. types other than `fix:` and `feat:` are allowed and don't trigger a release

If a commit does not contain a conventional commit style message you can fix
it during the squash and merge operation on the PR.

Once a commit has landed on the `main` branch a release will be created and automatically published to [pypi](https://pypi.org/)
using the GitHub Action in [.github/workflows/pypi.yaml](./.github/workflows/pypi.yaml) which uses [twine](https://twine.readthedocs.io/)
to publish the package to pypi.

## Development

### Install requirements

```bash
make init
```

### Run Tests

```bash
make test
```

### Generate docs

```bash
make docs
```
