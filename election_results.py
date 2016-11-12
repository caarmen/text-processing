import re
import sys
from collections import namedtuple
from bs4 import BeautifulSoup
import xlwt
from xlwt import XFStyle
from xlwt import Utils

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

    num_style = get_num_style()
    right_total_style = get_right_total_style()
    border_bottom_style = get_border_bottom_style()
    border_right_style = get_border_right_style()

    sheet = book.add_sheet("2016 results")
    sheet.set_panes_frozen(True)
    sheet.set_horz_split_pos(1)
    sheet.set_vert_split_pos(3)
    sheet.write(0, 0, "State", border_bottom_style)
    sheet.write(0, 1, "Reporting", border_bottom_style)
    sheet.write(0, 2, "Electoral Votes", get_border_bottom_right_style())

    for col, candidate in enumerate(election_result.candidates):
        sheet.write(0, col + 3, candidate, border_bottom_style)
    sheet.write(0, col + 4, "Total", get_border_bottom_left_style())

    for row, state_id in enumerate(sorted(election_result.results_per_state)):
        sheet.write(row + 1, 0, state_id)
        state_result = election_result.results_per_state[state_id]
        sheet.write(row + 1, 1, float(state_result.reporting))
        sheet.write(row + 1, 2, int(state_result.electoral_votes), border_right_style)
        for col, candidate in enumerate(election_result.candidates):
            popular_vote = state_result.popular_votes_per_candidate.get(candidate)
            if popular_vote:
                popular_vote = int(popular_vote.replace(",", ""))
            sheet.write(row + 1, col + 3, popular_vote, num_style)
        total_cell_start = xlwt.Utils.rowcol_to_cell(row + 1, 3)
        total_cell_end = xlwt.Utils.rowcol_to_cell(row + 1, col + 3)
        sheet.write(row + 1, col + 4, xlwt.Formula("sum(%s:%s)" % (total_cell_start, total_cell_end)),
                    right_total_style)

    row += 2
    total_cols = col + 4
    bottom_total_style = get_bottom_total_style()
    sheet.write(row, 0, "Total (votes):", bottom_total_style)
    sheet.write(row, 1, "", bottom_total_style)
    for col in range(2, total_cols + 1):
        total_cell_start = xlwt.Utils.rowcol_to_cell(1, col)
        total_cell_end = xlwt.Utils.rowcol_to_cell(row - 1, col)
        sheet.write(row, col, xlwt.Formula("sum(%s:%s)" % (total_cell_start, total_cell_end)), bottom_total_style)

    cell_total_all_votes = xlwt.Utils.rowcol_to_cell(row, total_cols)
    row += 1
    sheet.write(row, 0, "Total (%):")
    pct_style = get_pct_style()
    for col in range(3, total_cols + 1):
        total_cell_start = xlwt.Utils.rowcol_to_cell(row - 1, col)
        sheet.write(row, col, xlwt.Formula("%s/%s" %(total_cell_start, cell_total_all_votes)), pct_style)

    book.save(output_file)
    print("Wrote results to %s" % output_file)


def get_num_style():
    """
    :rtype: XFStyle
    """
    style = XFStyle()
    style.num_format_str = "#,##0"
    return style

def get_pct_style():
    """
    :rtype: XFStyle
    """
    style = XFStyle()
    style.num_format_str = "0.00%"
    return style

def get_bottom_total_style():
    """
    :rtype: XFStyle
    """
    borders = xlwt.Borders()
    borders.top = xlwt.Borders.DOUBLE
    style = XFStyle()
    style.borders = borders
    style.num_format_str = get_num_style().num_format_str
    return style


def get_right_total_style():
    """
    :rtype: XFStyle
    """
    borders = xlwt.Borders()
    borders.left = xlwt.Borders.DOUBLE
    style = XFStyle()
    style.borders = borders
    style.num_format_str = get_num_style().num_format_str
    return style


def get_border_right_style():
    """
    :rtype: XFStyle
    """
    borders = xlwt.Borders()
    borders.right = xlwt.Borders.HAIR
    style = XFStyle()
    style.borders = borders
    return style


def get_border_bottom_style():
    """
    :rtype: XFStyle
    """
    borders = xlwt.Borders()
    borders.bottom = xlwt.Borders.HAIR
    style = XFStyle()
    style.borders = borders
    return style


def get_border_bottom_right_style():
    """
    :rtype: XFStyle
    """
    borders = xlwt.Borders()
    borders.bottom = xlwt.Borders.HAIR
    borders.right = xlwt.Borders.HAIR
    style = XFStyle()
    style.borders = borders
    return style


def get_border_bottom_left_style():
    """
    :rtype: XFStyle
    """
    borders = xlwt.Borders()
    borders.bottom = xlwt.Borders.HAIR
    borders.left = xlwt.Borders.DOUBLE
    style = XFStyle()
    style.borders = borders
    return style


if __name__ == "__main__":
    main(sys.argv)
