This repository will hold tools or resources useful (to me at least :) ) for text processing.

Currently it contains a list of word frequencies. The data was obtained from the [Google Ngram dataset] ( http://storage.googleapis.com/books/ngrams/books/datasetsv2.html)

The specific data used here comes from the set of English 1-grams from 2012-07-01, with the following cleanup:

* Only files for the letters of the alphabet were used:
  - http://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-1gram-20120701-a.gz
  - http://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-1gram-20120701-b.gz
  - ...
  - http://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-1gram-20120701-z.gz
* Only counts for lowercase words from the last available year, 2008, were used, with this filter:
   ```
   grep "^[a-z]*.2008" |sed -e 's/2008.\([0-9]*\)[^0-9].*$/\1/g'
   ```
* Some remaining noise was further removed with this filter:
   ```
   egrep -v "^[^0-9]*$|[A-Z]"
   ```
* The results for each letter were concatenated into a single file.


<a rel="license" href="http://creativecommons.org/licenses/by/3.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/3.0/88x31.png" /></a><br />This repository as well as the Google N-gram compilation are licensed under the <a rel="license" href="http://creativecommons.org/licenses/by/3.0/">Creative Commons Attribution 3.0 Unported License</a>. To view a copy of this license, visit http://creativecommons.org/licenses/by/3.0/ or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

