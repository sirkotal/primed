class PagesController < ApplicationController
  def index
    # redirect_to action: "search"
  end
  def search
    results_file = Rails.root.join('..', 'solr_simple_response.json')
    puts results_file
    
    if File.exist?(results_file)
      @results = JSON.parse(File.read(results_file))
    else
      @results = { "error" => "No results found" }
    end
  end
end
