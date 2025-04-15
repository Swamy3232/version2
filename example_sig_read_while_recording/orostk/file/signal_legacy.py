class Signal(object):
    """
    This class represents a NVGate signal
    It's composed of Tracks
    """

    def __init__(self, nb_records=0, tracks=None, length=0):
        """

        :param nb_records: Number of records
        :param tracks: a list of track
        :param length: Length of the signal in seconds
        :return:
        """
        self.nb_records = nb_records
        self.length = length
        self.tracks = [] if tracks is None else list(tracks)
        self.file_idx = None

    @property
    def nb_tracks(self):
        return len(self.tracks)

    @property
    def frequencies(self):
        """

        :return: a set of all different track frequencies
        """
        frequencies = set()
        for track in self.tracks:
            frequencies.add(track.frequency)
        return frequencies

    @property
    def nb_frequencies(self):
        """

        :return: Number of different frequencies
        """
        return len(self.frequencies)

    @property
    def tracks_type(self):
        """

        :return: a set of all different track types
        """
        tracks_type = set()
        for track in self.tracks:
            tracks_type.add(track.track_type)
        return tracks_type


class Track(object):
    """
    This class represents a NVGate track
    """

    def __init__(self, name, frequency, magnitude, unit,
                 track_type, range_peak, coupling, nb_samples,
                 system_channel_string, data, coefs=(1, 0),
                 data_block_generator=None, generator_env=None):
        """

        :param name:
        :param frequency:
        :param magnitude:
        :param unit:
        :param track_type:
        :param range_peak:
        :param coupling:
        :param system_channel_string:
        :param coefs: A, B coefs for unit to SI unit
        :type coefs: (float, float)
        :param data: A list representing the data, can be empty if generator.
        :param data_generator: A data_generator to
        :param generator_env: The environment we wish to pass to
        our generator if needed, else pass an empty dict {}.
        """
        self.name = name
        self.frequency = frequency
        self.magnitude = magnitude
        self.unit = unit
        track_type_id = 1
        if track_type == 'ANALOG':
            track_type_id = 1
        elif track_type == 'SLOW':
            track_type_id = 2
        self.track_type = (track_type_id, track_type)
        self.range_peak = range_peak
        self.coupling = coupling
        self.nb_samples = nb_samples
        self.system_channel_string = system_channel_string
        self.coefs = coefs
        self.data = list(data)
        if data_block_generator is None:
            self.data_block_generator = self.base_data_generator
            self.generator_env = {}
        else:
            self.data_block_generator = data_block_generator.__get__(self,
                                                                     Track)
            self.generator_env = generator_env

    def base_data_generator(self, block_size=1024):
        """This generator is the default data generator, it reads
        data of the track and yield it by block.
        The generator will be used by the data_blocks method to write
        data_blocks in a signal file.

        :param block_size:
        :return: Yield blocks of data as lists of block_size
        """
        if (self.nb_samples % block_size) == 0:
            nb_blocks = self.nb_samples // block_size
        else:
            nb_blocks = (self.nb_samples // block_size) + 1
        for i in range(nb_blocks):
            begin = i * block_size
            end = (i + 1) * block_size
            yield self.data[begin:end]

    def data_blocks(self, block_size):
        """ Return the current data block generator

        :param block_size:
        :return: A generator
        """
        return self.data_block_generator(block_size=block_size)
