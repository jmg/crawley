import java.util.HashMap;
import java.util.Map;


public abstract class Action {
	private static Map<String, Action> actionElements = new HashMap<String, Action>();
	
	protected static void populateActions() {
		actionElements.put("first", new FirstAction());
		actionElements.put("last", new LastAction());
		actionElements.put("all", new AllAction());
	}
	
	public static Action getAction(String action) {
		populateActions();
		return actionElements.get(action);
	}
}
