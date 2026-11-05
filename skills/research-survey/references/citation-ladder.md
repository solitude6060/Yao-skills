# Citation ladder

Reviewers who find one citation that credits a source with content it does not contain stop trusting every
other citation. Each reference therefore climbs three steps, and only the third step admits it to the paper.

## The three steps

| Step | Check | Evidence recorded | Typical failure |
|---|---|---|---|
| 1. Exists | Resolve the identifier (DOI, arXiv id, proceedings page) | Resolver result and the date checked | A fabricated or mistyped reference |
| 2. Metadata correct | Compare authors, title, venue, year and pages with the resolver or the publisher page | The corrected entry | Wrong year, venue or author list; a preprint cited after its venue version appeared |
| 3. Claim present | Find the cited claim in the source's full text | A short quote with section and page | The source does not say what the sentence credits it with; a term attributed to a source that does not use it |

A reference at step 1 or 2 may sit in a reading list. In the paper, a sentence that cites it either reaches
step 3 or loses the citation.

## Record per citation

```markdown
| Key | Sentence in the paper (location) | Step reached | Quote and location in the source | Fix |
|---|---|---|---|---|
```

## Conceptual sources for method components

Before a component of the method is described as new, search for the same principle in earlier work (the
same estimator, weighting scheme, interpolation or decomposition under another name). Cite what is found as
the conceptual source and state the difference. A component with no conceptual source is described as a
design choice with its reason.

Generic cases: a weighting scheme was invented locally until the owner asked for its conceptual source, and
an established method with the same principle was cited instead; a well-known method was credited with a
term it does not use.

## Pre-submission pass

- Check every entry in the bibliography, not only the new ones.
- Run the pass in a fresh context, by a reader who did not write the citing sentences.
- Record the corrections; a generated bibliography is regenerated from its source, never hand-edited.
- Resolver queries carry no personal data: no email in polite-pool parameters, no names or tokens in
  headers, whatever the API convention suggests.

Generic case: a reference-verification lane placed the owner's email in a bibliographic API's polite-pool
parameter; the rule above now goes into every task card that queries external services.
