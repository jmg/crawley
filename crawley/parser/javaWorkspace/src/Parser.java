import java.util.HashMap;
import java.util.Map;


public class Parser {

	private static final String ACTION_END = " < ";
	private static final String QUERY_SEPARATOR = " => ";
	private Map<String, Action> actionElements = new HashMap<String, Action>();
	private Map<String, Property> propertyElements = new HashMap<String, Property>();
	
	public Parser() {
		this.populateMaps();
	}
	
	protected void populateMaps() {
		populateActions();	
		populateProperties();
	}

	protected void populateProperties() {
		propertyElements.put("id", new IDProperty());
		propertyElements.put("tag", new TagProperty());
		propertyElements.put("class", new ClassProperty());
	}

	protected void populateActions() {
		actionElements.put("first", new FirstAction());
		actionElements.put("last", new LastAction());
		actionElements.put("all", new AllAction());
	}

	public String parse(String crawleyDSL) {
		String[] parsingString = crawleyDSL.split(QUERY_SEPARATOR);
		String[] actionSection = parsingString[0].toLowerCase().split(ACTION_END);
		String action = actionSection[0];
		String properties = actionSection[1];
		//String getSection = parsingString[1];
		
		return getFinalQuery(action, properties);  
	}

	protected String getFinalQuery(String action, String properties) {
		return "return " 
				+ this.compoundProperty(properties, true)
				+ "PyQuery(html).query('"
				+ this.propertyElements.get(properties.split(":")[0]) 
				+ this.trimSingleQuotes(properties.split(":")[1]) 
				+ "')" + this.actionElements.get(action)
				+ this.compoundProperty(properties, false)
				;
	}

	protected String compoundProperty(String properties, Boolean startingPosition) {
		return (properties.contains("{") && properties.contains("}") ? ((startingPosition) ? "[" : "]") : ""); 
	}

	public String trimSingleQuotes(String htmlElement) {
		return htmlElement.replace("'", "");
	}
}
