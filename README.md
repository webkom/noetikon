# noetikon [![Build status](https://ci.frigg.io/badges/webkom/noetikon/)](https://ci.frigg.io/webkom/noetikon/last/) [![Build status](https://ci.frigg.io/badges/coverage/webkom/noetikon/)](https://ci.frigg.io/webkom/noetikon/last/)

File organizer

```bash
$ make
  dev        - install dev requirements
  prod       - install prod requirements
  venv       - create virtualenv venv-folder
  production - deploy production (used by chewie)
```

## Development
### Mac
```bash
brew update
brew install python3 postgresql
make noetikon/settings/local.py
mkvirtualenv noetikon
make dev
```
