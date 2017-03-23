package {{ class.base_package }}.service.impl;

import java.util.Map;

import org.springframework.stereotype.Repository;

import core.ifw.cmm.dataaccess.CmmBaseDAO;

/**
 * <pre>
 *	{{ class.code }}Dao - {{ coder.desc }} 프로그램 데이터처리 DAO 클래스
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

@Repository("{{ class.code }}Dao")
public class {{ class.code }}Dao extends CmmBaseDAO {
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
	{% if 'SEARCH' in x.name|string() %}
		return list("{{ class.code }}.{{ x.name }}", param);
	{% elif 'SAVE' in x.name|string() %}
		return insert("{{ class.code }}.{{ x.name }}", param);
	{% elif 'UPDATE' in x.name|string() %}
		return update("{{ class.code }}.{{ x.name }}", param);
	{% elif 'DELETE' in x.name|string() %}
		return delete("{{ class.code }}.{{ x.name }}", param);					
	{% else %}
		return null;
	{% endif -%}
	}
		
{% endfor %}
	
}
