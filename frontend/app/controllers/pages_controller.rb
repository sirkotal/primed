class PagesController < ApplicationController
  def index
  end
  def search
    query = params[:query]
    search_type = params[:type] || 'baseline'
    api_url = 'http://127.0.0.1:8000'

    response = HTTP.post(api_url, form: { query: query })

    if response.status.success?
      @results = response.parse['results']
    else
      @error = response.parse['error'] || "An error occurred"
    end

    render :search_results
  end
end
