public class Utils {
	public static String removeBraces(String value) {
		return value.replace("[", "").replace("]", "");
	}

	public static String compoundPropertyEndingBraces(String properties) {
		return compoundPropertyBraces(properties, false);
	}

	public static String compoundPropertyStartingBraces(String properties) {
		return compoundPropertyBraces(properties, true);
	}

	protected static String compoundPropertyBraces(String properties,
			Boolean startingPosition) {
		return (properties.contains("[") && properties.contains("]") ? ((startingPosition) ? "["
				: "]")
				: "");
	}

	public static String trimSingleQuotes(String htmlElement) {
		return htmlElement.replace("'", "");
	}
}
