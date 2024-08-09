'''
Com @property, você e sua equipe não precisarão modificar qualquer uma dessas linhas, pois você poderá adicionar getters e setters "internamente" sem afetar a 
sintaxe usada para acessar ou modificar o atributo quando ele era público.  É possível definir propriedades com a sintaxe @property, que é mais compacta e legível.
@property pode ser considerada a maneira do Python de definir getters, setters e deleters.  Ao definir as propriedades, você pode alterar a implementação interna
de uma classe sem afetar o programa. Desse modo, você pode adicionar os getters, setters e deleters que agem como intermediadores "internamente" para evitar o
acesso ou a modificação direta dos dados.

@property - Usado para indicar que vamos definir uma propriedade.

def preco(self) - O cabeçalho. Observe como o getter tem o nome exato da propriedade que estamos definindo: preco. 
    * Esse é o nome que vamos usar para acessar e modificar o atributo fora da classe. O método recebe apenas um parâmetro formal, self, 
    * que é uma referência da instância.

return self._preco - Essa linha é exatamente o que você esperaria de um getter normal. O valor do atributo protegido é retornado.   

@preco.setter - Usado para indicar que esse é o método setter para a propriedade preco. Observe que não usamos @property.setter, mas, sim, @preco.setter. 
    * O nome da propriedade é incluído antes de .setter.

def preco(self, novo_preco): - O cabeçalho e a lista de parâmetros. Observe como o nome da propriedade é usado como o nome do setter. 
    * Também temos um segundo parâmetro formal (novo_preco), que é o novo valor que será atribuído ao atributo preco (se o valor for válido).

@preco.deleter - Usado para indicar que esse é o método deleter para a propriedade preco. 
    * Observe que essa linha é muito semelhante a @preco.setter, mas agora estamos definindo o método deleter, por isso escrevemos @preco.deleter.   
    
def preco(self): - O cabeçalho. Esse método tem apenas um parâmetro formal definido, self.

del self._preco - O corpo do método, onde excluímos o atributo de instância.
'''

class Casa:

	def __init__(self, preco):
		self._preco = preco

	@property
	def preco(self):                        # Um getter - para acessar o valor do atributo. 
		return self._preco
	
	@preco.setter
	def preco(self, new_price):             # Um setter - para definir o valor do atributo.
		if novo_preco > 0 and isinstance(novo_preco, float):
			self._preco = novo_preco
		else:
			print("Insira um preço válido")

	@preco.deleter
	def preco(self):                       # Um deleter - para excluir o atributo de instância.
		del self._preco



'''O preço, agora, está "protegido"
Observe que o atributo preco agora está "protegido", pois adicionamos uma sublinha (_) precedente ao seu nome em self._preco
Em Python, por convenção (texto em inglês), quando você adiciona uma sublinha precedendo o nome de uma propriedade, 
você está dizendo aos outros desenvolvedores que ela não deve ser acessada ou modificada diretamente de fora da classe. 
Ela somente deve ser acessada por intermediadores (getters e setters), caso estejam disponíveis.




'''