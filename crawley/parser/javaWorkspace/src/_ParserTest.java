import static org.junit.Assert.*;

import org.junit.*;



public class _ParserTest {

	@Test
	public void pidoPrimerosElementosPorTagYRetornoElContenido() {
		assertEquals("pido el primer 'p' del html", "return PyQuery(html).query('p')[0]", new Parser().parse("first < tag:'p' => innerHTML"));
		assertEquals("pido el primer 'div' del html", "return PyQuery(html).query('div')[0]", new Parser().parse("first < tag:'div' => innerHTML"));
	}
	
	@Test
	public void pidoUltimosElementosPorTagYRetornoElContenido() {
		assertEquals("pido el ultimo 'p' del html", "return PyQuery(html).query('p')[-1]", new Parser().parse("last < tag:'p' => innerHTML"));
		assertEquals("pido el ultimo 'div' del html", "return PyQuery(html).query('div')[-1]", new Parser().parse("last < tag:'div' => innerHTML"));
	}
	
	@Test
	public void pidoTodosLosElementosPorTagYRetornoElContenido() {
		assertEquals("pido todos los 'p' del html","return PyQuery(html).query('p')", new Parser().parse("all < tag:'p' => innerHTML"));
		assertEquals("pido todos los 'div' del html","return PyQuery(html).query('div')", new Parser().parse("all < tag:'div' => innerHTML"));
	}
	
	@Test
	public void pidoTodosElementoPorID() {
		assertEquals("pido todos los elementos que tiene id = unid","return PyQuery(html).query('#unid')", new Parser().parse("all < id:'unID' => innerHTML"));
		assertEquals("pido todos los elementos que tiene id = otroid","return PyQuery(html).query('#otroid')", new Parser().parse("all < id:'otroID' => innerHTML"));
	}
	
	@Test
	public void pidoElPrimerElementoPorID() {
		assertEquals("pido el primer elemento que tiene id = unid","return PyQuery(html).query('#unid')[0]", new Parser().parse("first < id:'unID' => innerHTML"));
		assertEquals("pido el primer elemento que tiene id = otroid","return PyQuery(html).query('#otroid')[0]", new Parser().parse("first < id:'otroID' => innerHTML"));
	}
	
	@Test
	public void pidoElUltimoElementoPorID() {
		assertEquals("pido el ultimo elemento que tiene id = unid","return PyQuery(html).query('#unid')[-1]", new Parser().parse("last < id:'unID' => innerHTML"));
		assertEquals("pido el ultimo elemento que tiene id = otroid","return PyQuery(html).query('#otroid')[-1]", new Parser().parse("last < id:'otroID' => innerHTML"));
	}
	
	@Test
	public void pidoTodosElementoPorClase() {
		assertEquals("pido todos los elementos que tiene clase = mi-clase","return PyQuery(html).query('.mi-clase')", new Parser().parse("all < class:'mi-clase' => innerHTML"));
		//assertEquals("pido todos los elementos que tiene clase = (mi-clase || otra-clase)","return PyQuery(html).query('#otroid')", new Parser().parse("all < id:'otroID' => innerHTML"));
	}
	
	@Test
	public void pidoElPrimerElementoPorClase() {
		assertEquals("pido el primer elemento que tiene clase = mi-clase","return PyQuery(html).query('.mi-clase')[0]", new Parser().parse("first < class:'mi-clase' => innerHTML"));
		//assertEquals("pido el primer elemento que tiene clase = (mi-clase || otra-clase)","return PyQuery(html).query('#otroid')[0]", new Parser().parse("first < id:'otroID' => innerHTML"));
	}
	
	@Test
	public void pidoElUltimoElementoPorClase() {
		assertEquals("pido el ultimo elemento que tiene clase = mi-clase","return PyQuery(html).query('.mi-clase')[-1]", new Parser().parse("last < class:'mi-clase' => innerHTML"));
		//assertEquals("pido el ultimo elemento que tiene id = otroid","return PyQuery(html).query('#otroid')[-1]", new Parser().parse("last < id:'otroID' => innerHTML"));
	}
}
