import java.util.HashMap;
import java.util.Map;


public abstract class Property {
	
	protected static Map<String, Property> populateProperties() {
		Map<String, Property> propertyElements = new HashMap<String, Property>();
		propertyElements.put("id", new IDProperty());
		propertyElements.put("tag", new TagProperty());
		propertyElements.put("class", new ClassProperty());
		return propertyElements;
	}
	
	public static Property getProperty(String property) {
		return populateProperties().get(property);
	}
}
