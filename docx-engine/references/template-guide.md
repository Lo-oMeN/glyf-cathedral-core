# Template Guide

DOCX templates use Jinja2 syntax for dynamic content substitution.

## Basic Variables

Insert variables using double curly braces:

```
Dear {{ customer_name }},

Your order #{{ order_id }} has been shipped on {{ ship_date }}.
```

## Nested Objects

Access nested data using dot notation:

```
Company: {{ company.name }}
Address: {{ company.address.city }}, {{ company.address.country }}
Contact: {{ company.contact.email }}
```

## Conditionals

Use Jinja2 conditionals for optional content:

```
{% if premium_customer %}
Thank you for being a premium member!
{% endif %}

{% if status == 'urgent' %}
PRIORITY: This requires immediate attention.
{% else %}
Standard processing time applies.
{% endif %}
```

## Loops

Iterate over lists for repeating content:

### Simple List

```
{% for item in items %}
- {{ item }}
{% endfor %}
```

### Table Rows

For dynamic tables, create a table with headers, then use a loop row:

```
| Product | Qty | Price |
|---------|-----|-------|
{% for item in order_items %}
| {{ item.name }} | {{ item.quantity }} | ${{ item.price }} |
{% endfor %}
```

## Filters

Apply filters to format values:

```
Date: {{ date | default('N/A') }}
Amount: ${{ amount | default(0) }}
Name: {{ name | upper }}
```

## Escaping

To show literal braces, use:

```
Use {{ '{{' }} and {{ '}}' }} for template syntax.
```

## Best Practices

1. **Always provide defaults** - Use `| default('')` for optional fields
2. **Test with sample data** - Verify all template paths work
3. **Keep templates simple** - Complex logic belongs in preprocessing
4. **Use consistent naming** - snake_case for variable names

## Data Structure Example

```json
{
  "customer_name": "John Doe",
  "order_id": "ORD-2024-001",
  "company": {
    "name": "Acme Corp",
    "address": {
      "city": "New York",
      "country": "USA"
    }
  },
  "order_items": [
    {"name": "Widget", "quantity": 2, "price": 29.99},
    {"name": "Gadget", "quantity": 1, "price": 49.99}
  ],
  "premium_customer": true
}
```
