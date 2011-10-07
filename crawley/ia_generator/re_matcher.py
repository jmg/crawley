import re

def _re_all_single_elem_match(html, elem):
    """
        Gets all elements of a single kind
    """

    return re.findall("<%s[\w|\s|=|\"]*>\s*([\w|\s|_|-]*):?\s*</%s>" % (elem,elem), html)

def _re_title_match(html):
    """
        Gets all titles from a raw html
    """

    return _re_all_single_elem_match(html, "h[1-7]")

def get_title_matches(html, html2):
    """
        Gets all the amount of equal titles between two different html pages
    """

    return len([x for x in _re_title_match(html) if x in _re_title_match(html2)]) / min(len(_re_title_match(html), len(_re_title_match(html2))


def _re_td_match(html):
    """
        Gets all tds
    """

    return _re_all_single_elem_match(html, "td")

def get_table_td_match(html, html2):
    """
        Gets the amount of equal tds between two different html pages
    """

    return len([x for x in _re_td_match(html) if x in _re_td_match(html)]) / min(len(_re_td_match(html), len(_re_td_match(html2))

def _re_th_match(html):
    """
        Gets all th elements
    """

    return _re_all_single_elem_match(html, "th")

def get_table_th_header_match(html, html2):
    """
        Gets tables first row (if first row has th)
    """

    return len([x for x in _re_th_match(html) if x in _re_th_match(html)]) / min(len(_re_th_match(html), len(_re_th_match(html2))
