import re
import typing
from collections import deque
from copy import copy
from itertools import permutations, product
from pprint import pprint as pp

def get_tuples(parse_s: dict, parse_p: dict, pattern_tiers) -> list[tuple]:
    """Return a list of tuples.

    Notes:
        * we return for the highest ranked matching tier only
        * we return for every pattern in that tier
        * we return considering every token in the parse as a potential root wrt., each pattern
    """
    parse_idxs_ordered = get_ordered_idxs(parse_s)

    # consider each tier
    for tier_i, pattern_tier in enumerate(pattern_tiers):
        tuples = []
        for pattern_group in pattern_tier:

            # get all solutions for hightest ranked pattern in group only
            solutions = []
            for pattern in pattern_group:

                for parse_start in get_ordered_idxs(parse_s):
                    pattern_s, pattern_p, pattern_t = pattern
                    solutions += get_solutions_from_start(
                        parse_start, parse_s, parse_p, pattern_s, pattern_p
                    )

                for solution in solutions:
                    tuples += get_solution_tuples(solution, parse_p, pattern)

                if len(solutions) > 0:
                    break  # i.e., capture firstmost from pattern_group only

        # return on first matching tier
        if len(tuples) > 0:
            return tuples

    # return empty
    return []


def get_solution_tuples(solution: list[tuple], parse_p, pattern: tuple) -> list[tuple]:
    """Return a list of tuples, as expected by the passed pattern

    Args:
        solution (list[tuple]):
            I.e., the list of (parse_idx, pattern_idx) tuples corresponding to pattern.
            E.g., [(parse_idx, corresponding pattern_idx), ...]
    """

    # decompose pattern info
    pattern_s, pattern_p, pattern_t = pattern

    # for each (parse_idx, pattern_idx) pair, extract corresponding value and label instances
    label2value = {}
    for parse_idx, pattern_idx in solution:

        # pattern token is labelled? Then, it's corresponding parse token has wanted info
        if "label" in pattern_p[pattern_idx]:

            label = pattern_p[pattern_idx]["label"]
            value = parse_p[parse_idx]["lemma"]
            label2value[label] = value

    # build tuples given pattern_t and label2value knowledge
    returned = [
        [multiple_replace(label2value, s) for s in t[:2]] + list(t[2:])
        for t in pattern_t
    ]

    # handle negation retrospectively
    if "neg" in label2value.keys():
        for t in returned:
            t[1] = "NEG_" + t[1]

    # make tuples
    returned = [tuple(t) for t in returned]

    return returned


def multiple_replace(replacements, text):
    # Create a regular expression from the dictionary keys
    regex = re.compile("(%s)" % "|".join(map(re.escape, replacements.keys())))
    # For each match, look-up corresponding value in dictionary
    return regex.sub(lambda mo: replacements[mo.group()], text)


def get_ordered_idxs(parse_s: dict) -> list[int]:
    """Return a list of parse_s idxs in order of top to bottom of the tree.

        Note: ignores idx 0 (i.e., fakeroot)

    Args:
        parse_s (dict) : a tree of head::int->deps::list[int]
                         has a fakeroot idx=0, whose dependent is the real root
    """

    # accumulator
    ordered_idxs = []

    # state
    last = deque([0])

    while len(last) > 0:

        idx = last.pop()
        if idx != 0:
            ordered_idxs.append(idx)
        if idx in parse_s.keys():
            for child_idx in parse_s[idx]:
                last.appendleft(child_idx)  # append to left

    return ordered_idxs


