require 'aws-sdk'
require 'logger'

glue = Aws::Glue::Client.new(region: 'eu-west-1', logger: Logger.new($stdout), log_level: :debug, http_wire_trace: true)
job = glue.get_job(job_name: 'job')
