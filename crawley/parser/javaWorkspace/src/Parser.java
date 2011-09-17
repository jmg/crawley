import java.util.HashMap;
import java.util.Map;


public class Parser {

	private Map<String, Action> actionElements = new HashMap<String, Action>();
	//private Map<String, String> propertyElements = new HashMap<String, String>();
	
	public Parser() {
		this.populateMaps();
	}
	
	protected void populateMaps() {
		actionElements.put("first", new FirstAction());
		actionElements.put("last", new LastAction());
		actionElements.put("all", new AllAction());
	}

	public String parse(String crawleyDSL) {
		String[] parsingString = crawleyDSL.split(" => ");
		String[] actionSection = parsingString[0].toLowerCase().split(" < ");
		String action = actionSection[0];
		String properties = actionSection[1];
		//String getSection = parsingString[1];

		if (crawleyDSL.contains("id")) return "return PyQuery(html).query('#unID')[0]";
		
		return "return PyQuery(html).query('" 
				+ this.trimSingleQuotes(properties.split(":")[1]) 
				+ "')" + this.actionElements.get(action);  
	}

	public String trimSingleQuotes(String htmlElement) {
		return htmlElement.replace("'", "");
	}
}
