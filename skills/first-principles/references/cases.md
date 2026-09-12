# First-principles — public cases

These public incidents illustrate verification habits. The suggested checks are
engineering lessons drawn from the cited reports. Private project incidents and
results are omitted from this community edition.

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
