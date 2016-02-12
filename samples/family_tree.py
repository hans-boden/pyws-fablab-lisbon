# python3
"""
    build a 'tree' of family members

    None of the code snippets below could serve for a real genealogy application.
    They are just meant as simple examples, how to use recursion, classes and dictionaries

    One of the major problems when dealing with real persons is to have a good key for
    objects. A person could be reasonably identified by birth date, name, place of birth. But
    people change their names,  even places (towns) may change their name over time. And in
    our examples, the key would have the same content as the object it represents - ugly.

    Practical applications use an artificial index, kind of an anonymous "Personal Number",
    which is hard to deal with, when we would try to connect persons manually, like:
        (tree[342].has_father(tree[296])

    The best way is to use a graphical user interface with a "tree-view". We all actually
    use one of the best examples of a very powerful tree-view every day: That is the file
    explorer of our pc. It displays hierarchical dependencies by indentation (as does the
    Python source code ;-) ), show properties of objects in a table to the right -
    and it keeps the ugly object-key-problem hidden under the surface.
"""

def main():

    root = build_family_tree_simple()

    oldest = get_oldest(root)
    print("oldest: ", oldest.name, oldest.year)
    return

def build_family_tree_simple():
    me = Person('hans', 1956)

    me_f = Person('horst', 1934)
    me_m = Person('erna', 1935)

    me_f_f = Person('emil', 1910)
    me_f_m = Person('klara', 1912)

    me_m_f = Person('herbert', 1904)
    me_m_m = Person('elsa', 1908)

    me.has_father(me_f)
    me.has_mother(me_m)
    me_f.has_father(me_f_f)
    me_f.has_mother(me_f_m)
    me_m.has_father(me_m_f)
    me_m.has_mother(me_m_m)

    return me

def build_family_tree_changed():

    pers_list = {}
    pers_list['hans'] = Person('hans', 1956)

    pers_list['horst'] = Person('horst', 1934)
    pers_list['erna'] = Person('erna', 1935)

    pers_list['emil'] = Person('emil', 1910)
    pers_list['klara'] = Person('klara', 1912)

    pers_list['herbert'] = Person('herbert', 1904)
    pers_list['elsa'] = Person('elsa', 1908)

    pers_list['hans'].has_father(pers_list['horst'])
    pers_list['hans'].has_mother(pers_list['erna'])
    pers_list['horst'].has_father(pers_list['emil'])
    pers_list['horst'].has_mother(pers_list['klara'])
    pers_list['erna'].has_father(pers_list['herbert'])
    pers_list['erna'].has_mother(pers_list['elsa'])

    return pers_list['hans']

def get_oldest(person):
    ''' return the oldest known person in the family tree '''
    oldest = person
    if person.father:
        ancestor = get_oldest(person.father)
        if ancestor.year < oldest.year:
            oldest = ancestor

    if person.mother:
        ancestor = get_oldest(person.mother)
        if ancestor.year < oldest.year:
            oldest = ancestor

    return oldest

class Person():
    """ Person represents one individual as a member of a family tree """
    def __init__(self, name, year):
        self.name = name
        self.year = year
        self.father = None
        self.mother = None
    def has_father(self, pers):
        self.father = pers
    def has_mother(self, pers):
        self.mother = pers

class PersonMF():
    """ PersonsMF represents one individual as a member of a family tree
        This is an alternative implementation
    """
    def __init__(self, name, sex, year):
        self.name = name
        self.year = year
        self.sex = sex
        self.father = None
        self.mother = None

    def has_parent(self, pers):
        if pers.sex == 'm':
            self.father = pers
        else:
            self.mother = pers

class PersonAny():
    """ PersonAny represents one individual as a member of a family tree
        As society is increasingly agnostic about gender questions, we could choose this:
    """
    def __init__(self, name, year):
        self.name = name
        self.year = year
        self.parents = []

    def has_parent(self, pers):
        self.parents.append(pers)

    """ for this case, the tree search for the oldest also gets simpler """

def get_oldest_any(person):
    ''' return the oldest known person (PersonAny) in the family tree '''
    oldest = person
    for pers in person.parents:
        ancestor = get_oldest_any(pers)
        if ancestor.year < oldest.year:
            oldest = ancestor
    return oldest

main()
