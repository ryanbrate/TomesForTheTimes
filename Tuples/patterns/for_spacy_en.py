"""
Understanding frog pos tags:
    * CGN tags: https://universaldependencies.org/tagset-conversion/nl-cgn-uposf.html 
    * Corresponding universal pos tags https://universaldependencies.org/u/pos/all.html 
    * for dep tags https://www.let.rug.nl/~vannoord/Lassy/sa-man_lassy.pdf

Understanding spacy tags:
    * dep tags https://universaldependencies.org/docs/nl/dep/
    * pos tags https://universaldependencies.org/docs/en/pos/
"""


class Patterns:
    def __init__(self):

        self.patterns = {}
        adj_tiers = [
            [
                [
                    "A_anp",
                    "A_ap",
                    "A_anh",
                    "A_ah",
                    "A_an",
                    "A_a",
                ],  # adj + noun applied to , verb is root
                ["A_nh", "A_h", "A_n", "A"],  #  noun it root
            ],
        ]
        # note: every tuple in a tier taken, but only first in a group sublist wrt., that tier

        # ------
        # Adjectives
        # ------

        #
        # adj + noun it's applied to, where verb is root
        #

        # The Dutch are not tight with money
        s_anp = {0: [1], 1: [2, 3, 4], 4: [5], 5: [6]}
        p_anp = {
            1: {"lemma": "be|feel"},
            #
            2: {"pos": "NOUN|PROPN", "label": "noun"},
            3: {"pos": "PART", "dep": "neg", "label": "neg"},
            4: {"pos": "ADJ", "label": "tight"},
            #
            5: {"pos": "ADP", "label": "with"},
            #
            6: {"pos": "NOUN|PROPN", "label": "money"},
        }
        t_anp = [("noun", "tight_with_money", "adj", "A_anp")]
        self.patterns["A_anp"] = (s_anp, p_anp, t_anp)

        # The Dutch are tight with money
        # NOTE: must be superseded by
        s_ap = {0: [1], 1: [2, 3], 3: [4], 4: [5]}
        p_ap = {
            1: {"lemma": "be|feel"},
            #
            2: {"pos": "NOUN|PROPN", "label": "noun"},
            3: {"pos": "ADJ", "label": "tight"},
            #
            4: {"pos": "ADP", "label": "with"},
            #
            5: {"pos": "NOUN|PROPN", "label": "money"},
        }
        t_ap = [("noun", "tight_with_money", "adj", "A_ap")]
        self.patterns["A_ap"] = (s_ap, p_ap, t_ap)

        # The Dutch are not sandy-haired
        s_anh = {0: [1], 1: [2, 3, 4], 4: [5, 6]}
        p_anh = {
            1: {"lemma": "be|feel"},
            #
            2: {"pos": "NOUN|PROPN", "label": "noun"},
            3: {"pos": "PART", "dep": "neg", "label": "neg"},
            4: {"pos": "ADJ", "label": "haired"},
            #
            5: {"lemma": "-"},
            6: {"pos": "ADJ", "dep": "amod", "label": "sandy"},
        }
        t_anh = [("noun", "sandy-haired", "adj", "A_anh")]
        self.patterns["A_anh"] = (s_anh, p_anh, t_anh)

        # The Dutch are sandy-haired
        # NOTE: superseded by A_anh
        s_ah = {0: [1], 1: [2, 3], 3: [4, 5]}
        p_ah = {
            1: {"lemma": "be|feel"},
            #
            2: {"pos": "NOUN|PROPN", "label": "noun"},
            3: {"pos": "ADJ", "label": "haired"},
            #
            4: {"lemma": "-"},
            5: {"pos": "ADJ", "dep": "amod", "label": "sandy"},
        }
        t_ah = [("noun", "sandy-haired", "adj", "A_ah")]
        self.patterns["A_ah"] = (s_ah, p_ah, t_ah)

        # The Dutch are not tall
        # NOTE: supersesed by A_anh
        s_an = {0: [1], 1: [2, 3, 4]}
        p_an = {
            1: {"lemma": "be|feel"},
            #
            2: {"pos": "NOUN|PROPN", "label": "noun"},
            3: {"pos": "ADJ", "label": "word"},
            4: {"pos": "PART", "dep": "neg", "label": "neg"},
        }
        t_an = [("noun", "word", "adj", "A_an")]
        self.patterns["A_an"] = (s_an, p_an, t_an)

        # The man is tall
        # Bob was afraid
        # Bob has been afraid
        # NOTE: superseded by A_n, A_ah, A_anh, A_anp, A_ap
        s_a = {0: [1], 1: [2, 3]}
        p_a = {
            1: {"lemma": "be|feel"},
            #
            2: {"pos": "ADJ", "label": "word"},
            3: {"pos": "NOUN|PROPN", "label": "noun"},
        }
        t_a = [("noun", "word", "adj", "A_a")]
        self.patterns["A_a"] = (s_a, p_a, t_a)

        #
        # noun is root
        #

        # The not sandy-haired man
        s_nh = {0: [1], 1: [2, 3], 3: [4, 5]}
        p_nh = {
            1: {"pos": "NOUN|PROPN", "label": "noun"},
            #
            2: {"pos": "PART", "dep": "neg", "label": "neg"},
            3: {"pos": "ADJ", "dep": "amod", "label": "haired"},
            #
            4: {"lemma": "-"},
            5: {"pos": "ADJ", "dep": "amod", "label": "sandy"},
        }
        t_nh = [("noun", "sandy-haired", "adj", "A_nh")]
        self.patterns["A_nh"] = (s_nh, p_nh, t_nh)

        # The sandy-haired man
        # The turkish are shorter than the LONG-LIMBED DUTCH
        # NOTE: superseded by A_nh
        s_h = {0: [1], 1: [2], 2: [3, 4]}
        p_h = {
            1: {"pos": "NOUN|PROPN", "label": "noun"},
            #
            2: {"pos": "ADJ", "dep": "amod", "label": "haired"},
            #
            3: {"lemma": "-"},
            4: {"pos": "ADJ", "dep": "amod", "label": "sandy"},
        }
        t_h = [("noun", "sandy-haired", "adj", "A_h")]
        self.patterns["A_h"] = (s_h, p_h, t_h)

        # The not very tall man
        # NOTE: superseded by A_nh
        s_n = {0: [1], 1: [2, 3]}
        p_n = {
            1: {"pos": "NOUN|PROPN", "label": "noun"},
            2: {"pos": "ADJ", "dep": "amod", "label": "word"},
            3: {"pos": "PART", "dep": "neg", "label": "neg"},
        }
        t_n = [("noun", "word", "adj", "A_n")]
        self.patterns["A_n"] = (s_n, p_n, t_n)

        # The tall man
        # NOTE: superseded by A_n2, A_nh, A_h
        s = {0: [1], 1: [2]}
        p = {
            1: {"pos": "NOUN|PROPN", "label": "noun"},
            2: {"pos": "ADJ", "dep": "amod", "label": "word"},
        }
        t = [("noun", "word", "adj", "A")]
        self.patterns["A"] = (s, p, t)

        ##
        ## adj + noun inspiring it, where verb is root
        ##

        # NOTE: not used, e.g., due to "Tom is short of Money" ... common false positives

        ## e.g., "Tom was not afraid of David"
        ## eg.,  "Tom did not feel afraid of David"
        # s_in = {0: [1], 1: [2, 3, 4], 4: [5], 5: [6]}
        # p_in = {
        #    1: {"lemma": "be|feel"},  # coppula
        #    #
        #    2: {"pos": "NOUN|PROPN"},
        #    3: {"pos": "PART", "dep": "neg", "label": "neg"},
        #    4: {"pos": "ADJ", "label": "word"},
        #    #
        #    5: {"lemma": "of"},
        #    #
        #    6: {"pos": "NOUN|PROPN", "label": "noun"},
        # }
        # t_in = [("noun", "inspires_word", "adj", "A_in")]
        # self.patterns["A_in"] = (s_in, p_in, t_in)

        ## e.g., "Tom was afraid of David",
        ## e.g., "Tom felt afraid of David"
        ## NOTE: superseded by A_in
        # s_i = {0: [1], 1: [2, 3], 3: [4], 4: [5]}
        # p_i = {
        #    1: {"lemma": "be|feel"},
        #    #
        #    2: {"pos": "NOUN|PROPN"},
        #    3: {"pos": "ADJ", "label": "word"},
        #    #
        #    4: {"lemma": "of"},
        #    #
        #    5: {"pos": "NOUN|PROPN", "label": "noun"},
        # }
        # t_i = [
        #    ("noun", "inspires_word", "adj", "A_i"),
        # ]
        # self.patterns["A_i"] = (s_i, p_i, t_i)

        # ------
        # Verbs
        # ------

        verb_tiers = [
            [
                ["V_pas_pnv1", "V_pas_pv1"],  # passive, patient + veb1
                [
                    "V_pas_pnv2b",
                    "V_pas_pv2b",
                    "V_pas_pnv2_1",
                    "V_pas_pnv2_2",
                    "V_pas_pv2_1",
                ],  # passive, patient + verb after conj
                [
                    "V_pas_anv1c",
                    'V_pas_av1c',
                    "V_pas_anv1",
                    "V_pas_av1",
                ],  # passive, agent + verb 1
                [
                    "V_pas_anv2_1",
                    "V_pas_anv2_2",
                    "V_pas_av2",
                ],  # passive, agent + verb after conj
                [
                    "V_act_pnv1c",
                    "V_act_pv1c",
                    "V_act_pnv1",
                    "V_act_pv1",
                    "V_act_pnv1p",
                    "V_act_pv1p",
                ],  # active, patient + verb1
                [
                    "V_act_pnv2_2",
                    "V_act_pnv2",
                    "V_act_pv2",
                ],  #  active, patient + verb after conj
                ["V_act_anv1", "V_act_av1"],  # active, agent + verb1
                [
                    "V_act_anv2_2",
                    "V_act_anv2",
                    "V_act_av2",
                ],  # active, agent + verb after conj
            ]
        ]

        #
        # passive, patient and verb before conjunction
        #

        # Alice has not been applauded
        # Alice was not applauded
        s_pas_pnv1 = {0: [1], 1: [2, 3]}
        p_pas_pnv1 = {
            1: {"pos": "VERB", "label": "word"},
            #
            2: {"pos": "NOUN|PROPN", "dep": "nsubjpass", "label": "noun_p"},
            3: {"pos": "PART", "dep": "neg", "label": "neg"},
        }
        t_pas_pnv1 = [
            ("noun_p", "word", "patient", "V_pas_pnv1"),
        ]
        self.patterns["V_pas_pnv1"] = (s_pas_pnv1, p_pas_pnv1, t_pas_pnv1)

        # Alice has been applauded
        # Alice was applauded
        # NOTE: must be superseded by pas_pnv1
        s_pas_pv1 = {0: [1], 1: [2]}
        p_pas_pv1 = {
            1: {"pos": "VERB", "label": "word"},
            #
            2: {"pos": "NOUN|PROPN", "dep": "nsubjpass", "label": "noun_p"},
        }
        t_pas_pv1 = [
            ("noun_p", "word", "patient", "V_pas_pv1"),
        ]
        self.patterns["V_pas_pv1"] = (s_pas_pv1, p_pas_pv1, t_pas_pv1)

        #
        # passive, patient and verb after conjuction
        #

        # Alice has not been applauded and WAS NOT cheered
        # Alice was jeered by WAS NOT booed
        s_pas_pnv2b = {0: [1], 1: [2, 3, 4, 5], 5: [6, 7]}
        p_pas_pnv2b = {
            1: {"pos": "VERB"},
            #
            2: {"pos": "NOUN|PROPN", "dep": "nsubjpass", "label": "noun_p"},
            3: {"pos": "AUX"},
            4: {"pos": "CCONJ"},
            5: {"pos": "VERB", "label": "word"},
            #
            6: {"pos": "AUX"},
            7: {"pos": "PART", "dep": "neg", "label": "neg"},
        }
        t_pas_pnv2b = [
            ("noun_p", "word", "patient", "V_pas_pnv2b"),
        ]
        self.patterns["V_pas_pnv2b"] = (s_pas_pnv2b, p_pas_pnv2b, t_pas_pnv2b)

        # Alice has not been applauded AND WAS cheered
        # Aluce has been applauded AND WAS cheered
        # NOTE: must be superseded by pas_pnv2b
        s_pas_pv2b = {0: [1], 1: [2, 3, 4, 5], 5: [6]}
        p_pas_pv2b = {
            1: {"pos": "VERB"},
            #
            2: {"pos": "NOUN|PROPN", "dep": "nsubjpass", "label": "noun_p"},
            3: {"pos": "AUX"},
            4: {"pos": "CCONJ"},
            5: {"pos": "VERB", "label": "word"},
            #
            6: {"pos": "AUX"},
        }
        t_pas_pv2b = [
            ("noun_p", "word", "patient", "V_pas_pv2b"),
        ]
        self.patterns["V_pas_pv2b"] = (s_pas_pv2b, p_pas_pv2b, t_pas_pv2b)

        # Alice has not been applauded or cheered
        # Alice was not applauded or cheered
        # NOTE: must be superseded by pas_pv2b
        s_pas_pnv2_1 = {0: [1], 1: [2, 3, 4, 5, 6]}
        p_pas_pnv2_1 = {
            1: {"pos": "VERB"},
            #
            2: {"pos": "NOUN|PROPN", "dep": "nsubjpass", "label": "noun_p"},
            3: {"pos": "AUX"},
            4: {"pos": "PART", "dep": "neg", "label": "neg"},
            5: {"pos": "CCONJ"},
            6: {"pos": "VERB", "label": "word"},
        }
        t_pas_pnv2_1 = [
            ("noun_p", "word", "patient", "V_pas_pnv2_1"),
        ]
        self.patterns["V_pas_pnv2_1"] = (s_pas_pnv2_1, p_pas_pnv2_1, t_pas_pnv2_1)

        # Alice was applauded but not cheered
        # Alice has been applauded but not cheered
        # Alice was jeered but was not booed
        # Alice has been applauded but has not been cheered
        s_pas_pnv2_2 = {0: [1], 1: [2, 3, 4, 5], 5: [6]}
        p_pas_pnv2_2 = {
            1: {"pos": "VERB"},
            #
            2: {"pos": "NOUN|PROPN", "dep": "nsubjpass", "label": "noun_p"},
            3: {"pos": "AUX"},
            4: {"pos": "CCONJ"},
            5: {"pos": "VERB", "label": "word"},
            #
            6: {"pos": "PART", "dep": "neg", "label": "neg"},
        }
        t_pas_pnv2_2 = [
            ("noun_p", "word", "patient", "V_pas_pv2_2"),
        ]
        self.patterns["V_pas_pnv2_2"] = (s_pas_pnv2_2, p_pas_pnv2_2, t_pas_pnv2_2)

        # Alice has been applauded and cheered
        # Alice was applauded and cheered
        # Alice was applauded and was cheered
        # Alice was applauded and had been cheered
        # Alice has not been applauded but was cheered
        # Alice had not been applauded and had been jeered
        # NOTE: must of superseded by both pnv2_1 and pnv2_2
        s_pas_pv2_1 = {0: [1], 1: [2, 3, 4, 5]}
        p_pas_pv2_1 = {
            1: {"pos": "VERB"},
            #
            2: {"pos": "NOUN|PROPN", "dep": "nsubjpass", "label": "noun_p"},
            3: {"pos": "AUX"},
            4: {"pos": "CCONJ"},
            5: {"pos": "VERB", "label": "word"},
        }
        t_pas_pv2_1 = [
            ("noun_p", "word", "patient", "V_pas_pv2_1"),
        ]
        self.patterns["V_pas_pv2_1"] = (s_pas_pv2_1, p_pas_pv2_1, t_pas_pv2_1)

        #
        # passive, agent + verb1
        #

        # Alice has not been applauded by Bob
        # Alice was not applauded by Bob
        # NOTE: must supersede pas_av1
        s_pas_anv1 = {0: [1], 1: [2, 3, 4, 5], 5: [6]}
        p_pas_anv1 = {
            1: {"pos": "VERB", "label": "word"},
            #
            2: {"pos": "NOUN|PROPN", "dep": "nsubjpass"},
            3: {"pos": "AUX"},
            4: {"pos": "PART", "dep": "neg", "label": "neg"},
            5: {"lemma": "by"},
            #
            6: {"pos": "NOUN|PROPN", "dep": "pobj", "label": "noun_a"},
        }
        t_pas_anv1 = [
            ("noun_a", "word", "agent", "V_pas_anv1"),
        ]
        self.patterns["V_pas_anv1"] = (s_pas_anv1, p_pas_anv1, t_pas_anv1)

        # Alice has been applauded by Bob
        # Alice was applauded by Bob
        s_pas_av1 = {0: [1], 1: [2, 3, 4], 4: [5]}
        p_pas_av1 = {
            1: {"pos": "VERB", "label": "word"},
            #
            2: {"pos": "NOUN|PROPN", "dep": "nsubjpass"},
            3: {"pos": "AUX"},
            4: {"lemma": "by"},
            #
            5: {"pos": "NOUN|PROPN", "dep": "pobj", "label": "noun_a"},
        }
        t_pas_av1 = [
            ("noun_a", "word", "agent", "V_pas_av1"),
        ]
        self.patterns["V_pas_av1"] = (s_pas_av1, p_pas_av1, t_pas_av1)

        # Alice has been applauded and has not been cheered by Bob
        # Alice has been applauded and cheered by Bob
        # Alice was applauded and cheered by Bob
        s_pas_anv1c = {0: [1], 1: [2, 3, 4, 5, 6], 6: [7], 7: [8]}
        p_pas_anv1c = {
            1: {"pos": "VERB", "label": "word"},
            #
            2: {"pos": "NOUN|PROPN", "dep": "nsubjpass"},
            3: {"pos": "AUX"},
            4: {"pos": "CCONJ"},
            5: {"pos": "PART", "dep": "neg", "label": "neg"},
            6: {"pos": "VERB"},
            #
            7: {"lemma": "by"},
            #
            8: {"pos": "NOUN|PROPN", "dep": "pobj", "label": "noun_a"},
        }
        t_pas_anv1c = [
            ("noun_a", "word", "agent", "V_pas_anv1c"),
        ]
        self.patterns["V_pas_anv1c"] = (s_pas_anv1c, p_pas_anv1c, t_pas_anv1c)

        # Alice has been applauded and has not been cheered by Bob
        # Alice has been applauded and cheered by Bob
        # Alice was applauded and cheered by Bob
        # NOTE: must be superseded by anv1c
        s_pas_av1c = {0: [1], 1: [2, 3, 4, 5], 5: [6], 6: [7]}
        p_pas_av1c = {
            1: {"pos": "VERB", "label": "word"},
            #
            2: {"pos": "NOUN|PROPN", "dep": "nsubjpass"},
            3: {"pos": "AUX"},
            4: {"pos": "CCONJ"},
            5: {"pos": "VERB"},
            #
            6: {"lemma": "by"},
            #
            7: {"pos": "NOUN|PROPN", "dep": "pobj", "label": "noun_a"},
        }
        t_pas_av1c = [
            ("noun_a", "word", "agent", "V_pas_av1c"),
        ]
        self.patterns["V_pas_av1c"] = (s_pas_av1c, p_pas_av1c, t_pas_av1c)

        #
        # passive, agent + verb2
        #

        # Alice has been applauded and cheered by Bob
        # Alice was applauded and cheered by Bob
        # NOTE: must be superceded by pas_anv2_1 and pas_anv2_2
        s_pas_av2 = {0: [1], 1: [2, 3, 4, 5], 5: [6], 6: [7]}
        p_pas_av2 = {
            1: {"pos": "VERB"},
            #
            2: {"pos": "NOUN|PROPN", "dep": "nsubjpass"},
            3: {"pos": "AUX"},
            4: {"pos": "CCONJ"},
            5: {"pos": "VERB", "label": "word"},
            #
            6: {"lemma": "by"},
            #
            7: {"pos": "NOUN|PROPN", "dep": "pobj", "label": "noun_a"},
        }
        t_pas_av2 = [
            ("noun_a", "word", "agent", "V_pas_av2"),
        ]
        self.patterns["V_pas_av2"] = (s_pas_av2, p_pas_av2, t_pas_av2)

        # Alice has not been applauded and cheered by Bob
        # Alice was not applauded or cheered by Bob
        s_pas_anv2_1 = {0: [1], 1: [2, 3, 4, 5, 6], 6: [7], 7: [8]}
        p_pas_anv2_1 = {
            1: {"pos": "VERB"},
            #
            2: {"pos": "NOUN|PROPN", "dep": "nsubjpass"},
            3: {"pos": "AUX"},
            4: {"pos": "CCONJ"},
            5: {"pos": "PART", "dep": "neg", "label": "neg"},
            6: {"pos": "VERB", "label": "word"},
            #
            7: {"lemma": "by"},
            #
            8: {"pos": "NOUN|PROPN", "dep": "pobj", "label": "noun_a"},
        }
        t_pas_anv2_1 = [
            ("noun_a", "word", "agent", "V_pas_anv2_1"),
        ]
        self.patterns["V_pas_anv2_1"] = (s_pas_anv2_1, p_pas_anv2_1, t_pas_anv2_1)

        # Alice has been applauded and has not been cheered by Bob
        # Alice has been applauded and cheered by Bob
        # Alice was applauded and cheered by Bob
        s_pas_anv2_2 = {0: [1], 1: [2, 3, 4, 5], 5: [6, 7], 7: [8]}
        p_pas_anv2_2 = {
            1: {"pos": "VERB"},
            #
            2: {"pos": "NOUN|PROPN", "dep": "nsubjpass"},
            3: {"pos": "AUX"},
            4: {"pos": "CCONJ"},
            5: {"pos": "VERB", "label": "word"},
            #
            6: {"pos": "PART", "dep": "neg", "label": "neg"},
            7: {"lemma": "by"},
            #
            8: {"pos": "NOUN|PROPN", "dep": "pobj", "label": "noun_a"},
        }
        t_pas_anv2_2 = [
            ("noun_a", "word", "agent", "V_pas_anv2_2"),
        ]
        self.patterns["V_pas_anv2_2"] = (s_pas_anv2_2, p_pas_anv2_2, t_pas_anv2_2)

        #
        # active, patient + verb 1
        #

        # Bob has not clapped Alice
        # Bob has not been clapping Alice
        # Bob was not clapping Alice
        # NOTE: must by superseded by act_pnv1_1
        s_act_pnv1 = {0: [1], 1: [2, 3, 4, 5]}
        p_act_pnv1 = {
            1: {"pos": "VERB", "label": "word"},
            #
            2: {"pos": "NOUN|PROPN", "dep": "nsubj"},
            3: {"pos": "NOUN|PROPN", "dep": "dobj", "label": "noun_p"},
            4: {"pos": "PART", "dep": "neg", "label": "neg"},
            5: {"pos": "AUX"},
        }
        t_act_pnv1 = [
            ("noun_p", "word", "patient", "V_act_pnv1"),
        ]
        self.patterns["V_act_pnv1"] = (s_act_pnv1, p_act_pnv1, t_act_pnv1)

        # Bob clapped Alice
        # Bob has clapped Alice
        # Bob has been clapping Alice
        # NOTE: must be superseded by act_pnv1
        s_act_pv1 = {0: [1], 1: [2, 3]}
        p_act_pv1 = {
            1: {"pos": "VERB", "label": "word"},
            #
            2: {"pos": "NOUN|PROPN", "dep": "nsubj"},
            3: {"pos": "NOUN|PROPN", "dep": "dobj", "label": "noun_p"},
        }
        t_act_pv1 = [
            ("noun_p", "word", "patient", "V_act_pv1"),
        ]
        self.patterns["V_act_pv1"] = (s_act_pv1, p_act_pv1, t_act_pv1)

        # Bob did not shout to Alice
        s_act_pnv1p = {0: [1], 1: [2, 3, 4], 4: [5]}
        p_act_pnv1p = {
            1: {"pos": "VERB", "label": "word"},
            #
            2: {"pos": "NOUN|PROPN", "dep": "nsubj"},
            3: {"pos": "PART", "dep": "neg", "label": "neg"},
            4: {"pos": "ADP"},
            #
            5: {"pos": "NOUN|PROPN", "dep": "pobj", "label": "noun_p"},
        }
        t_act_pnv1p = [
            ("noun_p", "word", "patient", "V_act_pnv1p"),
        ]
        self.patterns["V_act_pnv1p"] = (s_act_pnv1p, p_act_pnv1p, t_act_pnv1p)

        # Bob shouted to Alice
        # NOTE: must be superseded by act_pnv1p
        s_act_pv1p = {0: [1], 1: [2, 3], 3: [4]}
        p_act_pv1p = {
            1: {"pos": "VERB", "label": "word"},
            #
            2: {"pos": "NOUN|PROPN", "dep": "nsubj"},
            3: {"pos": "ADP"},
            #
            4: {"pos": "NOUN|PROPN", "dep": "pobj", "label": "noun_p"},
        }
        t_act_pv1p = [
            ("noun_p", "word", "patient", "V_act_pv1p"),
        ]
        self.patterns["V_act_pv1p"] = (s_act_pv1p, p_act_pv1p, t_act_pv1p)

        # Bob did not cheer or applaud Alice
        s_act_pnv1c = {0: [1], 1: [2, 3, 4, 5, 6], 6: [7]}
        p_act_pnv1c = {
            1: {"pos": "VERB", "label": "word"},
            #
            2: {"pos": "NOUN|PROPN", "dep": "nsubj"},
            3: {"pos": "AUX"},
            4: {"pos": "PART", "dep": "neg", "label": "neg"},
            5: {"pos": "CCONJ"},
            6: {"pos": "VERB"},
            #
            7: {"pos": "NOUN|PROPN", "dep": "dobj", "label": "noun_p"},
        }
        t_act_pnv1c = [
            ("noun_p", "word", "patient", "V_act_pnv1c"),
        ]
        self.patterns["V_act_pnv1c"] = (s_act_pnv1c, p_act_pnv1c, t_act_pnv1c)

        # Bob cheered and applauded Alice
        # Bob cheered and has previously applauded Alice
        # NOTE: must by superseded by act_pnv1c
        s_act_pv1c = {0: [1], 1: [2, 3, 4], 4: [5]}
        p_act_pv1c = {
            1: {"pos": "VERB", "label": "word"},
            #
            2: {"pos": "NOUN|PROPN", "dep": "nsubj"},
            3: {"pos": "CCONJ"},
            4: {"pos": "VERB"},
            #
            5: {"pos": "NOUN|PROPN", "dep": "dobj", "label": "noun_p"},
        }
        t_act_pv1c = [
            ("noun_p", "word", "patient", "V_act_pv1c"),
        ]
        self.patterns["V_act_pv1c"] = (s_act_pv1c, p_act_pv1c, t_act_pv1c)

        #
        # active, patient + verb after conj
        #

        # Bob did not cheer or applaud Alice
        s_act_pnv2 = {0: [1], 1: [2, 3, 4, 5, 6], 6: [7]}
        p_act_pnv2 = {
            1: {"pos": "VERB"},
            #
            2: {"pos": "NOUN|PROPN", "dep": "nsubj"},
            3: {"pos": "AUX"},
            4: {"pos": "PART", "dep": "neg", "label": "neg"},
            5: {"pos": "CCONJ"},
            6: {"pos": "VERB", "label": "word"},
            #
            7: {"pos": "NOUN|PROPN", "dep": "dobj", "label": "noun_p"},
        }
        t_act_pnv2 = [
            ("noun_p", "word", "patient", "V_act_pnv2"),
        ]
        self.patterns["V_act_pnv2"] = (s_act_pnv2, p_act_pnv2, t_act_pnv2)

        # Bob cheered but did not applaud Alice
        # Bob cheered by has not previously applauded Alice
        s_act_pnv2_2 = {0: [1], 1: [2, 3, 4], 4: [5, 6]}
        p_act_pnv2_2 = {
            1: {"pos": "VERB"},
            #
            2: {"pos": "NOUN|PROPN", "dep": "nsubj"},
            3: {"pos": "CCONJ"},
            4: {"pos": "VERB", "label": "word"},
            #
            5: {"pos": "NOUN|PROPN", "dep": "dobj", "label": "noun_p"},
            6: {"pos": "PART", "dep": "neg", "label": "neg"},
        }
        t_act_pnv2_2 = [
            ("noun_p", "word", "patient", "V_act_pnv2_2"),
        ]
        self.patterns["V_act_pnv2_2"] = (s_act_pnv2_2, p_act_pnv2_2, t_act_pnv2_2)

        # Bob cheered and applauded Alice
        # Bob cheered and has previously applauded Alice
        # NOTE: must by superseded by act_pnv2 and act_pnv2
        s_act_pv2 = {0: [1], 1: [2, 3, 4], 4: [5]}
        p_act_pv2 = {
            1: {"pos": "VERB"},
            #
            2: {"pos": "NOUN|PROPN", "dep": "nsubj"},
            3: {"pos": "CCONJ"},
            4: {"pos": "VERB", "label": "word"},
            #
            5: {"pos": "NOUN|PROPN", "dep": "dobj", "label": "noun_p"},
        }
        t_act_pv2 = [
            ("noun_p", "word", "patient", "V_act_pv2"),
        ]
        self.patterns["V_act_pv2"] = (s_act_pv2, p_act_pv2, t_act_pv2)

        #
        # active, agent + verb 1
        #

        # Bob jumped
        # Bob was jumping
        # Bob has previously jumped
        s_act_anv1 = {0: [1], 1: [2, 3]}
        p_act_anv1 = {
            1: {"pos": "VERB", "label": "word"},
            #
            2: {"pos": "NOUN|PROPN", "dep": "nsubj", "label": "noun_a"},
            3: {"pos": "PART", "dep": "neg", "label": "neg"},
        }
        t_act_anv1 = [
            ("noun_a", "word", "agent", "V_act_avn1"),
        ]
        self.patterns["V_act_anv1"] = (s_act_anv1, p_act_anv1, t_act_anv1)

        # Bob jumped
        # Bob was jumping
        # Bob has previously jumped
        # NOTE: must be superseded by act_anv1
        s_act_av1 = {0: [1], 1: [2]}
        p_act_av1 = {
            1: {"pos": "VERB", "label": "word"},
            #
            2: {"pos": "NOUN|PROPN", "dep": "nsubj", "label": "noun_a"},
        }
        t_act_av1 = [
            ("noun_a", "word", "agent", "V_act_av1"),
        ]
        self.patterns["V_act_av1"] = (s_act_av1, p_act_av1, t_act_av1)

        #
        # active, agent + verb after conj
        #

        # Bob was not jumping or skipping
        s_act_anv2 = {0: [1], 1: [2, 3, 4, 5, 6]}
        p_act_anv2 = {
            1: {"pos": "VERB"},
            #
            2: {"pos": "NOUN|PROPN", "dep": "nsubj", "label": "noun_a"},
            3: {"pos": "AUX"},
            4: {"pos": "PART", "dep": "neg", "label": "neg"},
            5: {"pos": "CCONJ"},
            6: {"pos": "VERB", "label": "word"},
        }
        t_act_anv2 = [
            ("noun_a", "word", "agent", "V_act_anv2"),
        ]
        self.patterns["V_act_anv2"] = (s_act_anv2, p_act_anv2, t_act_anv2)

        # Bob jumped but didn't skip
        # Bob had jumped but not skipped
        # Bob jumped by hasn't been skipping
        s_act_anv2_2 = {0: [1], 1: [2, 3, 4], 4: [5]}
        p_act_anv2_2 = {
            1: {"pos": "VERB"},
            #
            2: {"pos": "NOUN|PROPN", "dep": "nsubj", "label": "noun_a"},
            3: {"pos": "CCONJ"},
            4: {"pos": "VERB", "label": "word"},
            #
            5: {"pos": "PART", "dep": "neg", "label": "neg"},
        }
        t_act_anv2_2 = [
            ("noun_a", "word", "agent", "V_act_anv2_2"),
        ]
        self.patterns["V_act_anv2_2"] = (s_act_anv2_2, p_act_anv2_2, t_act_anv2_2)

        # Bob jumped and skipped
        # Bob was jumping and skipping
        # NOTE: must be superseded by act_anv2 and act_anv_2_2
        s_act_av2 = {0: [1], 1: [2, 3, 4]}
        p_act_av2 = {
            1: {"pos": "VERB"},
            #
            2: {"pos": "NOUN|PROPN", "dep": "nsubj", "label": "noun_a"},
            3: {"pos": "CCONJ"},
            4: {"pos": "VERB", "label": "word"},
        }
        t_act_av2 = [
            ("noun_a", "word", "agent", "V_act_av2"),
        ]
        self.patterns["V_act_av2"] = (s_act_av2, p_act_av2, t_act_av2)

        # create iters
        self.adj_tiers = [
            [
                [self.patterns[pattern_name] for pattern_name in pattern_group]
                for pattern_group in tier
            ]
            for tier in adj_tiers
        ]
        self.verb_tiers = [
            [
                [self.patterns[pattern_name] for pattern_name in pattern_group]
                for pattern_group in tier
            ]
            for tier in verb_tiers
        ]
