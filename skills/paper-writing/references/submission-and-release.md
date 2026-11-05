# Submission package and release

Checks for the last stage before a paper leaves the project: the page gate, venue compliance, the anonymous
code release, bilingual editions and build delivery. Each rule comes from a near miss in one submission
cycle; the venue details below are examples, so read the current call of the target venue every time.

## Page limit is a build gate

- A build over the content-page or total-page limit is not a submission candidate, however good its text.
  Compile after every change that adds words or floats and record the page count with the commit.
- Count what the call counts: content pages, references, appendix and the total of a single PDF. Some calls
  desk-reject a PDF over the total.
- When a cut is needed, apply the body-versus-appendix tests ([body-appendix.md](body-appendix.md)) before
  shortening sentences.

## Venue compliance from the current call

Read the call and the publisher's author policies in full for each submission, record the version or date
read, and check every item below. Search the full text of the paper before reporting an item as missing; a
statement can sit in a section other than the one expected.

| Item | Check |
|---|---|
| Format | Template, document class options, fonts, page size, anonymity of the author block and metadata |
| Track statement | When the call requires it, the first page states the paper's relation to the venue's theme or the chosen track, in the place and wording the call allows |
| AI-use statement | A short statement of what AI tools were used for (for example code implementation and language polishing), that the authors set the questions, protocol and analyses and take responsibility; placed where the call or publisher policy allows |
| Reference format | The bibliography style and any required reference-format block |
| Supplementary material | Whether a separate file is accepted or everything goes into one PDF |
| Preprint policy | Whether an anonymous preprint may be posted or must be cited, and any rules on its title or timing |
| Concurrent submission | A paper under review at one venue is not submitted to another at the same time; a fallback venue is a later plan, not a parallel one |
| Code availability | Whether code may be linked during review, and how the link must be anonymized |

## Double-blind code release

1. Build the release in a separate, clean repository; never publish the working repository.
2. Include only what the paper needs to reproduce its results: no private paths, user names, account
   names, internal documents or plans, datasets or experiments that are not in the paper, and no result
   numbers or tuned settings in the README beyond what the paper states.
3. Check that the necessary parts are present: data preparation, the method, the evaluation, the commands
   to reproduce each table, and a license or terms file with anonymous authorship.
4. Scan the full history of the release repository (not only the last commit) for names, paths, accounts,
   keys and the venue name; commit as an anonymous author.
5. After the anonymous mirror updates, list its files and compare each file's hash with the release commit.
   A mirror that still serves an older commit is updated and checked again.
6. While the review is anonymous, do not add real names to a repository that an anonymous mirror copies.
7. Place the code link where strong papers at the target venue place it; check the abstract and introduction
   of recent accepted papers there.

## Preprints

Before posting a preprint during review: check the call's preprint policy and the publisher's, build the
preprint without the venue name or template marks that identify the submission, confirm that every
co-author agrees, and note that a posted preprint and its license cannot be withdrawn.

## Bilingual editions

- Every edit lands in both editions in one change; the editions share numbers, tables and terms.
- Figure text, legends and captions are in each edition's language.
- Terms in the text match the labels of the main table.
- Each edition is compiled and its page count recorded; one edition over the limit blocks the package.

## Build delivery

- Every build is delivered with the commit it was built from, to one fixed location, in each edition.
- Deliver only the newest build; a build older than changes the author already saw is never delivered.
- Pages, result tables and the paper that show the same numbers are published together from the same commit.

## Generic cases

- A draft over a total-page limit that the call enforces by desk rejection was nearly treated as a
  candidate.
- A compliance check reported a missing AI-use statement that was in another section; only the appendix had
  been searched.
- The anonymous mirror served an older commit than the release repository until it was refreshed and
  compared file by file.
