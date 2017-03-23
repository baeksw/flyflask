<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE sqlMap PUBLIC "-//ibatis.apache.org//DTD SQL Map 2.0//EN" "http://ibatis.apache.org/dtd/sql-map-2.dtd" >
<sqlMap namespace="{{ class.code }}">
<!--  
 *   프로그램명 : {{ coder.desc }}
 *   작 성 일 : {{ coder.since }}
 *   작 성 자 : {{ coder.name }}
 *   비   고 :
 *   Copyright (c) 2016 KTR Co.,Ltd All Rights reserved. 
 -->{% for x in class.method -%}
	{% if 'SEARCH' in x.name|string() %}
	{% set buf = [] -%}
	{% for column in x.table.columns -%}
		{% if column.alias -%}
			{% do buf.append("A.%s as %s\t/*%s*/" % ( column.name ,column.alias, column.comment)) -%}
		{% else %}
			{% do buf.append("A.%s\t/*%s*/" % ( column.name ,column.comment)) -%}
		{% endif %}
	{%- endfor %}	
	<!-- 
		작  성  자 : {{ coder.name }}
		작  성  일 : {{ coder.since }}
		내      용  : {{ x.descr.pre }}
	-->
	<select id="{{ class.code }}.{{ x.name }}" parameterClass="hashmap" resultClass="hashmap">
	<![CDATA[ 
        SELECT  
{{'\t\t\t'}}{{ buf|join('\n\t\t\t, ')}}
        FROM {{ x.table.name }} A
	]]>
	</select>
	{% elif 'SAVE' in x.name|string() %}
	<!-- 
		작  성  자 : {{ coder.name }}
		작  성  일 : {{ coder.since }}
		내      용  : {{ x.descr.pre }}
	-->
	<insert id="{{ class.code }}.{{ x.name }}" parameterClass="hashmap">
	<![CDATA[
	{% set buf = [] -%}
	{% set vbuf = [] -%}
	{% for column in x.table.columns -%}
		{% do buf.append("%s\t/*%s*/" % ( column.name, column.comment)) -%}
		{% do vbuf.append("#%s#\t/*%s*/" % ( column.name ,column.comment)) -%}
	{%- endfor %}	
         INSERT INTO {{ x.table.name }} (
{{'\t\t\t'}}{{ buf|join('\n\t\t\t, ')}}
       ) VALUES (
{{'\t\t\t'}}{{ vbuf|join('\n\t\t\t, ')}}
        )
	]]>
	</insert>
	{% elif 'UPDATE' in x.name|string() %}
	<!-- 
		작  성  자 : {{ coder.name }}
		작  성  일 : {{ coder.since }}
		내      용  : {{ x.descr.pre }}
	-->
	<update id="{{ class.code }}.{{ x.name }}" parameterClass="hashmap">
	<![CDATA[
	{% set buf = [] -%}
	{% for column in x.table.columns -%}
		{% do buf.append("%s = #%s#\t/*%s*/" % ( column.name,column.name, column.comment)) -%}
	{%- endfor %}	
        UPDATE {{ x.table.name }}
           SET
{{'\t\t\t'}}{{ buf|join('\n\t\t\t, ')}}
         WHERE 1=2 /* 조건절 수정 */ 
         ;
	]]>
	</update>
	{% elif 'DELETE' in x.name|string() %}
	<!-- 
		작  성  자 : {{ coder.name }}
		작  성  일 : {{ coder.since }}
		내      용  : {{ x.descr.pre }}
	-->
	<delete id="{{ class.code }}.{{ x.name }}" parameterClass="hashmap">
	<![CDATA[
		DECLARE
		BEGIN
			/* {{ x.table.name }} 삭제 처리*/
			DELETE FROM {{ x.table.name }}
			WHERE 1=2; /* 조건절 수정 */
			       
       	END;   
	]]>		
	</delete>			
	{% else %}
	{% endif -%}
		
{% endfor %}

</sqlMap>