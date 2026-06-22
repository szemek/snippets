require 'date'
require 'logger'
require 'octokit'
require 'pry'

f = open("#{ENV['HOME']}/.netrc", "r")
netrc = f.read
github_token = netrc.match(/ghp_.*/)[0]

client = Octokit::Client.new(access_token: github_token, per_page: 100)

# read previous report
report_name = Dir["report-*.tsv"].sort.reverse.first
puts "Previous report: #{report_name}"
report_file = open(report_name, "r")
checkpoint = report_file.read.lines.first.split("\t").last.strip
report_file.close

# get pull requests
pull_requests = client.search_issues('is:pr author:szemek archived:false is:closed sort:updated-desc')

pull_requests = pull_requests.items.select do |pr|
  pr[:html_url].include?('/my-company/')
end

current_date = Date.today.strftime("%Y-%m-%d")
new_report_name = "report-#{current_date}.tsv"
new_report_file = open(new_report_name, "a")

pull_requests.each do |pr|
  if pr[:updated_at].to_s > checkpoint
    new_report_file.puts("#{pr[:title]}\t#{pr[:html_url]}\t#{pr[:updated_at]}")
  end
end

new_report_file.close

puts "Saved new report to: #{new_report_name}"
