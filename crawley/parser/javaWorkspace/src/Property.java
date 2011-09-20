import java.util.HashMap;
import java.util.Map;


public abstract class Property {

	private static Map<String, Property> propertyElements = new HashMap<String, Property>();
	
	protected static void populateProperties() {
		propertyElements.put("id", new IDProperty());
		propertyElements.put("tag", new TagProperty());
		propertyElements.put("class", new ClassProperty());
	}
	
	public static Property getProperty(String property) {
		populateProperties();
		return propertyElements.get(property);
	}
}
