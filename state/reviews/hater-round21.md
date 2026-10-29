# Hater review round 21: proof-of-loss deadline tool (light check)

Checked: page text and inline script of the 4 pages; the `oracle` function in tools/test_tools.py (not rerun); eCFR 44 CFR 206.112 and 44 CFR 61 App. A(1) Art. VII fetched once each on 2026-10-29.
Confirmed: 206.112(a) says the registration period is 60 days following the date of the declaration, and (b) lets FEMA extend it. Art. VII says "Within 60 days after the loss, send us a proof of loss". Counting loss date + 60 days as the last day is a fair reading of "within 60 days after".
Confirmed: `id='deadline'` appears exactly once on each of the three pages and the three tool blocks are identical; home has no `dl`/`dlo` and no "proof of loss" text. The tool sits in the "How do I actually get covered - and how fast?" card, right after the "Already flooded?" note, which is the right place. Character encoding is fine (section sign is U+00A7).

## home
- No defects. The tool is absent (0 occurrences of the deadline div, input or output element).
Verdict: PASS

## louisiana
- MINOR: heading "Flooded? Work out your claim deadline." says "claim deadline", but the date input only produces the NFIP proof-of-loss date. Reporting a claim has no 60-day date in the text, and the FEMA aid window (60 days from the declaration) is a different clock that the date input does not compute. A newcomer can read the output as "the" deadline for everything. Fix: "Flooded? Work out your NFIP proof-of-loss date."
- MINOR: output "Your NFIP proof of loss is due by ..." says "Your" to every visitor, including an uninsured reader or one with a private policy. The private-policy sentence above mitigates this. Fix: "If you have an NFIP policy, your proof of loss is due by ..."
- MINOR: past-date output "The 60-day NFIP proof-of-loss date was ... Contact your insurer now." does not say the insurer can extend the date (FEMA often does after declared disasters). It could alarm a reader at day 70 who does not know that. The tool never says that the date can be extended, while the aid sentence does. Fix: add "Your insurer may have extended it." to the past-date sentence.
- MINOR: "NFIP" is not spelled out inside the tool block (check the card above defines it). The tool says "private (non-NFIP)" before the reader has met the term.
- MINOR: "due by ... (N days from today)" is correct for "within 60 days after the loss" (last day = loss date + 60). Not a defect, but the tool gives no hint that the day counts from the loss and not from today. The label "Date the water came in:" covers it.
- No legal-advice or promise wording found. "Contact your insurer now" is an instruction to act, not a guarantee. Both rule sentences match the eCFR text. Future date, bad date and empty input are handled calmly.
Verdict: PASS

## palm-beach-county-fl
- Same tool block, byte-identical to louisiana; the MINOR items above apply unchanged.
- MINOR: on a county page, the FEMA aid sentence is generic ("for your area"), so a reader may think it says their county is declared. The sentence is conditional ("If the President declares ..."), so it is not false.
Verdict: PASS

## broward-county-fl
- Same tool block, byte-identical to louisiana; the MINOR items above apply unchanged.
- MINOR: same generic "for your area" aid sentence as palm-beach-county-fl.
Verdict: PASS
