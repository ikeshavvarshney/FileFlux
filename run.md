# FileFlux CLI Tool - Commands Reference

## Standard Commands

* `ffx info <file>`  
  Show detailed info about a file or directory.
* `ffx copy <src> <dst>`  
  Copy file or directory.
* `ffx cut <src> <dst>`  
  Move file or directory.
* `ffx delete <path>`  
  Delete a file or directory.
* `ffx mkdir <path>`  
  Create a new directory.
* `ffx rename <src> <dst>`  
  Rename a file or directory.
* `ffx save <alias> <path>`  
  Save a frequently used path with an alias.
* `ffx jump <alias>`  
  Jump to a previously saved path.
* `ffx unsave <alias>`  
  Remove a saved path alias.
* `ffx showpaths`  
  List all saved path aliases.

## File Searching

* `ffx search --text <query> [--ext <ext>] [path]`  
  Search for a text string inside files. Defaults to current directory.
* `ffx search <pattern> [path]`  
  Search for files by name (substring match).

## File Listing

* `ffx ls [path]`  
  List all files in a directory (defaults to current directory) in a colored, structured format with name, size, and type.

## Archive & Extraction

* `ffx archive <src> [dst]`  
  Archive a file or folder into a `.zip` file.
* `ffx extract <src> [dst]`  
  Extract a `.zip` archive to the specified destination.

## Conversion

* `ffx convert --json <src> [dst]`  
  Convert a text file into JSON format.
* `ffx convert --txt <src> [dst]`  
  Convert a JSON file into plain text.

## Fuzzy Search

* `ffx fzf [path]`  
  Interactively browse and select files using FZF or fallback terminal interface.

## Password Manager

* `ffx pass <alias> <password>`  
  Store a password for an alias.
* `ffx pass <alias>`  
  Retrieve the password for an alias and copy it to the clipboard.

## Version & Help

* `ffx -v` or `ffx --version`  
  Show the current version.
* `ffx -h` or `ffx --help`  
  Show help and description of the tool.
