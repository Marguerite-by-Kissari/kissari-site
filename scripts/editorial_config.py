"""Strict shared data contract for the isolated M15 prototype."""
import copy
import json
import re
from urllib.parse import unquote,urlsplit

FIELDS={'title','enabled','article_paths'}
def load_json(text):
    if len(text.encode('utf-8'))>2*1024*1024:raise ValueError('Fichier JSON trop volumineux')
    def unique(pairs):
        out={}
        for k,v in pairs:
            if k in out:raise ValueError('Clé JSON en double : '+k)
            out[k]=v
        return out
    return json.loads(text,object_pairs_hook=unique,parse_constant=lambda x:(_ for _ in ()).throw(ValueError('Constante JSON interdite')))

def validate_field(key,value):
    if key=='title':
        if not isinstance(value,str) or any(c in value for c in '\r\n'):raise ValueError('Le titre doit être un texte sur une ligne')
        value=value.strip()
        if not 1<=len(value)<=100:raise ValueError('Le titre doit compter de 1 à 100 caractères')
    elif key=='enabled':
        if type(value) is not bool:raise ValueError('enabled doit être un booléen')
    elif key=='article_paths':
        if not isinstance(value,list) or len(value)>100:raise ValueError('Liste d’articles invalide')
        if any(not isinstance(p,str) for p in value):raise ValueError('Adresse d’article invalide')
        if len(set(value))!=len(value):raise ValueError('Article sélectionné en double')
        for p in value:
            u=urlsplit(p);decoded=unquote(p)
            if len(p)>2048 or not p.startswith('/blog/') or not p.endswith('/') or u.scheme or u.netloc or u.query or u.fragment or '\\' in decoded or '//' in decoded or any(x in ('.','..') for x in decoded.split('/')):
                raise ValueError('Adresse relative du blog attendue : '+p)
    else:raise ValueError('Champ interdit : '+str(key))
    return copy.deepcopy(value)

def validate_config(data):
    if not isinstance(data,dict) or set(data)!={'schema_version',*FIELDS} or type(data['schema_version']) is not int or data['schema_version']!=1:raise ValueError('Configuration ou version inconnue')
    return {'schema_version':1,**{k:validate_field(k,data[k]) for k in FIELDS}}

def validate_patch(data):
    if not isinstance(data,dict) or set(data)!={'schema_version','base_config_sha256','changes'} or type(data['schema_version']) is not int or data['schema_version']!=1:raise ValueError('Format d’export inconnu')
    if not isinstance(data['base_config_sha256'],str) or not re.fullmatch('[a-f0-9]{64}',data['base_config_sha256']):raise ValueError('Empreinte de référence invalide')
    changes=data['changes']
    if not isinstance(changes,dict) or not changes:raise ValueError('Aucune modification à intégrer')
    return {'schema_version':1,'base_config_sha256':data['base_config_sha256'],'changes':{k:validate_field(k,v) for k,v in changes.items()}}
