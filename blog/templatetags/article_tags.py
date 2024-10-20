from django import template

register = template.Library()


@register.filter
def truncate_chars(value, max_chars=100):
    """
    Обрезает строку до указанного количества символов и добавляет многоточие,
    если строка длиннее этого значения.

    :param value: Строка, которую нужно обрезать.
    :param max_chars: Максимальное количество символов, до которого следует
                      обрезать строку (по умолчанию 100).
    :return: Обрезанная строка с многоточием, если она была длиннее max_chars.
    """
    if len(value) > max_chars:
        return f"{value[:max_chars]}..."
    return value
