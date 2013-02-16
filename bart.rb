#!/Users/tp/.rvm/rubies/ruby-1.9.3-p194/bin/ruby
require 'open-uri'
require 'nokogiri'
require 'colorize'

INDENT = " "*3
DIRECTION = {'s' => 'south', 'n' => 'north'}
WALKING = 3
WARNING = 10

def get_time(orig, dir)
  base_url = "http://api.bart.gov/api/etd.aspx?cmd=etd&key=MW9S-E7SL-26DU-VV8V"
  powl_url = "#{base_url}&ORIG=#{orig}&dir=#{dir}"
  doc = Nokogiri::XML.parse(open(URI.parse powl_url))

  puts
  puts INDENT + "Heading #{DIRECTION[dir]} from #{doc.css('name').text}".underline.light_green

  doc.css('etd').each do |etd|
    estimates = etd.css('estimate')
      .collect { |estimate| estimate.css('minutes').text.rjust(2) }

    next_train = estimates.select { |est| est.to_i > WALKING }.first
    # estimates[0] = estimates[0].light_yellow
    estimates.each_with_index do |est, i|
      if est.to_i > 3
        estimates[i] = estimates[i].light_yellow
        break
      end
    end

    print INDENT
    print "[#{etd.css('abbreviation').text}]   "
    print "#{etd.css('destination').text.light_white}".ljust(36)
    print estimates.join(" <- ") + " minutes"
    print " " + " LEAVE NOW! ".on_red.light_white if next_train.to_i < WARNING #&& next_train.to_i > 3
    puts
  end
  # puts powl_url
end

station = !ARGV[0].nil? ? ARGV[0].upcase : 'POWL'
direction = (ARGV[1] =~ /^[sn]$/i) ? ARGV[1].downcase : 's'

get_time(station, direction)

# puts String.color_matrix