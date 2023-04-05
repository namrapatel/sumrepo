# sumrepo

Turn a Github link into a "One Pager" that describes the architecture of the codebase, similar to how https://architecturenotes.co/ does.

### Usage

```bash
python3 main.py
```

Note that you need to put your OpenAI API in a env.py file as `API_KEY`.

### TODOs
- [x] Find more ways to decrease amount of dirs and files that are checked (ignore .DS_Store, etc.)
- [ ] Feed Chat the File Path and File Name, alongside the code of the file and ask it to use that to understand architecture.
- [ ] Turn per file summarize into "One Pager" by asking Chat to do so.
- [ ] Fails when it sees some binary files