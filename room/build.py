# Assembles room/index.html from template.html + room.svg + content/slider code pulled from the main index.html.
import re,pathlib
here=pathlib.Path(__file__).parent
old=(here.parent/"classic"/"index.html").read_text()
t=(here/"template.html").read_text()
def block(name):
    m=re.search(r"^const "+name+r"=\[.*?^\];",old,re.S|re.M); return m.group(0)
data="\n\n".join(block(n) for n in ["DIGEST","NEWSLETTERS","BOOKS","PLAYLISTS","WRITING"])
arts=re.search(r"^/\* books: Artspace.*?^\.verdict small\{[^\n]*\n",old,re.S|re.M).group(0)
rb=re.search(r"^function rBooks\(el\)\{.*?^\}\n",old,re.S|re.M).group(0)
rb=rb.replace("const s=Math.max(.6,Math.min(1.05,vp.clientWidth/920));","const s=Math.max(.42,Math.min(1.05,vp.clientWidth/920,(innerHeight-520)/300));").replace("vp.style.height=maxH+52+\"px\"","vp.style.height=maxH+30+\"px\"").replace('<h2 class="arts-h"><small>Chapter<sup>3</sup></small>On the shelf</h2>',"").replace("The Dee Brief · Shelf","Dee's shelf").replace("if(!hover&&!document.hidden)","if(!hover&&!document.hidden&&arts.offsetParent)")
out=t.replace("{{ARTS_CSS}}",arts).replace("{{DATA}}",data).replace("{{RBOOKS}}",rb).replace("{{SVG}}",(here/"room.svg").read_text())
(here/"index.html").write_text(out)
(here.parent/"index.html").write_text(out)  # the room is the homepage
print("built",len(out))
