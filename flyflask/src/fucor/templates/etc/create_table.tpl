{% set buf = [] -%}
{% for column in columns -%}
	{% if column.primary_key -%}
		{% do buf.append("Column('%s',%s,primary_key=True,quote=False)" % ( column.name ,column.type)) -%}
	{% else %}
		{% if column.nullable -%}
			{% do buf.append("Column('%s',%s,nullable=%s,quote=False)" % ( column.name ,column.type, column.nullable)) -%}
		{% else -%}
			{% do buf.append("Column('%s',%s,quote=False)" % ( column.name ,column.type)) -%}
		{%- endif %}
	{%- endif %}
{%- endfor %}


{{ name| lower }} = Table('{{ name|upper }}',metadata,{{ buf|join('\n, ') }})
# ----------------------------------------------
# DROP IF EXISTS TABLE '{{ name|upper }}'
# ----------------------------------------------
check_table = Table('{{ name|upper }}',metadata,autoload=True,autoload_with=engine)
if check_table.exists():
	check_table.drop(checkfirst=False)


{{ name| lower }}.create(checkfirst=True)
print("done. {{ name| lower }}")