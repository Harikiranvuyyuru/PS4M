class Counter(dict):
    PRIMARY_DELIMITOR = ' '

    def drop_entry(self, key, value):
        return False

    def parse_key(self, raw_key):
        return raw_key

    def deserialize(self, file_path):
        file = open(file_path)
        for line in file:
            line = line.strip()
            (count, raw_key) = line.split(Counter.PRIMARY_DELIMITOR)

            key = self.parse_key(raw_key)
            value = int(count)

            if not self.drop_entry(key, value):
                self[key] = value
        file.close()


class TextCounter(Counter):
    SECONDARY_DELIMITOR = '\001'

    def drop_entry(self, key, value):
        if len(key) == 1:
            return value < 16
        elif len(key) == 2:
            return value < 8
        elif len(key) == 3:
            return value < 4
        else:
            raise RuntimeError("Unexpected length of key: %d" % len(key))

    def parse_key(self, raw_key):
        return tuple(raw_key.split(TextCounter.SECONDARY_DELIMITOR))
