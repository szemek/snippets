# count records in PostgreSQL via ActiveRecord
connection = ActiveRecord::Base.connection
query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
tables = connection.execute(query).values.flatten
tables.map { |name| connection.execute("SELECT COUNT(*) FROM #{name}").values.flatten.first.to_i }.reduce(:+)
