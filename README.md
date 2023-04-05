# sumrepo

Turn a Github link into a "One Pager" that describes the architecture of the codebase, similar to how https://architecturenotes.co/ does.

### Usage

```bash
python3 main.py
```

Note that you need to put your OpenAI API in a env.py file as `API_KEY`.

### TODOs
- [x] Find more ways to decrease amount of dirs and files that are checked (ignore .DS_Store, etc.)
- [x] Feed Chat the File Path and File Name, alongside the code of the file and ask it to use that to understand architecture.
- [x] Turn per file summarize into "One Pager" by asking Chat to do so.
- [x] Fails when it sees some binary files, don't download them
- [ ] Watch for token size going past 4k and don't try it the summary it does
- [ ] Multi-thread
- [ ] Use github api to get the list of files and folders
- [ ] Dig up other ways to make this realistic for large codebases