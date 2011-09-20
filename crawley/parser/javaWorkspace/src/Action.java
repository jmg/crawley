import java.util.HashMap;
import java.util.Map;


public abstract class Action {
	
	protected static Map<String, Action> populateActions() {
		Map <String, Action> actionElements = new HashMap<String, Action>();
		actionElements.put("first", new FirstAction());
		actionElements.put("last", new LastAction());
		actionElements.put("all", new AllAction());
		return actionElements;
	}
	
	public static Action getAction(String action) {
		return populateActions().get(action);
	}
}
