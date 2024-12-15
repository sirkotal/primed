class PagesController < ApplicationController
  def index
    # redirect_to action: "search"
  end
  def search
    @query = params[:query]
    case params[:type]
      when 'baseline'
        results_file = Rails.root.join('..', 'solr_simple_response.json')
        script = Rails.root.join('../docker', 'request_simple.py')
      when 'advanced'
        results_file = Rails.root.join('..', 'solr_adv_response.json')
        script = Rails.root.join('../docker', 'request_advanced.py')
      when 'semantic'
        results_file = Rails.root.join('..', 'solr_sem_response.json')
        script = Rails.root.join('../docker', 'request_semantic.py')
    end
    puts results_file
    
    stdout_str, stderr_str, status = Open3.capture3("python3 #{script} '#{@query}'")
    
    if status.success?
      if File.exist?(results_file)
        @results = JSON.parse(File.read(results_file))
      else
        @results = { "error" => "No results found" }
      end
    end
  end
end
