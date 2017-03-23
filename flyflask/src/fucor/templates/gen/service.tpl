package {{ class.base_package }}.service;

import java.util.Map;

/**
 * <pre>
 *	{{ class.code }}Service - {{ coder.desc }} 메뉴 서비스 인터페이스
 * </pre>
 *
 * @author	{{ coder.name }}
 * @since	{{ coder.since }}
 * @version	{{ coder.version }}
 *
 * <pre>
 * == Modification Information ==
 * Date		Modifier		Comment
 * ====================================================
 * {{ coder.since }}	{{ coder.name }}		Initial Created.
 * ====================================================
 * </pre>
 *
 * Copyright KTR(C) All right reserved.
 */ 
public interface {{ class.code }}Service {

{% for x in class.method %}
	{% if ( 'UPDATE' in x.name|string()) or ('DELETE' in x.name|string())  -%}
		{% set retType = 'int' -%}
	{% else -%}
		{% set retType = 'Object' -%}
	{% endif -%}
	
	/**
	 * <pre>
	 * {{ x.descr.pre }}
	 * </pre>
	 * @param param - {{ x.descr.param }}
	 * @return "{{ x.descr.return }}"
	 * @exception Exception - {{ x.descr.exception }}
	 */
	@SuppressWarnings({ "unchecked","rawtypes"})
	public {{retType}} process{{ x.name }}(Map param) throws Exception ;
	
{% endfor %}
	 
}