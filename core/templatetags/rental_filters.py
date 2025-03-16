from django import template

register = template.Library()

@register.filter
def filter_active(rentals):
    """Filter rentals to show only active ones"""
    return [rental for rental in rentals if rental.status in ['active', 'confirmed']]

@register.filter
def filter_past(rentals):
    """Filter rentals to show only past ones"""
    return [rental for rental in rentals if rental.status in ['completed', 'cancelled']]

@register.filter
def sub(value, arg):
    """Subtracts the arg from the value"""
    try:
        return value - arg
    except (ValueError, TypeError):
        return value 