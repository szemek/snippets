require 'uri'
uri = URI(ARGV[0])
puts "mysql -h #{uri.host} -D #{uri.path.delete('/')} -u #{uri.user} -p#{uri.password}"
