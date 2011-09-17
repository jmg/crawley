
public class Parser {

	public String parse(String crawleyDSL) {
		String[] parsingString = crawleyDSL.split("=>");
		String actionSection = parsingString[0].toLowerCase();
		//String getSection = parsingString[1];
		
		return "PyQuery(html).query('" + ((actionSection.contains("tag:'p'")) ? "p" : "div") + "')" + ((actionSection.contains("for")) ? "" : ((actionSection.contains("first")) ? "[0]" : "[-1]"));  
		
		//if (crawleyDSL.contains("'p'")) return "PyQuery(html).query('p')[0]";
		//else if (crawleyDSL.contains("'div'")) return "PyQuery(html).query('div')[0]";
		//return "";
	}

}
