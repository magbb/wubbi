# Wubbi

Wubbi is a web service providing quick access to the lexicon of the Referenzkorpus Altdeutsch 1.0 (Old High German and Old Saxon, released under CC BY-NC-SA 3.0 DE), including token-level annotations. The corpus was downloaded from the Laudatio Repository (https://doi.org/10.34644/laudatio-dev-xyV0DnMB7CArCQ9CuAeJ) and converted from ELAN XML into a PostgreSQL database. The converted corpus is provided here as well under the same license as the original.

Searching is as simple as entering a word form. Due to the rich graphematic variation in medieval manuscripts and the transcription principles of editorial practice, the search is fuzzy be default. Enclose the word in quotation marks to do an exact search: "uuortes". Search for the word forms of a certain lemma by prefixing it with @: @wort. You can also search via New High German, by using =: =Wort. Be warned, however, that this might be considered as cheating. :)

# Installation instructions
1. Load Postgres database from data directory (e.g. with psql)
2. pip install -r requriements.txt
3. cp webapp/config.example webapp/config.py and and add credentials
3. python run.py

# License
CC BY-NC-SA 3.0

Magnus Breder Birkenes, 2018
