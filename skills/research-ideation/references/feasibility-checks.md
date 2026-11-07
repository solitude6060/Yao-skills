# Feasibility checks on the real data

Run these before committing to a topic. Each takes minutes to hours on data already at hand, and each has
stopped or redirected a topic that would otherwise have cost weeks. Write them as one script with a saved
output, so that a new session can rerun the script and diff the result.

## Checks

| Check | How | Adjust or stop when | Generic case |
|---|---|---|---|
| 1. The needed modality or field exists | Count the items that carry the field in the source the method actually reads; confirm that every method in the comparison uses it | The method, or a method the claim depends on, does not use the modality | A multimodal plan stopped when the second method turned out to use no images |
| 2. The defining counts hold | Count the population that defines the claim under the actual time and tie rules (for example, targets that are new or cold at request time) | The population is too small to carry a claim, or mostly differs from what its label says | Most targets labelled new at request time already had interactions before the request; the truly cold subset was a small fraction |
| 3. The obvious variant is not saturated | Run the cheapest version of the idea, such as a learned recombination of the existing signals at the output, and an oracle that picks the better source per query, an upper bound for source switching only (a recombination can rank a target above both sources) | The cheap variant barely moves the metric and the oracle gap is small | A learned recombination of the same signals at the output changed the metric by a few percent at most, which moved the plan to a different mechanism |
| 4. The mechanism can differ from the simpler alternative | Derive, or simulate on a small sample, whether the proposed mechanism can produce outputs the simpler alternative cannot | The two are equivalent under the model's form, so no experiment can separate them | A derivation showed that guidance through item embeddings changes scores only inside the embedding span, so it cannot reproduce the per-item bonus of late fusion; the comparison was therefore informative |
| 5. Closest and concurrent work are known | Landscape and concurrent-work modes of `research-survey` | A published work already does the same thing in the same setting | A preprint already wrote the same statistics as text into the model's input and reported that the model had to be trained to read them |
| 6. Implementation exists | Code (official or credible, revision, licence), released checkpoints and their training data, data access, the protocol each was evaluated under | An essential component cannot be reproduced | Model code, checkpoints and protocols of the candidate base models were inventoried before the preliminary route was chosen |
| 7. Resources fit | Compute, paid-API balance, and the resource restrictions in force for this topic | The first stage needs a resource the owner has not authorized | A preliminary study was planned around hosted APIs only, because the local accelerators were reserved for another project |
| 8. Inherited numbers reproduce | Rerun the script that produced the numbers the topic builds on and diff against the saved output | The numbers do not reproduce | A new topic's first command reran the inherited feasibility script and diffed it against the saved output |

## Recording

- One script computes every check; its output is saved next to it; the start document cites both.
- Each check names the research question it protects.
- A check that fails is recorded with its numbers as evidence and moves the topic to adjust or stop through
  the decision log. A failed check is never rerun with a looser definition to make it pass.
