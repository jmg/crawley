import re

def _re_title_match(html):
    """
        Gets all titles from a raw html
    """

    return re.findall("<h[1-7]>([\w|\s|_|-]+):?</h[1-7]>", html)

def get_title_matches(html, html2):
    """
        Gets all the amount of equal titles between two different html pages
    """

    return len([x for x in _re_title_match(html) if x in _re_title_match(html2)]) / min(len(_re_title_match(html), len(_re_title_match(html2))

def _re_td_match(html):
    """
        Gets all tds
    """

    return re.findall("<td[\w|\s|=|\"]*>\s*([\w|\s|_|-]*):?\s*</td>",a)

def get_table_td_match(html, html2):
    """
        Gets the amount of equal tds between two different html pages
    """

    return len([x for x in _re_td_match(html) if x in _re_td_match(html)]) / min(len(_re_td_match(html), len(_re_td_match(html2))

def _re_th_match(html):
    """
        Gets all th elements
    """

    return re.findall("<th[\w|\s|=|\"]*>\s*([\w|\s|_|-]*):?\s*</th>",a)

def get_table_th_header_match(html, html2):
    """
        Gets tables first row (if first row has th)
    """

    return len([x for x in _re_th_match(html) if x in _re_th_match(html)]) / min(len(_re_th_match(html), len(_re_th_match(html2))
