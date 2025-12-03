import json

WEEKDAYS = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"]

class DayHours:
    def __init__(self, enabled=False, open_time="00:00", close_time="00:00"):
        self.enabled = enabled
        self.open_time = open_time
        self.close_time = close_time

    def to_dict(self, day_name):
        return {
            f"switch_{day_name}": 1 if self.enabled else 0,
            f"{day_name}_i": self.open_time if self.enabled else "00:00",
            f"{day_name}_u": self.close_time if self.enabled else "00:00",
        }


class Shift:
    """
    Represents a FULL WEEK of opening hours for a single shift.
    """

    def __init__(self, days=None):
        # days must be list of 7 tuples: (enabled, open, close)
        self.days = []

        if days and len(days) == 7:
            for enabled, start, end in days:
                self.days.append(DayHours(enabled, start, end))
        else:
            # default closed week
            for _ in range(7):
                self.days.append(DayHours(False))

    def to_dict(self):
        result = {}
        for idx, wd in enumerate(WEEKDAYS):
            result.update(self.days[idx].to_dict(wd))
        return result


class Hours:

    def __init__(self, shifts=None):
        self.shifts = []

        if shifts and len(shifts) == 3:
            for shift in shifts:
                if isinstance(shift, Shift):
                    self.shifts.append(shift)
                else:
                    raise ValueError("Each element must be a Shift instance")
        else:
            for _ in range(3):
                self.shifts.append(Shift())
 
    def __str__(self):
        return json.dumps(self.to_list())

    def set_shift(self, index, shift):
        if index < 0 or index > 2:
            raise IndexError("Shift index must be 0,1,2")
        if not isinstance(shift, Shift):
            raise ValueError("shift must be a Shift instance")
        self.shifts[index] = shift

    def get_shift(self, index):
        return self.shifts[index]

    def to_list(self):
        return [shift.to_dict() for shift in self.shifts]