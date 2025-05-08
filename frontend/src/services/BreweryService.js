import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

export default {
  /**
   * Get breweries with optional filters
   * @param {Object} params - Query parameters for filtering
   * @returns {Promise} - Promise with brewery data
   */
  getBreweries(params = {}) {
    return axios.get(`${API_URL}/breweries/`, { params });
  },
  
  /**
   * Get a specific brewery by ID
   * @param {string} id - Brewery ID
   * @returns {Promise} - Promise with brewery data
   */
  getBreweryById(id) {
    return axios.get(`${API_URL}/breweries/${id}/`);
  },
  
  /**
   * Search breweries by keyword
   * @param {string} query - Search term
   * @returns {Promise} - Promise with brewery data
   */
  searchBreweries(query) {
    return axios.get(`${API_URL}/breweries/search/`, { 
      params: { query } 
    });
  },
  
  /**
   * Get a random brewery
   * @returns {Promise} - Promise with brewery data
   */
  getRandomBrewery() {
    return axios.get(`${API_URL}/breweries/random/`);
  }
};
