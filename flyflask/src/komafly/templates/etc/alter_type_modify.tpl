{% set buf = [] -%}
{% for c in columns -%}
	{% do buf.append("%-18s VARCHAR2(%d)" % (c.column_name, c.data_length*2) ) -%}
{%- endfor %}

ALTER TABLE {{ table_name }} MODIFY ( 
{{ '  ' }}{{ buf|join("\n\t, ")}}   
);