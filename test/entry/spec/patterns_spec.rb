# coding: utf-8
require_relative "./spec_helper"
require "json"

# Load pattern test cases
pattern_data = Dir[File.join(File.dirname(__FILE__), 'pattern_data/**/*.json')]

pattern_data.each do |data_file|
  # Load test case data from file
  @@test_case = JSON.parse(File.read(data_file))

  describe "#{@@test_case['name']} (#{@@test_case['pattern']}, #{File.basename(data_file)})" do
    @@test_case['cases'].each_with_index do |item,i|
      name = "##{i} - #{item["in"][0..25]}..."
      expected_fields = item["out"].keys
      pattern = @@test_case['pattern']

      # Expected fields are present, have expected value, and no other fields are present
      it "'#{name}' should be correct" do
        match_res = grok_match(pattern, item['in'])
        # Ignore logstash added fields. These are always present.
        result = match_res.select{ |x| !['@version', '@timestamp', 'message'].include?(x) }

        # test for missing fields in match output
        missing = expected_fields.select { |f| not result.keys.include?(f) }
        msg = "\nFields missing in pattern output: #{missing}\nComplete grok output: #{result}\n\n--"
        expect(missing).to be_empty, msg

        # test for unexpected fields in match output
        extra = result.keys.select { |f| not expected_fields.include?(f) }
        msg = "\nUnexpected fields in pattern output: #{extra}\nComplete grok output: #{result}\n\n--"
        expect(extra).to be_empty, msg

        # test for field values
        item['out'].each do |name,value|
          msg = "\nField mismatch: '#{name}'\nExpected: #{value}\nGot: #{match_res[name]}\nComplete grok output: #{result}\n\n--"
          expect(result[name]).to eq(value), msg
        end
      end
    end
  end
end

