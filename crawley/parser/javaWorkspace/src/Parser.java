import java.util.HashMap;
import java.util.Map;


public class Parser {

	private Map<String, String> htmlElements = new HashMap<String, String>();
	
	public Parser() {
		this.populateMaps();
	}
	
	protected void populateMaps() {
		htmlElements.put("'p'", "p");
		htmlElements.put("'div'", "div");
		htmlElements.put("'table'", "table");
		htmlElements.put("'ul'", "ul");
		htmlElements.put("'ol'", "ol");
	}

	public String parse(String crawleyDSL) {
		String[] parsingString = crawleyDSL.split(" => ");
		String[] actionSection = parsingString[0].toLowerCase().split(" < ");
		String action = actionSection[0];
		String properties = actionSection[1];
		//String getSection = parsingString[1];
		
		return "return PyQuery(html).query('" + this.htmlElements.get(properties.split(":")[1]) + "')" + ((action.contains("all")) ? "" : ((action.contains("first")) ? "[0]" : "[-1]"));  
	}

}
