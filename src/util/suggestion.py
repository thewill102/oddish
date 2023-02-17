import heapq
from src.config.definitions import config
from src.util.logger import suggestion_log

standard = {
    'Unit price revenue': 'gap_percent',
    'Price difference': 'gap'
}


def suggest(table):
    suggestion_log.info('Buff Buy Steam Sell：\n')
    for info, column in standard.items():
        # buff sell to steam, steam - the bigger the buff the better, so the biggest in front
        sort_by_column(table, info, column, ascending=False)

    suggestion_log.info('Steam Buy Buff Sell\n')
    for info, column in standard.items():
        # steam to buff sale, steam - buff the smaller the better, preferably negative, so the smallest in front
        sort_by_column(table, info, column, ascending=True)


def sort_by_column(table, suggestion, column, ascending=True):
    filtered_table = filter_table(table)

    if ascending:
        top = heapq.nsmallest(config.TOP_N, filtered_table, key = lambda s: getattr(s, column))
    else:
        top = heapq.nlargest(config.TOP_N, filtered_table, key = lambda s: getattr(s, column))

    suggestion_log.info(suggestion + 'Descending order: ')
    for item in top:
        suggestion_log.info(item.detail())
    suggestion_log.info('\n')


def filter_table(table):
    return [x for x in table if getattr(x, 'history_sold') >= config.MIN_SOLD_THRESHOLD]
