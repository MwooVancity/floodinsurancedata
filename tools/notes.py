"""How-it-is-counted notes: one home each, on /methodology/#<key>; a page card links there with how(key) instead of
repeating the paragraph (hater r5: half of every county page's prose was the same notes; google_gate S13 measures it).
A caveat a reader needs beside the figure (not a quote, not adjusted for inflation, not your home) stays on the page."""
# Google Analytics (this site's own property, owner 2026-10-30). Real host only: gate and phone runs never count as visits
# and never wait on Google. /privacy/ discloses it.
GA_TAG = ('<script>if(location.hostname=="floodinsurancedata.com"){window.dataLayer=window.dataLayer||[];'
          'window.gtag=function(){dataLayer.push(arguments)};gtag("js",new Date());gtag("config","G-EXCYW0PJYG");'
          'var s=document.createElement("script");s.async=true;s.src="https://www.googletagmanager.com/gtag/js?id=G-EXCYW0PJYG";'
          'document.head.appendChild(s)}</script>')
NOTES = {
    "zones": ("Policy units by flood zone",
              "Insured units by the flood zone each policy is rated in; a condo-building policy counts each of its units."),
    "zip": ("ZIP codes",
            "A ZIP median is shown when the ZIP has 25 or more priced single-family policies; otherwise the lookup gives its "
            "policy count. Policy units also count condo units, so they can be far more than the priced policies. Each town "
            "name is the Census place with the largest share of that ZIP code area."),
    "averages": ("Why published prices differ",
                 "Published figures rarely say which measure they are, or which year. Policies renew on their own "
                 "anniversaries, so the latest term year shows where renewals are heading. Private flood insurance is not in "
                 "FEMA's data."),
    "rebuild": ("Rebuilding cost and the building limit",
                "Rebuilding cost is the replacement-cost figure on single-family primary-home policies that report one. Many "
                "owners insure to the building maximum even when that figure is lower, so the two shares measure different "
                "things. The damage share counts every paid claim with a damage figure, all building types."),
    "unpaid": ("Claims closed without payment",
               "The building non-payment reason on each NFIP claim closed with nothing paid, every claim counted once. "
               "“Assigned in error” and “Other” are FEMA's own labels; some closed claims are paperwork, "
               "not a denied flood."),
    "events": ("Flood events",
               "Paid NFIP claims grouped by the flood event FEMA assigned (FEMA's name). A catch-all "
               "label spanning many years gets its own row; floods with too few paid claims here to count as one flood (see the card) are not listed. Event totals include code-upgrade (ICC) payments, "
               "which the yearly totals leave out."),
    "claims": ("Claims by year",
               "Net building and contents payments by year of loss. Claims are matched by the claims dataset's county code, "
               "which may not exactly match a policy's property county."),
    "multiloss": ("Repeat-flood records",
                  "One home appears once for each declared disaster that damaged it, so the count is damage events on "
                  "repeat-flooded homes, not distinct homes (FEMA says these records cannot be totaled by property). "
                  "Disaster-aid records since 2002, separate from NFIP insurance claims."),
    "declarations": ("Disaster declarations",
                     "Distinct storms by calendar year: one storm's emergency and major-disaster declarations are counted "
                     "once, not each declaration record."),
    "nri": ("FEMA's National Risk Index",
            "The rating is FEMA's modeled expected flood loss, adjusted for social vulnerability and community resilience, "
            "compared across counties (coastal and inland flooding are rated separately). Because it weighs "
            "vulnerability and resilience, and a place with many valuable buildings can have a large total loss but a low "
            "loss per dollar, the rating and the loss percentile can differ. Any loss figure is a whole-county model of all "
            "flood loss, insured or not, averaged per year, so it runs far above insurance payouts; it is never one home's "
            "expected loss or premium."),
}

def how(key, base="../../"):
    assert key in NOTES, key
    return f' <a class="how" href="{base}methodology/#{key}">How this is counted</a>'
