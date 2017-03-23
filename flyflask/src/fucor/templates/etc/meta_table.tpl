{% set buf = [] -%}
{% for x, y in attr -%}
	{% do buf.append("%-18s AS \"%0s\"" % (x,y) ) -%}
{%- endfor %}

/*
TRUNCATE TABLE {{ tobe_table }};
SELECT * FROM {{ tobe_table }} WHERE ROWNUM < 10000;
*/

INSERT INTO {{ tobe_table }} ( 
	{{ '  ' }}{{ tobe|join("\n\t, ") }} 
	, REGIST_DT
	, REGISTER_ID
	, CHANGE_DT 
	, CHANGER_ID )
SELECT
	{{ '  ' }}{{ buf|join("\n\t, ")}}
	, SYSDATE            AS "REGIST_DT"
	, 'SYSTEM'           AS "REGISTER_ID"
	, SYSDATE            AS "CHANGE_DT"
	, 'SYSTEM'           AS "CHANGER_ID"
FROM
	{{ asis_table }}
{{ condition }}
;

