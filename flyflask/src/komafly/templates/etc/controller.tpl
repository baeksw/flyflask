package {{ class.base_package }}.web;

import java.util.Map;

import javax.annotation.Resource;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Controller;
import org.springframework.ui.ModelMap;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.servlet.ModelAndView;

import {{ class.base_package }}.service.{{ class.code }}Service;
import core.ifw.cmm.request.CoreRequest;
import core.ifw.cmm.result.CoreResultData;


/**
 * <pre>
 *	{{ class.code }}Controller - {{ coder.desc }} 프로그램 컨트롤러 클래스
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
 
@Controller
public class {{ class.code }}Controller {

	/**
	 * Logger init.
	 */
	private static final Logger logger = LoggerFactory.getLogger({{ class.code }}Controller.class);

	/**
	 * {{ coder.descr }} 서비스 클래스
	 */
	@Resource(name="{{ class.code }}Service")
	private {{ class.code }}Service service;

{% for x in class.method %}
	/**
	 * <pre>
	 * {{ x.descr.pre }}
	 * </pre>
	 * @param param - {{ x.descr.param }}
	 * @return "{{ x.descr.return }}"
	 * @exception Exception - {{ x.descr.exception }}
	 */
	@RequestMapping(value = "/{{ class.base_package|replace('.','/') }}/{{ class.code }}_{{x.name}}.do")
	@SuppressWarnings("rawtypes")
	public ModelAndView process{{ x.name }}(CoreRequest coreRequest, ModelMap model) throws Exception {

		ModelAndView mav = new ModelAndView("coreReturnView");
		CoreResultData coreResultData = new CoreResultData(coreRequest.getCALL_TYPE());

		try {
			/**
			Map param = coreRequest.getMapVariableList();
			logger.info("param : " + param.toString());
			
			coreResultData.setReturnDataMap((Map<String, Object>) service.process{{ x.name }}(param));
			coreResultData.setResultMessageSuccessSelect();
			*/
		} catch(Exception e) {
			logger.error("process{{ x.name }} : " + e.getMessage());
			coreResultData.setResultMessageFailSelect(e);
		}

		mav.addObject("FORM_DATA", coreResultData);
		return mav;

	} 
	
	
{% endfor %}

}
