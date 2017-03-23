<?xml version="1.0" encoding="UTF-8"?>
<metadata>
    <table name="{{ table_name }}">
	{%- for column in columns %}
        <column name="{{ column.col_name }}" type="{{ column.col_type }}" {% if column.col_opt|string() != 'nan' %} {{ column.col_opt }} {% endif %} />{% if column.description|string() != 'nan' %}<!-- {{ column.description }} -->{% endif %}
	{%- endfor %}
    </table>
</metadata>