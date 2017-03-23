package {{ class.base_package }}.service.impl;


import java.util.HashMap;
import java.util.List;
import java.util.Map;

import javax.annotation.Resource;

import org.springframework.stereotype.Service;

import {{ class.base_package }}.service.{{ class.code }}Service; 
import egovframework.rte.fdl.cmmn.EgovAbstractServiceImpl;


/**
 * <pre>
 *	{{ class.code }}ServiceImpl - {{ coder.desc }} 메뉴 서비스 인터페이스 구현 클래스
 * </pre>
 *
 * @author	{{ coder.name }}
 * @since	{{ coder.since }}
 * @version	{{ coder.version }}
 * @see		{@link {{ class.code }}Service}
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

@Service("{{ class.code }}Service")
public class {{ class.code }}ServiceImpl extends EgovAbstractServiceImpl implements {{ class.code }}Service {

	/**
	 * {{ coder.desc }} DAO class inject.
	 */
	@Resource(name = "{{ class.code }}Dao")
	private {{ class.code }}Dao dao;

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
	public {{retType}} process{{ x.name }}(Map param) throws Exception {
	{% if retType|string() == 'int' %}
		return -1;
	{% else %}
		return null;
	{% endif -%}
	}
	
{% endfor %}
	 
}
