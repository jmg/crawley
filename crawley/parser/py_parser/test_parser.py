import unittest
from parser import Parser

class ParserTest(unittest.TestCase):

	def test_primeros_elementos(self):
        
		self.assertEquals("return PyQuery(html).query('p')[0]", Parser().parse("first < tag:'p' => innerHTML"), "pido el primer 'p' del html")
		self.assertEquals("return [PyQuery(html).query('p')[0], PyQuery(html).query('div')[0]]", Parser().parse("first < tag:['p','div'] => innerHTML"), "pido el primer elemento con tag = p o tag = div")
		
		self.assertEquals("return PyQuery(html).query('#unid')[0]", Parser().parse("first < id:'unID' => innerHTML"), "pido el primer elemento que tiene id = unid")
		self.assertEquals("return [PyQuery(html).query('#unid')[0], PyQuery(html).query('#otroid')[0]]",Parser().parse("first < id:['unid','otroid'] => innerHTML"), "pido el primer elemento con id = unid o id = otroid")
		
		self.assertEquals("return PyQuery(html).query('.mi-clase')[0]", Parser().parse("first < class:'mi-clase' => innerHTML"), "pido el primer elemento que tiene clase = mi-clase")
		self.assertEquals("return [PyQuery(html).query('.mi-clase')[0], PyQuery(html).query('.otra-clase')[0]]",Parser().parse("first < class:['mi-clase','otra-clase'] => innerHTML"), "pido el primer elemento con clase = mi-clase o clase = otra-clase")
	
	def test_ultimos_elementos(self):
        
		self.assertEquals("return PyQuery(html).query('p')[-1]", Parser().parse("last < tag:'p' => innerHTML"), "pido el ultimo 'p' del html")
		self.assertEquals("return [PyQuery(html).query('p')[-1], PyQuery(html).query('div')[-1]]",Parser().parse("last < tag:['p','div'] => innerHTML"), "pido el ultimo elemento con tag = p o tag = div")

		self.assertEquals("return PyQuery(html).query('#unid')[-1]", Parser().parse("last < id:'unID' => innerHTML"), "pido el ultimo elemento que tiene id = unid")
		self.assertEquals("return [PyQuery(html).query('#unid')[-1], PyQuery(html).query('#otroid')[-1]]",Parser().parse("last < id:['unid','otroid'] => innerHTML"), "pido el ultimo elemento con id = unid o id = otroid")

		self.assertEquals("return PyQuery(html).query('.mi-clase')[-1]", Parser().parse("last < class:'mi-clase' => innerHTML"), "pido el ultimo elemento que tiene clase = mi-clase")
		self.assertEquals("return [PyQuery(html).query('.mi-clase')[-1], PyQuery(html).query('.otra-clase')[-1]]",Parser().parse("last < class:['mi-clase','otra-clase'] => innerHTML"), "pido el ultimo elemento con clase = mi-clase o clase = otra-clase")

	def test_todos_los_elementos(self):
		
		self.assertEquals("return PyQuery(html).query('p')", Parser().parse("all < tag:'p' => innerHTML"), "pido todos los 'p' del html")
		self.assertEquals("return [PyQuery(html).query('p'), PyQuery(html).query('div')]",Parser().parse("all < tag:['p','div'] => innerHTML"), "pido todos los elementos con tag = p o tag = div")

		self.assertEquals("return PyQuery(html).query('#unid')", Parser().parse("all < id:'unID' => innerHTML"), "pido todos los elementos que tiene id = unid")
		self.assertEquals("return [PyQuery(html).query('#unid'), PyQuery(html).query('#otroid')]",Parser().parse("all < id:['unid','otroid'] => innerHTML"), "pido el ultimo elemento con id = unid o id = otroid")

		self.assertEquals("return PyQuery(html).query('.mi-clase')", Parser().parse("all < class:'mi-clase' => innerHTML"), "pido todos los elementos que tiene clase = mi-clase")
		self.assertEquals("return [PyQuery(html).query('.mi-clase'), PyQuery(html).query('.otra-clase')]",Parser().parse("all < class:['mi-clase','otra-clase'] => innerHTML"), "pido todos los elementos con clase = mi-clase o clase = otra-clase")


if __name__ == "__main__":
    
    unittest.main()
