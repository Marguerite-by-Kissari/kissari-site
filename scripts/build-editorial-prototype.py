"""Build the integrated M15 atelier, its catalogue and the Hugo site."""
from pathlib import Path
import argparse,base64,json,mimetypes,re,subprocess,tempfile
from editorial_config import load_json,validate_config
ROOT=Path(__file__).resolve().parents[1]
ASSETS=['images/logo-kissari.png','images/separation-visuel-tight.png','images/cloudseeders-monogram.png','images/blog/guillemets.png','images/blog/photo-femme.png','images/blog/photo_casserole.png','images/blog/photo_lemuriens.png','images/blog/homme_lunettes.png','images/Femme.png']
def uri(path):return 'data:'+(mimetypes.guess_type(path.name)[0] or 'application/octet-stream')+';base64,'+base64.b64encode(path.read_bytes()).decode()
def build(out):
    subprocess.run(['hugo','--source',str(ROOT),'--destination',str(out),'--baseURL','http://127.0.0.1:1335/'],check=True)
def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--destination',type=Path,default=ROOT/'public');args=parser.parse_args()
    validate_config(load_json((ROOT/'data/blog_editorial.json').read_text()))
    stage=Path(tempfile.mkdtemp(prefix='m15-catalogue-',dir=Path.home()/'.hermes/cache/scratch'));build(stage)
    cat=load_json((stage/'blog/catalogue-editorial.json').read_text())
    folder=ROOT/'static/atelier-article';source=folder/'atelier-source.html'
    if not source.exists():
        html=(folder/'index.html').read_text()
        html=re.sub(r'<style>.*?</style>','',html,flags=re.S)
        html=re.sub(r'<script>.*?</script>','',html,flags=re.S)
        html=re.sub(r'<!-- KISSARI Atelier standalone:[^>]*-->\s*','',html)
        html=html.replace('<main class="workspace">',(folder/'editorial-panel.html').read_text()+'\n<main id="article-panel" class="workspace" role="tabpanel" aria-labelledby="tab-article">')
        source.write_text(html)
    html=source.read_text();css=(folder/'app.css').read_text()+'\n'+(folder/'editorial.css').read_text()
    for font in ['Poppins-Regular.ttf','Poppins-Bold.ttf','Poppins-ExtraBold.ttf']:
        data=uri(ROOT/'static/fonts'/font)
        for prefix in ['/fonts/','../fonts/']:
            for q in ["'",'"','']:css=css.replace('url('+q+prefix+font+q+')','url("'+data+'")')
    assets={p:uri(ROOT/'static'/p) for p in ASSETS}
    def jsjson(data):return json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
    scripts='window.ATELIER_ASSETS='+jsjson(assets)+';window.KISSARI_EDITORIAL_CATALOG='+jsjson(cat)+';\n'+(folder/'publication-date.js').read_text()+'\n'+(folder/'app.js').read_text()+'\n'+(folder/'editorial.js').read_text()+'\n'+(folder/'connected-preview.js').read_text()+'\n'+(folder/'publication-ui.js').read_text()
    html=html.replace('</head>','<style>'+css+'</style>\n</head>').replace('</body>','<script>'+scripts+'</script>\n</body>')
    (folder/'index.html').write_text(html)
    deliverables=ROOT/'livrables';deliverables.mkdir(exist_ok=True)
    portable=deliverables/'atelier-editorial-kissari-autonome.html';portable.write_text(html)
    (deliverables/'catalogue-editorial.json').write_text(json.dumps(cat,ensure_ascii=False,indent=2)+'\n')
    build(args.destination)
    assert (args.destination/'atelier-article/index.html').read_bytes()==portable.read_bytes()
    print('PORTABLE:',portable);print('SITE:',args.destination);print('ARTICLES:',len(cat['articles']))
if __name__=='__main__':main()
