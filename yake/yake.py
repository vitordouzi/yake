# -*- coding: utf-8 -*-

"""Main module."""

import string
import os
import jellyfish
import Levenshtein

from datarepresentation import DataCore

class YakeKeywordExtractor(object):

    def __init__(self, lan="en", n=3, dedupLim=0.8, dedupFunc='levenshtein', windowsSize=2, top=20, features=None):
        self.lan = lan

        dir_path = os.path.dirname(os.path.realpath(__file__))
        # root_path = os.path.dirname(dir_path)
        # root_path = dir_path
        
        local_path = os.path.join("StopwordsList", "stopwords_%s.txt" % lan[:2].lower())
        resource_path = os.path.join(dir_path,local_path)
        try:
            with open(resource_path, encoding='utf-8') as stop_fil:
                self.stopword_set = set( stop_fil.read().lower().split("\n") )
        except:
            print('Warning, read stopword list as ISO-8859-1')
            with open(resource_path, encoding='ISO-8859-1') as stop_fil:
                self.stopword_set = set( stop_fil.read().lower().split("\n") )


        self.n = n
        self.top = top
        self.dedupLim = dedupLim
        self.features = features
        self.windowsSize = windowsSize
        if dedupFunc == 'jaro_winkler' or dedupFunc == 'jaro':
            self.dedu_function = self.jaro
        elif dedupFunc.lower() == 'sequencematcher' or dedupFunc.lower() == 'seqm':
            self.dedu_function = self.seqm
        else:
            self.dedu_function = self.levs

    def jaro(self, cand1, cand2):
        return jellyfish.jaro_winkler(cand1, cand2 )
    def levs(self, cand1, cand2):
        return 1.-jellyfish.levenshtein_distance(cand1, cand2 ) / max(len(cand1),len(cand2))
    def seqm(self, cand1, cand2):
        return Levenshtein.ratio(cand1, cand2)
    
    """def extract_keywords(self, text):
        text = text.replace('\n\t',' ')
        dc = DataCore(text=text, stopword_set=self.stopword_set, windowsSize=self.windowsSize, n=self.n)
        dc.build_single_terms_features(features=self.features)
        dc.build_mult_terms_features(features=self.features)
        resultSet = []
        for cand in dc.candidates.values():
            if cand.isValid():
                cand_to_replace = None
                max_cand = None
                for (i,(h, candResult)) in enumerate(resultSet):
                    if max_cand == None or max_cand[0] < h:
                        max_cand = (h, i)
                    if candResult.H >= cand.H:
                        dist = self.dedu_function(cand.unique_kw, candResult.unique_kw)
                        if dist > self.dedupLim and (cand_to_replace == None or cand_to_replace[0] < dist):
                            cand_to_replace = ( dist, i, candResult )
                if cand_to_replace != None:
                    resultSet[cand_to_replace[1]] = (cand.H, cand)
                elif len(resultSet) != self.top:
                    resultSet.append( (cand.H, cand) )
                elif max_cand[0] >= cand.H:
                    resultSet[max_cand[1]] = (cand.H, cand)
        resultSet = sorted(resultSet, key=lambda c: c[0])
        return [ (h,cand.unique_kw) for (h,cand) in resultSet]"""
    
    def extract_keywords_on(self, text):
        text = text.replace('\n\t',' ')
        dc = DataCore(text=text, stopword_set=self.stopword_set, windowsSize=self.windowsSize, n=self.n)
        dc.build_single_terms_features(features=self.features)
        dc.build_mult_terms_features(features=self.features)
        resultSet = []
        todedup = sorted([cc for cc in dc.candidates.values() if cc.isValid()], key=lambda c: c.H)
        if self.dedupLim >= 1.:
            return ([ (cand.H, cand.unique_kw) for cand in todedup])[:self.top]
        for cand in todedup:
            toadd = True
            for (h, candResult) in resultSet:
                dist = self.dedu_function(cand.unique_kw, candResult.unique_kw)
                if dist > self.dedupLim:
                    toadd = False
                    break
            if toadd:
                resultSet.append( (cand.H, cand) )
            if len(resultSet) == self.top:
                break
        return [ (h,cand.unique_kw) for (h,cand) in resultSet]
