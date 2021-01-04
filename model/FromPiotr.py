def __calculate_stats(self, point_list: list, stats_list: list):
    point: Point
    for point in point_list:
        ln = point.line
        pn = point.point
        x = point.easting
        y = point.northing

        if x < self.__x_min:
            self.__x_min = x

        if x > self.__x_max:
            self.__x_max = x

        if y < self.__y_min:
            self.__y_min = y

        if y > self.__y_max:
            self.__y_max = y

        stats_list = self.__calculate_stats_helper(stats_list, ln, pn)


@staticmethod
def __calculate_stats_helper(stats_list: list, line: float, point: float):
    stat: Stats
    newstat: Stats
    n: int
    size = len(stats_list)

    i = 0
    while i < size:
        stat = stats_list[i]

        ln = stat.ln
        fp = stat.fp
        lp = stat.lp

        if fp > point:
            fp = point

        if lp < point:
            lp = point

        if ln == line:
            n = stat.n + 1
            newstat = Stats()
            newstat.n = n
            newstat.ln = ln
            newstat.fp = fp
            newstat.lp = lp

            stats_list[i] = newstat

            return stats_list

        i += 1

    newstat = Stats()
    newstat.ln = line
    newstat.fp = point
    newstat.lp = point
    newstat.n = 1
    stats_list.append(newstat)

    return stats_list

# STATS ends
