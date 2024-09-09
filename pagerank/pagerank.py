import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    output = dict()
    random_distr = float()
    if len(corpus[page]) == 0:
        random_distr = 1/(len(corpus))
        for el in corpus:
            output.update({el: random_distr})
        return output
    random_distr = (1-damping_factor)/len(corpus)

    for el in corpus:
        if el not in corpus[page]:
            output.update({el: random_distr})

    percent = (1 - (random_distr * len(output))) / len(corpus[page])

    for el in corpus[page]:
        output.update({el: percent})

    return output


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    start = random.sample(sorted(corpus), k=1)[0]
    all_samples = []
    temp_choices = []
    temp_distributions = []
    trans = None

    while n != 0:
        trans = transition_model(corpus, start, damping_factor)
        for el in trans:
            temp_choices.append(el)
            temp_distributions.append(trans[el])
        start = random.choices(temp_choices, weights=temp_distributions, k=1)[0]
        all_samples.append(start)
        temp_choices = []
        temp_distributions = []
        n -= 1

    output = dict()
    for el in corpus:
        output.update({el: (all_samples.count(el))/len(all_samples)})
    return output


def NumLinks(corpus, i):
    if len(corpus[i]) == 0:
        return len(corpus)
    return len(corpus[i])


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    output = dict()
    temp_output = dict()
    N = len(corpus)
    for el in corpus:
        output.update({el: 1/N})

    p_list = set()
    for el in corpus:
        p_list.add(el)
    i_list = set()

    while p_list:
        for p in p_list.copy():  # iterate over all pages p
            PR = (1-damping_factor)/N
            for el in corpus:  # find pages i of page p
                if len(corpus[el]) == 0:
                    i_list.add(el)
                elif p in corpus[el]:
                    i_list.add(el)

            for i in i_list:  # formula
                PR += damping_factor*output[i]/NumLinks(corpus, i)
            i_list.clear()
            temp_output.update({p: PR})

        for p in temp_output:
            if abs(output[p] - temp_output[p]) <= 0.001:
                p_list.remove(p)
            else:
                output[p] = temp_output[p]
        temp_output.clear()

    return output


if __name__ == "__main__":
    main()
