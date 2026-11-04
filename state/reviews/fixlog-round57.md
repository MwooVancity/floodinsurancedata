# Fixlog round 57

- MAJOR A1 (all pages): "with a loan" dropped the manual's "secured by the insured property". Root cause: rule text shortened the manual's scope. Fix: `wait_exceptions` now reads "with a loan secured by the insured property (making, increasing, extending or renewing it)", excerpt added. Proof: fim_check excerpt OK; rebuilt pages carry the new text.
- MAJOR T1 (tool): loan option said "refinancing" (not the manual's word). Root cause: label paraphrase. Fix: label now "making, increasing, extending or renewing it". Proof: dist label.
- MAJOR T2 (tool): contents-only coverage qualifies for the loan exception only if the contents secure the loan. Root cause: condition left out of `start_loan`. Fix: sentence added to `start_loan` with the manual's excerpt. Proof: fim_check excerpt OK.
- MAJOR T3 (tool): map results never printed the 13-month receipt limit. Root cause: limit only in a label pointer. Fix: `start_map` rule states it, and every map result ends with the 13-month sentence (JS and oracle both). Proof: test_tools oracle = page on every input in Chromium and WebKit.
