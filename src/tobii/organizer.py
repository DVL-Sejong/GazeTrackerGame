class Organizer:
    def __init__(self, data):
        self.data = data
        self.ranges = []
        self.t_index = []
        self.t_order = []
        self.order_in_type()

    def order_in_type(self):
        end_index = 0
        while True:
            start_index = end_index
            end_index = start_index + 1
            status = self.data[start_index].status
            while self.data[end_index].status == status and end_index < len(self.data) - 1:
                end_index += 1

            self.ranges.append([start_index, end_index - 1])
            index, order = self.order_in_time_by_status(start_index, end_index - 1)
            self.t_index.append(index)
            self.t_order.append(order)

            if end_index == len(self.data) - 1: break

    def order_in_time_by_status(self, start, end):
        time_first = self.data[start].timestamp
        time_index = 0
        time_order = -1
        index = []
        order = []

        for i in range(start, end + 1):
            if self.data[i].timestamp - time_first >= 1000000:
                time_first = self.data[i].timestamp
                time_index += 1
                time_order = 0
                t_index = time_index
                t_order = time_order
            else:
                time_order += 1
                t_index = time_index
                t_order = time_order

            index.append(t_index)
            order.append(t_order)

        return index, order
