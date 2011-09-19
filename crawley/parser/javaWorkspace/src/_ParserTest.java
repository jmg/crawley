import static org.junit.Assert.*;

import org.junit.*;



public class _ParserTest {

	@Test
	public void primerosElementos() {
		assertEquals("pido el primer 'p' del html", 
				"return PyQuery(html).query('p')[0]", new Parser().parse("first < tag:'p' => innerHTML"));
		assertEquals("pido el primer elemento con tag = p o tag = div",
				"return [PyQuery(html).query('p')[0], PyQuery(html).query('div')[0]]",new Parser().parse("first < tag:['p','div'] => innerHTML"));
		
		assertEquals("pido el primer elemento que tiene id = unid",
				"return PyQuery(html).query('#unid')[0]", new Parser().parse("first < id:'unID' => innerHTML"));
		assertEquals("pido el primer elemento con id = unid o id = otroid",
				"return [PyQuery(html).query('#unid')[0], PyQuery(html).query('#otroid')[0]]",new Parser().parse("first < id:['unid','otroid'] => innerHTML"));
		
		assertEquals("pido el primer elemento que tiene clase = mi-clase",
				"return PyQuery(html).query('.mi-clase')[0]", new Parser().parse("first < class:'mi-clase' => innerHTML"));
		assertEquals("pido el primer elemento con clase = mi-clase o clase = otra-clase",
				"return [PyQuery(html).query('.mi-clase')[0], PyQuery(html).query('.otra-clase')[0]]",new Parser().parse("first < class:['mi-clase','otra-clase'] => innerHTML"));		
	}
	
	@Test
	public void ultimosElementos() {
		assertEquals("pido el ultimo 'p' del html", 
				"return PyQuery(html).query('p')[-1]", new Parser().parse("last < tag:'p' => innerHTML"));
		assertEquals("pido el ultimo elemento con tag = p o tag = div",
				"return [PyQuery(html).query('p')[-1], PyQuery(html).query('div')[-1]]",new Parser().parse("last < tag:['p','div'] => innerHTML"));

		assertEquals("pido el ultimo elemento que tiene id = unid",
				"return PyQuery(html).query('#unid')[-1]", new Parser().parse("last < id:'unID' => innerHTML"));
		assertEquals("pido el ultimo elemento con id = unid o id = otroid",
				"return [PyQuery(html).query('#unid')[-1], PyQuery(html).query('#otroid')[-1]]",new Parser().parse("last < id:['unid','otroid'] => innerHTML"));

		assertEquals("pido el ultimo elemento que tiene clase = mi-clase",
				"return PyQuery(html).query('.mi-clase')[-1]", new Parser().parse("last < class:'mi-clase' => innerHTML"));
		assertEquals("pido el ultimo elemento con clase = mi-clase o clase = otra-clase",
				"return [PyQuery(html).query('.mi-clase')[-1], PyQuery(html).query('.otra-clase')[-1]]",new Parser().parse("last < class:['mi-clase','otra-clase'] => innerHTML"));
	}
	
	
	@Test
	public void todosLosElementos() {
		assertEquals("pido todos los 'p' del html",
				"return PyQuery(html).query('p')", new Parser().parse("all < tag:'p' => innerHTML"));
		assertEquals("pido todos los elementos con tag = p o tag = div",
				"return [PyQuery(html).query('p'), PyQuery(html).query('div')]",new Parser().parse("all < tag:['p','div'] => innerHTML"));
		
		assertEquals("pido todos los elementos que tiene id = unid",
				"return PyQuery(html).query('#unid')", new Parser().parse("all < id:'unID' => innerHTML"));
		assertEquals("pido el ultimo elemento con id = unid o id = otroid",
				"return [PyQuery(html).query('#unid'), PyQuery(html).query('#otroid')]",new Parser().parse("all < id:['unid','otroid'] => innerHTML"));

		assertEquals("pido todos los elementos que tiene clase = mi-clase",
				"return PyQuery(html).query('.mi-clase')", new Parser().parse("all < class:'mi-clase' => innerHTML"));
		assertEquals("pido todos los elementos con clase = mi-clase o clase = otra-clase",
				"return [PyQuery(html).query('.mi-clase'), PyQuery(html).query('.otra-clase')]",new Parser().parse("all < class:['mi-clase','otra-clase'] => innerHTML"));
	}
}
