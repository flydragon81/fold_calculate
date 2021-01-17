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

    @staticmethod
    def __min_float():
        return sys.float_info.min

    @staticmethod
    def __max_float():
        return sys.float_info.max

    def calculate_corners(self, sps_data: SpsData):
        min_x = sys.float_info.max
        max_x = sys.float_info.min
        min_y = sys.float_info.max
        max_y = sys.float_info.min

        src_point = sps_data.get_sps()
        rcv_point = sps_data.get_rps()

        point: Point
        for point in src_point:
            x = point.easting
            y = point.northing
            if x < min_x:
                self.__corners[0] = point
                min_x = x
            if x > max_x:
                self.__corners[2] = point
                max_x = x
            if y < min_y:
                self.__corners[1] = point
                min_y = y
            if y > max_y:
                self.__corners[3] = point
                max_y = y

        for point in rcv_point:
            x = point.easting
            y = point.northing
            if x < min_x:
                self.__corners[0] = point
                min_x = x
            if x > max_x:
                self.__corners[2] = point
                max_x = x
            if y < min_y:
                self.__corners[1] = point
                min_y = y
            if y > max_y:
                self.__corners[3] = point
                max_y = y

    def point_rotate_x_y(self, point: Point, counterclockwise=False):
        x = point.easting
        y = point.northing
        x0 = float(self.__x0)
        y0 = float(self.__y0)
        rot = float(self.__rot)
        if counterclockwise is True:
            rot = rot * -1
        radians = math.radians(rot)

        dx = x - x0
        dy = y - y0
        cos_rad = math.cos(radians)
        sin_rad = math.sin(radians)

        rot_x = x0 + dx * cos_rad - dy * sin_rad
        rot_y = y0 + dx * sin_rad + dy * cos_rad
        new_point = point
        new_point.easting = rot_x
        new_point.northing = rot_y
        return new_point

    def point_rotate(self, sps_data: SpsData):

        rcv_line_number_max_n = sps_data.get_line_for_max_n_rps()
        min_point_number = sps_data.get_line_stats_for_rcv_line(rcv_line_number_max_n).fp
        max_point_number = sps_data.get_line_stats_for_rcv_line(rcv_line_number_max_n).lp
        rcv_line_n = sps_data.get_n_points_for_rcv_line(rcv_line_number_max_n)

        minRP = sps_data.get_point_for_rcv_line_point(rcv_line_number_max_n, min_point_number)
        maxRP = sps_data.get_point_for_rcv_line_point(rcv_line_number_max_n, max_point_number)

        lenR = math.sqrt(math.pow((minRP.easting - maxRP.easting), 2) +
                         math.pow((minRP.northing - maxRP.northing), 2))
        dRly = maxRP.northing - minRP.northing
        self.rot_rcv = math.acos(dRly / lenR) * 180 / math.pi
        self.d_rcv = lenR / (rcv_line_n - 1)

        src_line_max_n = sps_data.get_line_for_max_n_sps()
        min_point_number = sps_data.get_line_stats_for_src_line(src_line_max_n).fp
        max_point_number = sps_data.get_line_stats_for_src_line(src_line_max_n).lp
        src_line_n = sps_data.get_n_points_for_src_line(src_line_max_n)

        minSP = sps_data.get_point_for_src_line_point(src_line_max_n, min_point_number)
        maxSP = sps_data.get_point_for_src_line_point(src_line_max_n, max_point_number)

        lenS = math.sqrt(math.pow((minSP.easting - maxSP.easting), 2) +
                         math.pow((minSP.northing - maxSP.northing), 2))
        dSly = maxSP.northing - minSP.northing
        self.rot_src = math.acos(dSly / lenS) * 180 / math.pi
        self.d_src = lenS / (src_line_n - 1)

        if self.rot_rcv < self.rot_src:
            if self.lockrot == False:
                self.rot = self.rot_rcv
            if self.lockdxb == False:
                self.dxb = self.d_src / 2
            if self.lockdyb == False:
                self.dyb = self.rot_rcv / 2
        else:
            if self.lockrot == False:
                self.rot = self.rot_src
            if self.lockdxb == False:
                self.dxb = self.d_rcv / 2
            if self.lockdyb == False:
                self.dyb = self.rot_src / 2

    def calculate_grid_origin(self, sps_data: SpsData):
        min_x = self.__corners[0].easting
        min_y = self.__corners[1].northing
        self.__x0 = min_x - self.__dxb
        self.__y0 = min_y - self.__dyb

    def calculate_grid_nb(self, sps_dat: SpsData):
        n = 10
        max_x = self.__corners[2].easting
        max_y = self.__corners[3].northing

        pass

