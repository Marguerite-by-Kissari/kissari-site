"""Contact page acceptance: direct email and LinkedIn, no form or sending service."""
from pathlib import Path
from html.parser import HTMLParser
import subprocess,tempfile,unittest
ROOT=Path(__file__).resolve().parents[1]
class Tags(HTMLParser):
    def __init__(self,text):super().__init__();self.tags=[];self.feed(text)
    def handle_starttag(self,tag,attrs):self.tags.append((tag,dict(attrs)))
class ContactTests(unittest.TestCase):
    def test_contact_links_replace_form(self):
        with tempfile.TemporaryDirectory(prefix='kissari-contact-test-',dir=Path.home()/'.hermes/cache/scratch') as d:
            r=subprocess.run(['hugo','--source',str(ROOT),'--destination',d,'--baseURL','https://kissari.com/'],capture_output=True,text=True)
            self.assertEqual(r.returncode,0,r.stderr)
            page=Path(d)/'contact/index.html'
            self.assertTrue(page.is_file())
            html=page.read_text();p=Tags(html)
            info=[a for t,a in p.tags if t=='details' and a.get('id')=='contact-privacy-info']
            self.assertEqual(len(info),1)
            self.assertTrue(any(t=='summary' and a.get('aria-label')=='Informations sur le traitement de vos données' for t,a in p.tags))
            notice="contact@kissari.fr traite les informations de ce formulaire pour répondre à votre demande et suivre nos échanges, sur la base de l'intérêt légitime née de votre demande de contact, et, ou, d'informations. Les champs marqués d’un astérisque sont nécessaires à remplir, l’absence d'information adaptée dans ces champs rend la demande impossible à traiter. Pour connaître les destinataires, la conservation et vos droits, consultez dpo@kissari.fr."
            self.assertIn(notice,html)
            self.assertTrue(any(t=='script' and '/js/contact-info.js?' in a.get('src','') for t,a in p.tags))
            self.assertEqual(sum(t=='h1' for t,a in p.tags),1)
            self.assertEqual(sum(t=='footer' for t,a in p.tags),1)
            self.assertFalse(any(t in ('form','input','textarea') for t,a in p.tags),'The old contact form is still rendered')
            buttons=[a for t,a in p.tags if t=='button']
            self.assertEqual(len(buttons),1)
            self.assertEqual(buttons[0].get('class'),'mobile-nav-toggle')
            self.assertEqual(buttons[0].get('type'),'button')
            self.assertEqual(buttons[0].get('aria-controls'),'primary-navigation')
            links=[a for t,a in p.tags if t=='a']
            self.assertEqual(sum(a.get('href')=='mailto:contact@kissari.fr' for a in links),1)
            linkedin=[a for a in links if a.get('href')=='https://www.linkedin.com/company/kissari/home/']
            self.assertEqual(len(linkedin),1)
            self.assertIn('noopener',linkedin[0].get('rel',''))
            self.assertTrue(any(t=='img' and a.get('src','').endswith('/images/contact/linkedin.svg') for t,a in p.tags))
            self.assertTrue(any(t=='img' and a.get('src','').endswith('/images/contact/email.svg') for t,a in p.tags))
            self.assertNotIn('contact-channel-label',html)
            self.assertNotIn('email :</span>',html)
            self.assertNotIn('linkedin :</span>',html)
            self.assertIn('class="contact-channel-list"',html)
            self.assertIn('KISSARI sur linkedin',html)
            self.assertIn('class="contact-response-note"',html)
            self.assertIn('Votre message sera',html)
            self.assertNotIn('Merci, votre message est',html)
            self.assertIn('entre de bonnes mains !',html)
            self.assertIn('On met tout en œuvre pour vous répondre sous 48 h.',html)
            self.assertIn('Et s’il y a le feu au lac, appelez-nous au',html)
            self.assertIn('06 64 10 13 35',html)
            self.assertIn('tel:+33664101335',[a.get('href') for a in links])
            self.assertLess(html.index('id="contact-linkedin"'),html.index('class="contact-response-note"'))
            self.assertLess(html.index('class="contact-response-note"'),html.index('<footer'))
            for stale in ['Objet du message','id="contact-message"','Envoyer le message','600 mots','Envoi non activé','contact-confirmation','js/contact.js']:
                self.assertNotIn(stale,html)
            self.assertNotIn('Site KISSARI-Fomulaire.png',html)
            for t,a in p.tags:
                if t in ('img','script','link'):
                    src=a.get('src') if t!='link' else a.get('href')
                    if src and src.startswith('/'):
                        self.assertTrue((Path(d)/src.split('?',1)[0].lstrip('/')).is_file(),src)
if __name__=='__main__':unittest.main(verbosity=2)
