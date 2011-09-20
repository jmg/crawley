import java.util.*;

public class Parser {

	private static final String CLOSING_PARENTHESIS = "')";
	private static final String PYQUERY_HEAD = "PyQuery(html).query('";
	private static final String RETURN = "return ";
	private static final String ACTION_SEPARATOR = " < ";
	private static final String QUERY_SEPARATOR = " => ";

	public String parse(String crawleyDSL) {
		String[] parsingString = crawleyDSL.split(QUERY_SEPARATOR);
		String[] actionSection = parsingString[0].toLowerCase().split(ACTION_SEPARATOR);
		String action = actionSection[0];
		String properties = actionSection[1];
		// String getSection = parsingString[1];

		return getFinalQuery(action, properties);
	}

	protected String getFinalQuery(String action, String properties) {
		LinkedHashMap<String, String[]> propertyMap = new LinkedHashMap<String, String[]>();

		for (String name : properties.split(" ")) propertyMap.put(name.split(":")[0], this.removeBraces(name.split(":")[1]).split(","));

		String result = RETURN + this.compoundPropertyStartingBraces(properties);

		for (String property : propertyMap.keySet()) {
			for (int j = 0; j < propertyMap.get(property).length; j++)
				result += ((j == 0) ? "" : ", ") + PYQUERY_HEAD
						+ Property.getProperty(property)
						+ this.trimSingleQuotes(propertyMap.get(property)[j])
						+ CLOSING_PARENTHESIS + Action.getAction(action);
		}

		return result + this.compoundPropertyEndingBraces(properties);
	}

	protected String removeBraces(String propertyValues) {
		return propertyValues.replace("[", "").replace("]", "");
	}

	protected String compoundPropertyEndingBraces(String properties) {
		return this.compoundPropertyBraces(properties, false);
	}

	protected String compoundPropertyStartingBraces(String properties) {
		return this.compoundPropertyBraces(properties, true);
	}

	protected String compoundPropertyBraces(String properties,
			Boolean startingPosition) {
		return (properties.contains("[") && properties.contains("]") ? 
				((startingPosition) ? "[" : "]")
				: "");
	}

	public String trimSingleQuotes(String htmlElement) {
		return htmlElement.replace("'", "");
	}
}