def get_solutions_from_start(
    parse_start: int, parse_s: dict, parse_p: dict, pattern_s: dict, pattern_p: dict
) -> list[list[tuple]]:
    """Return a list of solutions, wrt., a parse tree taking parse_start as the
    root for pattern comparison.

    Args:
        parse_start (int): the parse_s idx which we assume to be

    Returns accumulator, a list of solutions:
    """
    accumulator = [
        # [],  # identified solution, as a list of (parse_idx, pattern_idx) matches
        # ... other solutions
    ]

    # check if starting point if a match, and if so, init stack.
    if is_match(parse_p[parse_start], pattern_p[pattern_s[0][0]]):
        stack = [
            (
                [],  # 'earlier': the matches from previous loops
                [
                    (parse_start, pattern_s[0][0])
                ],  # 'last': the matches added in the most recent loop
            ),  # potential set of solutions
            # ... other potential solutions
        ]
    else:
        stack = []

    # loop
    while len(stack) > 0:

        earlier, last = stack.pop()

        # 'last' is the immediately previous loop's identified (parse_token_idx, pattern_token_idx) matches
        #
        # unresolved_pattern_token_idxs:
        #   a list of pattern token idxs, wrt., pattern_p or pattern_s, in 'last' with unresolved children
        #
        # corresponding_perms:
        #   a list of itertools.permutations outputs
        #   where corresponding_perms[i] corresponds to unresolved_pattern_token_idxs[i]
        #   where corresponding_perms[i] is a group of parse_token_idx.children perms
        #       *meeting* the property requirements of
        #       unresolved_pattern_token_idxs.children in their given order.

        unresolved_pattern_token_idxs = []
        corresponding_perms = []

        # build unresolved_pattern_token_idxs and corresponding_perms
        # or otherise identify that unresolved nodes are unresolvable
        unresolved_are_unresolvable = False
        for parse_idx, pattern_idx in last:

            if len(pattern_s.get(pattern_idx, [])) == 0:
                # pattern idx has no children
                pass
            else:
                # pattern idx has children, which need resolving

                # children perms of parse_idx, which meets children requirements of pattern_idx
                perms = permutations(
                    parse_s.get(parse_idx, []), r=len(pattern_s[pattern_idx])
                )
                ok_perms = [
                    perm
                    for perm in perms
                    if is_counterpart_match(
                        perm, pattern_s[pattern_idx], parse_p, pattern_p
                    )
                ]

                if len(ok_perms) == 0:
                    # there exists no per of chidrem of parse_idx which can meet
                    # requirements of children of pattern_idx
                    unresolved_are_unresolvable = True
                    continue
                else:
                    # there exists ...
                    unresolved_pattern_token_idxs.append(pattern_idx)
                    corresponding_perms.append(ok_perms)
                    # E.g.,
                    # [
                    #     [
                    #         [17, 18],  a possible perm
                    #         [18, 17]
                    #     ],  # parse_token_index.children perms corresponding to e.g., children of pattern_idx = 2
                    #     [
                    #         [31, 33],  a possible perm
                    #         [33, 31]
                    #     ],  # parse_token_index.children perms corresponding to e.g., children of pattern_idx = 3
                    #     ...
                    # ]  # unresolved_pattern_token_idxs

        # solution failed
        if unresolved_are_unresolvable == True:
            pass
        # solution complete
        elif len(unresolved_pattern_token_idxs) == 0:
            accumulator.append(earlier + last)
        # solution ongoing ...
        else:

            # add previous 'last' to 'earlier', in readyness for creation of a new 'last'
            earlier += last

            # add new potential solutions to the stack
            for solution in product(*corresponding_perms):
                # E.g., one such solution, could be ([17,18], [31,33]),
                # i.e., solution[i] is a perm of parse_idx[i].children meeting the req. of pattern_idx[i].children
                # the solution tuple, satisfies all children of all unresolved_pattern_token_idxs

                last = []
                for pattern_idx, parse_idx_children_idxs in zip(
                    unresolved_pattern_token_idxs, solution
                ):
                    pattern_idx_children_idxs = pattern_s[pattern_idx]
                    last += list(
                        zip(parse_idx_children_idxs, pattern_idx_children_idxs)
                    )

                stack.append((earlier, last))

    return accumulator


def is_counterpart_match(
    parse_token_idxs: list[int],  # order matters
    pattern_token_idxs: list[int],  # order matters
    parse_p: dict,
    pattern_p: dict,
) -> bool:
    """Return True if the properties of the tokens at parse_token_idxs match their correspondings pattern_token_idxs."""
    for parse_token_idx, pattern_token_idx in zip(parse_token_idxs, pattern_token_idxs):
        parse_token_properties = parse_p[parse_token_idx]
        pattern_token_properties = pattern_p[pattern_token_idx]
        if is_match(parse_token_properties, pattern_token_properties) == False:
            return False
    return True


# def is_match(
#     parse_token_properties: dict,
#     criteria_token_properties: dict,
#     *,
#     excluded_labels: list[str] = ["label"]
# ) -> bool:
#     """Return True if each of parse_token_properties is a re.match for corresponding criteria_token_properties. Excempting properties in 'excluded_labels'"""
#     for criteria_key, criteria_value in criteria_token_properties.items():
#         if criteria_key in excluded_labels:
#             pass
#         elif criteria_key not in parse_token_properties.keys():
#             return False  # cannot meet criteria
#         else:
#             match = re.match(criteria_value, parse_token_properties[criteria_key])
#             if match:
#                 pass
#             else:  # does not meet criteria
#                 return False
#     return True

def is_match(
    parse_token_properties: dict,
    criteria_token_properties: dict,
    *,
    excluded_labels: list[str] = ["label"]
) -> bool:
    """Return True if ...
    """
    for criteria_key, criteria_value in criteria_token_properties.items():
        if criteria_key in excluded_labels:
            pass
        elif criteria_key not in parse_token_properties.keys():
            return False  # cannot meet criteria
        else:
            if parse_token_properties[criteria_key] in criteria_value.split("|"):
                pass
            else:  # does not meet criteria
                return False
    return True
