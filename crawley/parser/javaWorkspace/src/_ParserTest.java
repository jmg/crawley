import static org.junit.Assert.*;

import org.junit.*;



public class _ParserTest {

	@Test
	public void pidoPrimerosElementosPorTagYRetornoElContenido() {
		assertEquals("pido el primer 'p' del html", "return PyQuery(html).query('p')[0]", new Parser().parse("first < tag:'p' => innerHTML"));
		assertEquals("pido el primer 'div' del html", "return PyQuery(html).query('div')[0]", new Parser().parse("first < tag:'div' => innerHTML"));
		assertEquals("pido el primer 'table' del html", "return PyQuery(html).query('table')[0]", new Parser().parse("first < tag:'table' => innerHTML"));
		assertEquals("pido el primer 'ol' del html", "return PyQuery(html).query('ol')[0]", new Parser().parse("first < tag:'ol' => innerHTML"));
		assertEquals("pido el primer 'ul' del html", "return PyQuery(html).query('ul')[0]", new Parser().parse("first < tag:'ul' => innerHTML"));
	}
	
	@Test
	public void pidoUltimosElementosPorTagYRetornoElContenido() {
		assertEquals("pido el ultimo 'p' del html", "return PyQuery(html).query('p')[-1]", new Parser().parse("last < tag:'p' => innerHTML"));
		assertEquals("pido el ultimo 'div' del html", "return PyQuery(html).query('div')[-1]", new Parser().parse("last < tag:'div' => innerHTML"));
		assertEquals("pido el ultimo 'table' del html", "return PyQuery(html).query('table')[-1]", new Parser().parse("last < tag:'table' => innerHTML"));
		assertEquals("pido el ultimo 'ol' del html", "return PyQuery(html).query('ol')[-1]", new Parser().parse("last < tag:'ol' => innerHTML"));
		assertEquals("pido el ultimo 'ul' del html", "return PyQuery(html).query('ul')[-1]", new Parser().parse("last < tag:'ul' => innerHTML"));
	}
	
	@Test
	public void pidoTodosLosElementosPorTagYRetornoElContenido() {
		assertEquals("pido todos los 'p' del html","return PyQuery(html).query('p')", new Parser().parse("all < tag:'p' => innerHTML"));
		assertEquals("pido todos los 'div' del html","return PyQuery(html).query('div')", new Parser().parse("all < tag:'div' => innerHTML"));
		assertEquals("pido todos los 'table' del html", "return PyQuery(html).query('table')", new Parser().parse("all < tag:'table' => innerHTML"));
		assertEquals("pido todos los 'ol' del html", "return PyQuery(html).query('ol')", new Parser().parse("all < tag:'ol' => innerHTML"));
		assertEquals("pido todos los 'ul' del html", "return PyQuery(html).query('ul')", new Parser().parse("all < tag:'ul' => innerHTML"));
	}
}
