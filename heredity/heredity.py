import csv
import itertools
import sys
import random

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def prob_of_passing_gene_of_parent(num_of_genes):
    prob = None
    if num_of_genes == 2:
        prob = 1 - PROBS['mutation']
    elif num_of_genes == 1:
        prob = 0.5
    elif num_of_genes == 0:
        prob = PROBS['mutation']
    return prob


def prob_of_not_passing_gene_of_parent(num_of_genes):
    prob = None
    if num_of_genes == 2:
        prob = PROBS['mutation']
    elif num_of_genes == 1:
        prob = 0.5
    elif num_of_genes == 0:
        prob = 1 - PROBS['mutation']
    return prob


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    zero_gene = set()
    no_trait = set()
    people_to_genes = dict()
    joint = 1
    for person in people:
        if (person not in one_gene) and (person not in two_genes):
            zero_gene.add(person)
        if person not in have_trait:
            no_trait.add(person)
    for person in people:
        if person in zero_gene:
            people_to_genes[person] = 0
        elif person in one_gene:
            people_to_genes[person] = 1
        elif person in two_genes:
            people_to_genes[person] = 2

    for person in people:
        if not people[person]["mother"]:  # if not parents
            joint *= PROBS["gene"][people_to_genes[person]]
            if person in no_trait:
                joint *= PROBS["trait"][people_to_genes[person]][False]
            elif person in have_trait:
                joint *= PROBS["trait"][people_to_genes[person]][True]

        else:  # if parents
            from_mother = prob_of_passing_gene_of_parent(people_to_genes[people[person]['mother']])
            not_from_mother = prob_of_not_passing_gene_of_parent(
                people_to_genes[people[person]['mother']])
            from_father = prob_of_passing_gene_of_parent(people_to_genes[people[person]['father']])
            not_from_father = prob_of_not_passing_gene_of_parent(
                people_to_genes[people[person]['father']])

            if person in zero_gene:
                joint *= not_from_father * not_from_mother
            elif person in one_gene:
                joint *= ((from_father * not_from_mother) + (not_from_father * from_mother))
            elif person in two_genes:
                joint *= from_father * from_mother

            if person in no_trait:
                joint *= PROBS["trait"][people_to_genes[person]][False]
            elif person in have_trait:
                joint *= PROBS["trait"][people_to_genes[person]][True]

    return joint


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """

    for person in probabilities:
        if person in one_gene:
            probabilities[person]['gene'][1] += p
        elif person in two_genes:
            probabilities[person]['gene'][2] += p
        else:
            probabilities[person]['gene'][0] += p

        if person in have_trait:
            probabilities[person]['trait'][True] += p
        else:
            probabilities[person]['trait'][False] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """

    for person in probabilities:
        k_trait = 1 / (probabilities[person]['trait'][True] + probabilities[person]['trait'][False])
        probabilities[person]['trait'][True] *= k_trait
        probabilities[person]['trait'][False] *= k_trait

        k_gene = 1 / (probabilities[person]['gene'][0] + probabilities[person]
                      ['gene'][1] + probabilities[person]['gene'][2])
        probabilities[person]['gene'][0] *= k_gene
        probabilities[person]['gene'][1] *= k_gene
        probabilities[person]['gene'][2] *= k_gene


if __name__ == "__main__":
    main()
