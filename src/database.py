import json
from dataclasses import dataclass, field
from typing import List

import os
import duolingo
import pandas as pd
from pattern import de


@dataclass
class Database():
    nouns: List[dict] = field(default_factory=list)
    verbs: List[str] = field(default_factory=list)
    adjectives: List[str] = field(default_factory=list)
    pfverbs: List[dict] = field(default_factory=list)

    def load_duolingo(self, creds_path: str = '../data/config.json') -> None:
        '''Connects to Duolingo.'''
        with open(creds_path, 'r') as js:
            credentials = json.load(js)
        username, password = credentials['username'], credentials['password']
        duo = duolingo.Duolingo(username, password)
        self.process_duolingo(duo)

    def process_duolingo(self, duo) -> None:
        '''Loads nouns, verbs, and adjectives from Duolingo.'''
        vocab = duo.get_vocabulary('de')['vocab_overview']
        words = [(w['word_string'], w['pos'], w.get(
            'gender'), w.get('infinitive')) for w in vocab]

        df = pd.DataFrame(words, columns=['word', 'pos', 'gender', 'inf'])
        df['gender'] = df['gender'].apply(
            lambda v: v[0].lower() if v else None)
        df['noun'] = df.apply(lambda v: de.singularize(
            v['word']).lower() if v['pos'] == 'Noun' else None, axis=1)

        self.verbs = [v for v in df['inf'].unique() if v]
        self.adjectives = df[df['pos'] == 'Adjective']['word'].to_list()
        self.nouns = df[df['pos'] == 'Noun'][[
            'noun', 'gender']].to_dict('records')

    def load_pfverbs_csv(self, csv_path: str = '../data/pfverbs.csv') -> None:
        '''Loads prefix verbs from a csv.'''
        df = pd.read_csv(csv_path)
        df.columns = df.columns.str.lower()
        self.pfverbs = df.to_dict('records')

    def save_vocab_json(self, vocab_path: str = '../data/vocab.json') -> None:
        '''Saves the current vocab as a json.'''
        vocab = dict(zip(['nouns', 'verbs', 'adjectives', 'pfverbs'], [
                     self.nouns, self.verbs, self.adjectives, self.pfverbs]))

        if os.path.exists(vocab_path):
            raise FileExistsError

        with open(vocab_path, 'w') as js:
            js.write(json.dumps(vocab, indent=4))

    def load_vocab_json(self, vocab_path: str = '../data/vocab.json') -> None:
        '''Loads vocab list from a json.'''
        with open(vocab_path, 'r') as js:
            vocab = json.load(js)

        self.nouns, self.verbs, self.adjectives, self.pfverbs = vocab.values()
