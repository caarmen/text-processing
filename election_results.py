import re
import sys
from collections import namedtuple
from bs4 import BeautifulSoup
import xlwt

StateResult = namedtuple("StateResult", ["reporting", "electoral_votes", "popular_votes_per_candidate"])
ElectionResult = namedtuple("ElectionResult", ["candidates", "results_per_state"])


def main(args):
    input_file = args[1]
    output_file = args[2]
    election_result = read_input(input_file)
    write_output(election_result, output_file)


def read_input(input_file):
    """
    :param input_file: the location of the election results HTML file
    :return: an ElectionResult
    :rtype ElectionResult
    """
    soup = BeautifulSoup(open(input_file), "html.parser")
    articles = soup.find_all("article", id=re.compile("state[A-Z][A-Z]"))
    results_per_state = {}
    candidates = set([])
    for article in articles:
        popular_votes_per_candidate = {}
        state_id = article["id"].replace("state", "")
        reporting_line = article.select('p[class="reporting"]')[0].text
        m = re.search("([0-9\.]*)[^0-9]*([0-9]*)", reporting_line)
        reporting = m.group(1)
        electoral_votes = m.group(2)

        results_table = article.select('table[class="results-table"]')[0]
        results_candidates = results_table.select("tr")
        for results_candidate in results_candidates:
            candidate_name = results_candidate \
                                 .select('th[class="results-name"]')[0] \
                                 .select('span[class="name-combo"]')[0] \
                                 .text \
                                 .replace("Winner ", "")[2:]
            candidates.add(candidate_name)
            popular_vote = results_candidate.select('td[class="results-popular"]')[0].text
            popular_votes_per_candidate[candidate_name] = popular_vote

        results_per_state[state_id] = StateResult(reporting, electoral_votes, popular_votes_per_candidate)
    return ElectionResult(sorted(candidates), results_per_state)


def write_output(election_result, output_file):
    """
    :type election_result: ElectionResult
    :param election_result: the result of #read_input
    :param output_file: the path to an excel file where the results will be written.
    """
    book = xlwt.Workbook()
    sheet = book.add_sheet("2016 results")
    sheet.set_panes_frozen(True)
    sheet.set_horz_split_pos(1)
    sheet.set_vert_split_pos(3)
    sheet.write(0, 0, "State")
    sheet.write(0, 1, "Reporting")
    sheet.write(0, 2, "Electoral Votes")

    for col, candidate in enumerate(election_result.candidates):
        sheet.write(0, col + 3, candidate)

    for row, state_id in enumerate(sorted(election_result.results_per_state)):
        sheet.write(row + 1, 0, state_id)
        state_result = election_result.results_per_state[state_id]
        sheet.write(row + 1, 1, state_result.reporting)
        sheet.write(row + 1, 2, state_result.electoral_votes)
        for col, candidate in enumerate(election_result.candidates):
            popular_vote = state_result.popular_votes_per_candidate.get(candidate) or ""
            sheet.write(row + 1, col + 3, popular_vote)

    book.save(output_file)
    print("Wrote results to %s" % output_file)


if __name__ == "__main__":
    main(sys.argv)
