'''
.. py:module:: therex
    :platform: Unix
    
Interface for accessing `Thesaurus Rex <http://ngrams.ucd.ie/therex2/>`_. 
'''
import urllib2
import logging
import traceback
import operator
from unidecode import unidecode
from xml.etree import ElementTree as ET

logger = logging.getLogger('tweets.default')
THESAURUS_REX_MEMBER_URL = "http://ngrams.ucd.ie/therex2/common-nouns/member.action?member={0}&kw={0}&needDisamb=true&xml=true"
THESAURUS_REX_SHARE_URL = "http://ngrams.ucd.ie/therex2/common-nouns/share.action?word1={0}&word2={1}&xml=true"
THESAURUS_REX_CATEGORY_URL= "http://ngrams.ucd.ie/therex2/common-nouns/category.action?cate={0}%3A{1}&xml=true"

def _build_url(word1, word2 = None, category = False):
    # Convert unicode strings to normal ones as URL cannot have unicode chars.
    if type(word1) is unicode:
        word1 = unidecode(word1)
    if type(word2) is unicode:
        word2 = unidecode(word2)
        
    if category:
        return THESAURUS_REX_CATEGORY_URL.format(word1, word2)
    
    if word2 is None:
        return THESAURUS_REX_MEMBER_URL.format(word1)
    else:
        return THESAURUS_REX_SHARE_URL.format(word1, word2)
    
    
def _get_dict(element_tree, word1, word2, category = False):
    d = {}
    cat_key1 = 'Members' if category else 'Categories' 
    cat_key2 = 'Modifiers'
    cat_key3 = 'CategoryHeads'
    if word2 is not None and not category:
        cat_key2 = u'{0}->{1}'.format(word1, word2)
        cat_key3 = u'{1}->{0}'.format(word1, word2)
    d[cat_key1] = []
    d[cat_key2] = []
    d[cat_key3] = []
    for e in element_tree[0]:
        d[cat_key1].append((e.text.strip(), int(e.attrib['weight'])))
    for e in element_tree[1]:
        d[cat_key2].append((e.text.strip(), int(e.attrib['weight'])))
    for e in element_tree[2]:
        d[cat_key3].append((e.text.strip(), int(e.attrib['weight'])))       

    for k in d:
        d[k] = sorted(d[k], key = operator.itemgetter(1), reverse = True)      
    return d
        

def categories(word1, word2 = None):
    '''Query for Thesaurus Rex categories.
    
    Does a web query to http://ngrams.ucd.ie/therex2/. The search type is defined
    by the format and amount of strings used as parameter(s). The request 
    response is an XML, which is converted into a dictionary. Dictionary values 
    are lists ordered by weight of the category. Dictionary keys depend on the 
    query type.
    
    ====================    =============    ============    ====================================
    Query Type              word1 format     word2 format    Returned Dictionary Keys
    ====================    =============    ============    ====================================
    Members of category     'headCat:Cat'    None            Members, Modifiers, CategoryHeads
    Categories of a word    'str'            None            Categories, Modifiers, CategoryHeads
    Shared categories       'str1'           'str2'          Categories, str1->str2, str2->str1
    ====================    =============    ============    ====================================
    
    The keys 'str1->str2' and 'str2->str1' contain categories derived from 
    another word to another.
    
    :param word1: First word
    :type word1: str or unicode
    :param word2: Optional, second word for the shared category query.
    :type word2: str or unicode
    :returns: dict -- Dictionary object converted from XML response, or None if the web query was not successful.
    '''
    if type(word1) not in (str, unicode):
        raise TypeError("'word1' must be str or unicode. Got {}".format(type(word1)))
    if word2 is not None and type(word2) not in (str, unicode):
        raise TypeError("If specified, 'word2' must be str or unicode. Got {}".format(type(word2)))
    
    category = False
    if word2 is None and len(word1.split(":")) == 2:
        word1, word2 = word1.split(":")
        category = True
    try:
        url = _build_url(word1, word2, category = category)
        logging.info("Requesting Thesaurus Rex URL: {}".format(url))
        response = urllib2.urlopen(url).read()
        et = ET.fromstring(response)
    except Exception:
        e = traceback.format_exc()
        logger.error("Could not get Thesaurus Rex categories, because of error: {}".format(e))
        return None 
    return _get_dict(et, word1, word2, category = category)