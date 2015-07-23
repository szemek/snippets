# See http://jordan.broughs.net/archives/2012/07/enumerablecount_by-for-ruby

module Enumerable
  def count_by(&block)
    Hash[group_by(&block).map { |key,vals| [key, vals.size] }]
  end
end
