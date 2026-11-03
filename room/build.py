# Assembles room/index.html from template.html + room.svg + content/slider code pulled from the main index.html.
import re,pathlib
here=pathlib.Path(__file__).parent
old=(here/"_content.html").read_text()  # content source; files starting with _ are not published
t=(here/"template.html").read_text()
def block(name):
    m=re.search(r"^const "+name+r"=\[.*?^\];",old,re.S|re.M); return m.group(0)
data="\n\n".join(block(n) for n in ["DIGEST","NEWSLETTERS","BOOKS","PLAYLISTS","WRITING"])
arts=re.search(r"^/\* books: Artspace.*?^\.verdict small\{[^\n]*\n",old,re.S|re.M).group(0)
rb=re.search(r"^function rBooks\(el\)\{.*?^\}\n",old,re.S|re.M).group(0)
rb=rb.replace("const s=Math.max(.6,Math.min(1.05,vp.clientWidth/920));","const s=Math.max(.42,Math.min(1.05,vp.clientWidth/920,(innerHeight-520)/300));").replace("vp.style.height=maxH+52+\"px\"","vp.style.height=maxH+30+\"px\"").replace('<h2 class="arts-h"><small>Chapter<sup>3</sup></small>On the shelf</h2>',"").replace("The Dee Brief · Shelf","Dee's shelf").replace("if(!hover&&!document.hidden)","if(!hover&&!document.hidden&&arts.offsetParent)")
out=t.replace("{{ARTS_CSS}}",arts).replace("{{DATA}}",data).replace("{{RBOOKS}}",rb).replace("{{SVG}}",(here/"room.svg").read_text())
# Y2K bedroom fonts: map every serif / condensed face used in the shared CSS onto the site's font tokens
st=out.index("<style>"); en=out.index("</style>")
css=out[st:en]
for old,new in [('"IM Fell English SC","IM Fell English",Georgia,"Times New Roman",serif',"var(--display)"),
                ('"IM Fell English SC","IM Fell English",Georgia,serif',"var(--display)"),
                ('"IM Fell English",Georgia,serif',"var(--display)"),
                ('Oswald,"Arial Narrow",sans-serif',"var(--display)"),
                ("font-family:var(--display);font-weight:400","font-family:var(--display);font-weight:800"),
                ("font-family:var(--display);font-weight:700","font-family:var(--display);font-weight:800")]:
    css=css.replace(old,new)
out=out[:st]+css+out[en:]
(here/"index.html").write_text(out)
(here.parent/"index.html").write_text(out)  # the room is the homepage
print("built",len(out))
