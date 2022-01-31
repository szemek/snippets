require 'srt'
require 'json'

transcripts = Dir['**/*.json']

filename = transcripts[0]

f = open(filename, 'r')
transcript = JSON.parse(f.read)
f.close

f = open(filename.gsub('.json', '.srt'), 'w')
sequence = 1

transcript['results'].each do |block|
  words = block['alternatives'].first['words']

  words.each do |word|
    line = SRT::Line.new(
      sequence: sequence,
      start_time: word['startTime'].to_f,
      end_time: word['endTime'].to_f,
      text: word['word']
    )

    f.write("#{line.to_s}\n")

    sequence += 1
  end
end

f.close
