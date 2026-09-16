# GitHub Gadgets (GHG)

A Python TUI app, packed with GitHub automation gadgets. All in your terminal.

---

TODO:

1. Add session for connections

2. Add a few lightweight, random requests between the main requests to break up consecutive repeated requests and potentially reduce the risk of being flagged or banned.

3. Use a temp file like a global variable for holding data such as my_followers, my_following, etc; If it exists, then use it instead.
<br>Since those data can be large, I suggest using a simple text file instead of global variables, because variables are in RAM and the files are on disk

---

There are some issues with token management and tokens username extraction.
The first release will be just a MVP, and more professional methods will replace the old ones in future versions.
It also includes other configuration adjustments.
