import datetime
import re
import time

from ... import Command


class GetSignalProperties(Command):
    def __init__(self, project_name, measurement_name):
        super().__init__(name=None, parameters=[project_name, measurement_name])
        self.value = None
        return

    def parse_response(self, response):
        temp = self.parse_response_list_string(response)

        self.value = {'creation_time': temp[0]}
        element = datetime.datetime.strptime(temp[0], "%m/%d/%Y - %H:%M:%S").timetuple()
        self.value['creation_timestamp'] = int(time.mktime(element))
        self.value['type'] = temp[1]
        self.value['sampling_freq_1'] = temp[2]
        self.value['sampling_freq_2'] = temp[3]
        self.value['sampling_freq_slow'] = temp[4]

        try:
            self.value['sampling_freq_slow_value'] = float(re.findall("\d+\.\d+", temp[4])[0])
        except (Exception,):
            self.value['sampling_freq_slow_value'] = 12.5

        self.value['signal_on_analyzer'] = temp[5]
        self.value['signal_on_computer'] = temp[6]
        self.value['signal_size'] = temp[7]
        self.value['signal_duration'] = temp[8]
        self.value['number_tracks'] = temp[9]
        self.value['format'] = temp[10]
        self.value['signal_duration_seconds'] = temp[11]
