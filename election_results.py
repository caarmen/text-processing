import re
import sys
from bs4 import BeautifulSoup
import xlwt


def main(args):
    input_file = args[1]
    output_file = args[2]
    results_per_state = read_input(input_file)
    write_output(results_per_state, output_file)


def read_input(input_file):
    """
    :param input_file: the location of the election results HTML file
    :return: a dict of state id to a dict of candidate to popular vote
    """
    soup = BeautifulSoup(open(input_file), "html.parser")
    articles = soup.find_all("article", id=re.compile("state[A-Z][A-Z]"))
    results_per_state = {}
    for article in articles:
        results_this_state = {}
        state_id = article["id"].replace("state", "")
        results_table = article.select('table[class="results-table"]')[0]
        results_candidates = results_table.select("tr")
        for results_candidate in results_candidates:
            candidate_name = results_candidate \
                                 .select('th[class="results-name"]')[0] \
                                 .select('span[class="name-combo"]')[0] \
                                 .text \
                                 .replace("Winner ", "")[2:]
            popular_vote = results_candidate.select('td[class="results-popular"]')[0].text
            results_this_state[candidate_name] = popular_vote

        results_per_state[state_id] = results_this_state
    return results_per_state


def write_output(results_per_state, output_file):
    """
    :param results_per_state: the result of #read_input
    :param output_file: the path to an excel file where the results will be written.
    """
    book = xlwt.Workbook()
    sheet = book.add_sheet("2016 results")
    sheet.set_panes_frozen(True)
    sheet.set_horz_split_pos(1)
    sheet.set_vert_split_pos(1)
    row = 0
    col = 0
    sheet.write(row, col, "State")
    col += 1
    all_candidates = set([])
    for state_result in results_per_state.values():
        all_candidates |= state_result.keys()
    all_candidates = sorted(all_candidates)

    for candidate in all_candidates:
        sheet.write(row, col, candidate)
        col += 1

    for state_id in sorted(results_per_state):
        row += 1
        col = 0
        sheet.write(row, col, state_id)
        col += 1
        state_result = results_per_state[state_id]
        for candidate in all_candidates:
            popular_vote = state_result.get(candidate) or ""
            sheet.write(row, col, popular_vote)
            col += 1
    book.save(output_file)
    print("Wrote results to %s" % (output_file))


if __name__ == "__main__":
    main(sys.argv)
