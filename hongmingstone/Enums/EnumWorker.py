from enum import Enum


class EnumWorker(Enum):
    """
    :status_on: 在職
    :status_off: 離職
    """

    status_on = 1
    status_off = 0

    CHOICES = (
        [1, '在職'],
        [0, '離職']
    )
