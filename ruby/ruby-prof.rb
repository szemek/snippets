# inspired by https://speakerdeck.com/eileencodes/fullstackfest-2015-how-to-performance

require 'ruby-prof'

RubyProf.measure_mode = RubyProf::WALL_TIME

result = RubyProf.profile do
  # ...
end

File.open('output.html', 'w') do |file|
  RubyProf::GraphHtmlPrinter.new(result).print(file)
end
