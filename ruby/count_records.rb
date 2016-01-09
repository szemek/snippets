# count records via ActiveRecord
connection = ActiveRecord::Base.connection
tables = connection.tables
tables.map { |name| connection.execute("SELECT COUNT(*) FROM #{name}").values.flatten.first.to_i }.reduce(:+)
