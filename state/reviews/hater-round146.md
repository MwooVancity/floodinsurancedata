# Hater round 146 (light): screen-1 reorder, 390x844, rendered in Chromium

Checked: order of tiles / map button / quick answers / compare line, DOM vs HEAD (text unchanged), screen-1 contents.
Worked: answers now come in a sensible order (risky, required, cost, start, payout, flooded, pay less, quote); the reorder itself is right.
Broke: the compare line was moved without its antecedent.

## home
- Unchanged: `git diff HEAD -- dist/index.html` is empty. No new defect.
Verdict: PASS

## louisiana
- **MAJOR** Dangling "That" (label-vs-context, checklist D/N). The compare line "That is 5% above the U.S. median of $1,066; 16th highest of the 50 states and DC." now follows the quick-answer list, so its nearest antecedent is the last item, "Is my quote normal? Type it in to compare with existing policies here (not a quote)." The reader reads "That is ..." as the quote or the last answer. Before, it sat directly under the tiles, which it describes. The sentence carries no figure of its own. It sits at y=1218 on a 390x844 screen (tiles at y~200), about 1.5 screens below the figure it describes. Check that should have caught it: a gate that the first sentence after the answer list does not begin with a bare pronoun ("That", "it") with no figure in the same sentence.
- MINOR Screen 1 (844px) now shows tiles, the map button, "Am I required" and the start of "Cost in my zone?" (y=733) and "How fast" (y=820). Good order. The state list has no "How risky" or "Can I pay less" item, unlike counties (not a change; GAP at most).
- MINOR "Pick your parish" renders with a disclosure-style triangle but is a plain label with a jump link under it, so it looks like a collapsed control. Nothing is hidden.
Verdict: FAIL

## palm-beach-county-fl
- **MAJOR** Dangling "That" (label-vs-context, checklist D/N). The compare line "That is 32% below the Florida median of $985 and 37% below the U.S. median of $1,066; 8th lowest of 55 Florida counties with 100+ priced policies." now follows the quick-answer list, so its nearest antecedent is the last item, "Is my quote normal? Type it in to compare with existing policies here (not a quote)." The reader reads "That is ..." as the quote or the last answer. Before, it sat directly under the tiles, which it describes. The sentence carries no figure of its own. It sits at y=1436 on a 390x844 screen (tiles at y~200), about 1.7 screens below the figure it describes. Check that should have caught it: a gate that the first sentence after the answer list does not begin with a bare pronoun ("That", "it") with no figure in the same sentence.
- MINOR Screen 1 shows only "How risky" and "Am I required" (the Citizens clause makes it ~210px). "Cost in my zone?" starts at y=864, just below the fold. The $673 tile covers cost; the order is sensible.
- "By ZIP it ranges" has no subject either (same defect).
Verdict: FAIL

## new-york-county-ny
- **MAJOR** Dangling "That" (label-vs-context, checklist D/N). The compare line "That is 19% below the New York median of $1,261 and 4% below the U.S. median of $1,066; 11th lowest of 48 New York counties with 100+ priced policies." now follows the quick-answer list, so its nearest antecedent is the last item, "Is my quote normal? Type it in to compare with existing policies here (not a quote)." The reader reads "That is ..." as the quote or the last answer. Before, it sat directly under the tiles, which it describes. The sentence carries no figure of its own. It sits at y=1352 on a 390x844 screen (tiles at y~200), about 1.5 screens below the figure it describes. Check that should have caught it: a gate that the first sentence after the answer list does not begin with a bare pronoun ("That", "it") with no figure in the same sentence.
- MINOR Screen 1 shows how risky, am I required, and the "Cost in my zone?" heading (y=801) with one line visible. Order is sensible. (No ZIP line on this page.)
Verdict: FAIL

