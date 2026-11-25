"""The one place ad-network code lives (PLAN 4i/4k): swap the network here, never in a template.
Adsterra Banner 300x250 only (owner 11-24 "wire in adsterra"). No popunder, Social Bar, Smartlink or native: never added.
The ad sits in a sandboxed lazy iframe whose page is /ad-frame.html on our own domain (srcdoc hid the host from Adsterra, 0 impressions 11-25): it loads only when scrolled near, cannot push the page (fixed 250px box, so no layout shift)
and has no allow-top-navigation, so an ad cannot redirect the reader away. Kill switch: tools/tools_flags.json "ads"."""

KEY = "0dccda8a39039f244fe2fca6d9d73cb3"     # public ad-unit key (visible in any page that shows the ad), not a secret
SRC = "https://bauval.org/22/" + KEY          # script host Adsterra gave for this unit (11-24)
FRAME = ("<!doctype html><meta name=\"robots\" content=\"noindex\"><body style='margin:0'><script>atOptions={'key':'" + KEY + "','format':'iframe','height':250,'width':300,'params':{}};</script>"
         "<script data-cfasync='false' src='" + SRC + "'></script>")
SANDBOX = "allow-scripts allow-popups allow-popups-to-escape-sandbox"   # no allow-top-navigation

def ad_slot():
    """One labelled banner box. Put after a page's opening answer, never before it, never on a lookup tool."""
    return ('<aside class="adslot" aria-label="Advertisement"><p class="adlabel">Advertisement</p>'
            f'<iframe title="Advertisement" loading="lazy" width="300" height="250" scrolling="no" sandbox="{SANDBOX}" '
            'src="/ad-frame.html"></iframe></aside>')

CSS = ".adslot{margin:18px auto;text-align:center;max-width:300px}.adslot .adlabel{margin:0 0 4px;font-size:11px;color:#6b7280;letter-spacing:.04em;text-transform:uppercase}.adslot iframe{display:block;width:300px;height:250px;max-width:100%;border:0;margin:0 auto}"
