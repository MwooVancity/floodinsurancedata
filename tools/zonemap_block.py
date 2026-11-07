"""The address tool's HTML, shared by county pages and the /flood-zone-map/ hub (one source, one look).
Without JavaScript it is a plain link to FEMA's map. With JavaScript, tapping it loads Leaflet and
/zonemap.js (about 50 KB gzipped) only then, so screen 1 stays light. Law and disclaimer text only via rule()."""
MSC = "https://msc.fema.gov/portal/home"

LOADER = """<script>(function(){var b=document.getElementById('zm');if(!b)return;var o=b.querySelector('.zm-open'),u=b.querySelector('.zm-ui'),busy=0;
function js(s){return new Promise(function(r,j){var e=document.createElement('script');e.src=s;e.onload=r;e.onerror=j;document.head.appendChild(e)})}
o.addEventListener('click',function(e){e.preventDefault();u.hidden=false;o.hidden=true;b.querySelector('.zm-addr').focus();if(busy)return;busy=1;
var c=document.createElement('link');c.rel='stylesheet';c.href='/vendor/leaflet.css';document.head.appendChild(c);
js('/vendor/leaflet.js').then(function(){return js('/zonemap.js')}).then(function(){window.__zmStart(b)}).catch(function(){b.querySelector('.zm-out').innerHTML='<p>The map did not load. <a href="""+'"'+MSC+'"'+""">Use FEMA\\'s map</a>.</p>'})})})();</script>"""

def block(rule):
    return (f'<div class="zm" id="zm"><a class="btn zm-open" href="{MSC}" rel="noopener" target="_blank">Find your flood zone on FEMA\'s map →</a>'
            f'<div class="zm-ui" hidden><label for="zm-a"><b>Street address, city and state</b></label>'
            '<input id="zm-a" class="zm-addr" autocomplete="street-address" enterkeyhint="search" style="width:100%;min-height:44px">'
            '<p><button type="button" class="btn zm-go">Find it on FEMA\'s map</button> <button type="button" class="zm-loc" style="min-height:44px">Use my location</button></p>'
            '<p class="mut">Your address goes to the Census Bureau\'s address finder and the map point to FEMA\'s map service, not to this site.</p>'
            '<div class="zm-map" style="height:320px;display:none"></div><div class="zm-out" aria-live="polite"></div>'
            f'<div class="zm-label" hidden><p class="mut">FEMA\'s map, not an official determination. {rule("fema_asis")}</p></div>'
            f'</div></div>{LOADER}')
