Person = Struct.new(:id, :name)

list = [
  Person.new(1, 'Alice'),
  Person.new(2, 'Bob')
]

Hash[list.map {|e| [e.id, e]}]

#  => {1=>#<struct Person id=1, name="Alice">, 2=>#<struct Person id=2, name="Bob">}
