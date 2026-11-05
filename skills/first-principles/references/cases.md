# First-principles — public cases

These public incidents and one research case illustrate verification habits. The
suggested checks are engineering lessons drawn from the cited reports. Private project
incidents and results are omitted from this community edition; the research case is
described without project details.

## Knight Capital — incomplete deployment

The SEC found that new code reached seven of eight servers; the remaining server
still contained callable Power Peg code. A repurposed flag activated that old
path. Removing the new code from the other servers during the response worsened
the incident. Verify the deployed revision on every target and the behavior of
any reused flag before relying on a deployment assumption.

Source: [SEC Release 34-70694, paragraphs 13–17](https://www.sec.gov/Archives/edgar/data/1569391/000119312513401173/d613486dex101.htm).

## Mars Climate Orbiter — interface units

NASA/JPL's preliminary findings identified English-unit data passed to a navigation
system expecting metric units. Check the producer's actual units against the
consumer's contract, including integration checks across team boundaries.

Source: [NASA/JPL, September 30, 1999](https://www.jpl.nasa.gov/news/mars-climate-orbiter-team-finds-likely-cause-of-loss/).

## Heartbleed — unchecked input length

OpenSSL's advisory describes a missing bounds check in the TLS heartbeat handling
that could expose process memory. Validate the length supplied by an untrusted
input against the available buffer; a library's reputation does not establish
coverage of that specific path.

Source: [OpenSSL security advisory, April 7, 2014](https://openssl-library.org/news/secadv/20140407.txt).

## Research case — inherited split, deferred protocol finding

- **Inherited assumption**: the project specification prescribed a user-disjoint split
  with a shared global time cutoff "to prevent leakage", and it was implemented as
  written.
- **First-principles trigger**: the project lead asked why evaluated users needed
  fold-in and why all users shared one cutoff.
- **What the audit found**: the trained baselines never saw the evaluation users'
  histories, so the comparison measured unseen-user (cold-start) performance, a
  different question from the one the method answers. Later, an internal audit rated a
  second protocol issue HIGH: the method's auxiliary terms used the time of the
  held-out event, which the trained baselines never received. That finding was
  deprioritized and handled by wording.
- **What happened instead of a fix**: every result under the first protocol was rerun
  under per-user leave-one-out. The deferred HIGH finding became the central objection
  of an external pre-submission review and had to be answered by new experiments
  shortly before the deadline.
- **Root-cause fix**: the split was derived from a one-sentence research question
  (`recsys-evaluation` checklist item 1); the HIGH finding was answered by a run that
  applied the same global cutoff to both sides and by an information-matched control.
- **Lesson**: an inherited protocol is an unverified assumption, and a HIGH protocol
  finding is answered by an experiment, not by moving text.