## dixie-county-fl
- **MAJOR** Dangling "That" (label-vs-context, checklist D/N). The compare line "That is within one percent of the Florida median of $985 and 7% below the U.S. median of $1,066; 25th highest of 55 Florida counties with 100+ priced policies." now follows the quick-answer list, so its nearest antecedent is the last item, "Is my quote normal? Type it in to compare with existing policies here (not a quote)." The reader reads "That is ..." as the quote or the last answer. Before, it sat directly under the tiles, which it describes. The sentence carries no figure of its own. It sits at y=1436 on a 390x844 screen (tiles at y~200), about 1.7 screens below the figure it describes. Check that should have caught it: a gate that the first sentence after the answer list does not begin with a bare pronoun ("That", "it") with no figure in the same sentence.
- MINOR "Cost in my zone?" starts at y=885, below the fold, because the Florida Citizens clause in "Am I required" is long. "By ZIP it ranges" has no subject either (same defect).
Verdict: FAIL

## levy-county-fl
- **MAJOR** Dangling "That" (label-vs-context, checklist D/N). The compare line "That is 65% above the Florida median of $985 and 53% above the U.S. median of $1,066; 4th highest of 55 Florida counties with 100+ priced policies." now follows the quick-answer list, so its nearest antecedent is the last item, "Is my quote normal? Type it in to compare with existing policies here (not a quote)." The reader reads "That is ..." as the quote or the last answer. Before, it sat directly under the tiles, which it describes. The sentence carries no figure of its own. It sits at y=1448 on a 390x844 screen (tiles at y~200), about 1.7 screens below the figure it describes. Check that should have caught it: a gate that the first sentence after the answer list does not begin with a bare pronoun ("That", "it") with no figure in the same sentence.
- MINOR "Cost in my zone?" starts at y=855, just below the fold. "By ZIP it ranges" has no subject either (same defect).
Verdict: FAIL

## sonoma-county-ca
- **MAJOR** Dangling "That" (label-vs-context, checklist D/N). The compare line "That is 20% above the California median of $1,055 and 19% above the U.S. median of $1,066; 12th highest of 42 California counties with 100+ priced policies." now follows the quick-answer list, so its nearest antecedent is the last item, "Is my quote normal? Type it in to compare with existing policies here (not a quote)." The reader reads "That is ..." as the quote or the last answer. Before, it sat directly under the tiles, which it describes. The sentence carries no figure of its own. It sits at y=1352 on a 390x844 screen (tiles at y~200), about 1.5 screens below the figure it describes. Check that should have caught it: a gate that the first sentence after the answer list does not begin with a bare pronoun ("That", "it") with no figure in the same sentence.
- MINOR Screen 1 shows how risky, am I required and the "Cost in my zone?" heading with part of its line (y=801). Order is sensible. "By ZIP it ranges" has no subject either (same defect).
Verdict: FAIL

## wakulla-county-fl
- **MAJOR** Dangling "That" (label-vs-context, checklist D/N). The compare line "That is 49% above the Florida median of $985 and 38% above the U.S. median of $1,066; 5th highest of 55 Florida counties with 100+ priced policies." now follows the quick-answer list, so its nearest antecedent is the last item, "Is my quote normal? Type it in to compare with existing policies here (not a quote)." The reader reads "That is ..." as the quote or the last answer. Before, it sat directly under the tiles, which it describes. The sentence carries no figure of its own. It sits at y=1499 on a 390x844 screen (tiles at y~200), about 1.8 screens below the figure it describes. Check that should have caught it: a gate that the first sentence after the answer list does not begin with a bare pronoun ("That", "it") with no figure in the same sentence.
- MINOR "Cost in my zone?" starts at y=885, below the fold. "By ZIP it ranges" has no subject either (same defect).
Verdict: FAIL

## Classes
- County and state template: the compare line ("That is X% above/below ... median") begins with a bare "That" and now follows the answer list; the ZIP line ("By ZIP it ranges") has the same subject-less pattern. Fix: give the sentence its own subject (e.g. "The median of $673 is 32% below ...", built with the number helpers), or move it back under the tiles.
- Florida county template: the Citizens clause in "Am I required" pushes "Cost in my zone?" below the fold at 844px.
