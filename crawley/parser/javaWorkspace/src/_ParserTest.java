import static org.junit.Assert.*;

import org.junit.*;



public class _ParserTest {

	@Test
	public void lePasoUnaLineaDeDSLyMeRetornaAlgoParseado() {
		assertEquals("pido el primer 'p' del html", "PyQuery(html).query('p')[0]", new Parser().parse("first : tag:'p' => innerHTML"));
		assertEquals("pido el primer 'div' del html", "PyQuery(html).query('div')[0]", new Parser().parse("first : tag:'div' => innerHTML"));
		assertEquals("pido el ultimo 'p' del html", "PyQuery(html).query('p')[-1]", new Parser().parse("last : tag:'p' => innerHTML"));
		assertEquals("pido el ultimo 'div' del html", "PyQuery(html).query('div')[-1]", new Parser().parse("last : tag:'div' => innerHTML"));
		assertEquals("pido todos los 'p' del html","PyQuery(html).query('p')", new Parser().parse("for : tag:'p' => innerHTML"));
		assertEquals("pido todos los 'div' del html","PyQuery(html).query('div')", new Parser().parse("for : tag:'div' => innerHTML"));
	}
	
}
