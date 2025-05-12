<template>
  <div class="container mx-auto p-4">
    <h1 class="text-2xl font-bold mb-6">Brewery Explorer</h1>

    <!-- Filters -->
    <div class="mb-6 grid grid-cols-1 md:grid-cols-3 gap-4">
      <div>
        <label class="block text-sm font-medium mb-1">Brewery Type</label>
        <select
          id="brewery-type"
          v-model="selectedType"
          class="w-full border rounded p-2"
          @change="fetchBreweries"
        >
          <option value="">All Types</option>
          <option v-for="type in breweryTypes" :key="type" :value="type">
            {{ type }}
          </option>
        </select>
      </div>

      <div>
        <label class="block text-sm font-medium mb-1">Search</label>
        <input
          id="search-input"
          v-model="searchQuery"
          class="w-full border rounded p-2"
          placeholder="Search by name"
          @input="debouncedSearch"
        />
      </div>

      <div>
        <label class="block text-sm font-medium mb-1">Group By</label>
        <select
          id="group-by"
          v-model="groupBy"
          class="w-full border rounded p-2"
          @change="updateGroups"
        >
          <option value="">No Grouping</option>
          <option value="brewery_type">Brewery Type</option>
          <option value="state">State</option>
          <option value="city">City</option>
          <option value="country">Country</option>
        </select>
      </div>
    </div>

    <div class="mb-6 grid grid-cols-1 md:grid-cols-3 gap-4">
      <div>
        <label class="block text-sm font-medium mb-1">Filter by State</label>
        <input
          v-model="filters.by_state"
          class="w-full border rounded p-2"
          placeholder="Full state name"
          @input="debouncedStateSearch"
        />
      </div>

      <div>
        <label class="block text-sm font-medium mb-1">Filter by City</label>
        <input
          v-model="filters.by_city"
          class="w-full border rounded p-2"
          placeholder="City name"
          @input="debouncedCitySearch"
        />
      </div>

      <div>
        <label class="block text-sm font-medium mb-1">Per Page</label>
        <select
          v-model="perPage"
          class="w-full border rounded p-2"
          @change="fetchBreweries"
        >
          <option value="10">10</option>
          <option value="25">25</option>
          <option value="50">50</option>
          <option value="100">100</option>
          <option value="200">200</option>
        </select>
      </div>
    </div>

    <!-- Random Brewery Button -->
    <div class="mb-6">
      <button
        id="random-brewery-btn"
        @click="fetchRandomBrewery"
        class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
      >
        Get Random Brewery
      </button>
    </div>

    <!-- Chart -->
    <div v-if="groupBy && breweries.length > 0" class="mb-8">
      <h2 class="text-xl font-bold mb-4">{{ groupByLabel }}</h2>
      <div
        ref="chartContainer"
        class="w-full h-80 bg-white p-4 rounded shadow"
      ></div>
    </div>

    <!-- Breweries List -->
    <div v-if="loading" class="py-8 text-center">
      <div
        class="inline-block animate-spin rounded-full h-8 w-8 border-4 border-t-blue-500"
      ></div>
      <p class="mt-2">Loading breweries...</p>
    </div>

    <div v-else-if="error" class="py-8 text-center text-red-500">
      {{ error }}
    </div>

    <div v-else-if="breweries.length === 0" class="py-8 text-center">
      <p>No breweries found matching your criteria.</p>
    </div>

    <div v-else>
      <h2 class="text-xl font-bold mb-4">Breweries ({{ breweries.length }})</h2>

      <div class="bg-white shadow rounded-lg overflow-hidden">
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Name
                </th>
                <th
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Type
                </th>
                <th
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  City
                </th>
                <th
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  State
                </th>
                <th
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Country
                </th>
                <th
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Website
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="brewery in breweries" :key="brewery.id">
                <td class="px-6 py-4 whitespace-nowrap">{{ brewery.name }}</td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span
                    class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                    :class="getTypeClass(brewery.brewery_type)"
                  >
                    {{ brewery.brewery_type }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">{{ brewery.city }}</td>
                <td class="px-6 py-4 whitespace-nowrap">{{ brewery.state }}</td>
                <td class="px-6 py-4 whitespace-nowrap">
                  {{ brewery.country }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <a
                    v-if="brewery.website_url"
                    :href="brewery.website_url"
                    target="_blank"
                    class="text-blue-600 hover:text-blue-900"
                  >
                    Visit
                  </a>
                  <span v-else class="text-gray-400">N/A</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Pagination -->
      <div class="mt-4 flex justify-between items-center">
        <button
          :disabled="currentPage === 1"
          @click="prevPage"
          class="bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-2 px-4 rounded disabled:opacity-50"
        >
          Previous
        </button>
        <span>Page {{ currentPage }}</span>
        <button
          @click="nextPage"
          class="bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-2 px-4 rounded"
        >
          Next
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import {ref, onMounted, computed, watch, nextTick} from 'vue'
import * as d3 from 'd3'
import _ from 'lodash'
import axios from 'axios'

export default {
  name: 'BreweryExplorer',

  setup() {
    const API_URL = 'http://localhost:8000/api/breweries'

    const breweries = ref([])
    const loading = ref(false)
    const error = ref(null)
    const selectedType = ref('')
    const searchQuery = ref('')
    const groupBy = ref('')
    const currentPage = ref(1)
    const perPage = ref(50)
    const chartContainer = ref(null)
    const groups = ref({})
    const filters = ref({
      by_state: '',
      by_city: '',
    })

    const breweryTypes = [
      'micro',
      'nano',
      'regional',
      'brewpub',
      'large',
      'planning',
      'bar',
      'contract',
      'proprietor',
      'closed',
    ]

    const groupByLabel = computed(() => {
      const labels = {
        brewery_type: 'Breweries by Type',
        state: 'Breweries by State',
        city: 'Breweries by City',
        country: 'Breweries by Country',
      }
      return labels[groupBy.value] || 'Breweries'
    })

    const fetchBreweries = async () => {
      loading.value = true
      error.value = null

      try {
        const params = {
          page: currentPage.value,
          per_page: perPage.value,
        }

        if (selectedType.value) {
          params.by_type = selectedType.value
        }

        if (filters.value.by_state) {
          params.by_state = filters.value.by_state
        }

        if (filters.value.by_city) {
          params.by_city = filters.value.by_city
        }

        const response = await axios.get(API_URL, {params})
        breweries.value = response.data

        if (groupBy.value) {
          renderChart()
        }
      } catch (err) {
        error.value = 'Failed to fetch breweries'
        console.error('Error fetching breweries:', err)
      } finally {
        loading.value = false
      }
    }

    const searchBreweries = async () => {
      if (!searchQuery.value) {
        await fetchBreweries()
        return
      }

      loading.value = true
      error.value = null

      try {
        const response = await axios.get(`${API_URL}/search`, {
          params: {query: searchQuery.value},
        })
        breweries.value = response.data

        if (groupBy.value) {
          renderChart()
        }
      } catch (err) {
        error.value = 'Failed to search breweries'
        console.error('Error searching breweries:', err)
      } finally {
        loading.value = false
      }
    }

    const fetchRandomBrewery = async () => {
      loading.value = true
      error.value = null

      try {
        const response = await axios.get(`${API_URL}/random`, {
          params: {size: 1},
        })
        breweries.value = response.data

        if (groupBy.value) {
          renderChart()
        }
      } catch (err) {
        error.value = 'Failed to fetch random brewery'
        console.error('Error fetching random brewery:', err)
      } finally {
        loading.value = false
      }
    }

    const groupBreweriesByAttribute = () => {
      if (!groupBy.value || !breweries.value.length) return null

      // Group data by selected attribute
      const grouped = {}
      breweries.value.forEach((brewery) => {
        const key = brewery[groupBy.value] || 'Unknown'
        if (!grouped[key]) {
          grouped[key] = []
        }
        grouped[key].push(brewery)
      })

      // Update the groups ref for testing
      groups.value = grouped

      return grouped
    }

    const renderChart = async () => {
      if (!chartContainer.value || !groupBy.value || !breweries.value.length)
        return

      // Clear previous chart
      d3.select(chartContainer.value).selectAll('*').remove()

      const grouped = groupBreweriesByAttribute()
      if (!grouped) return

      // Prepare data for chart
      const data = Object.entries(grouped).map(([key, items]) => ({
        name: key,
        value: items.length,
      }))

      // Sort data by value descending
      data.sort((a, b) => b.value - a.value)

      // Limit to top 10 if too many categories
      const chartData =
        data.length > 10
          ? [
              ...data.slice(0, 9),
              {
                name: 'Others',
                value: data.slice(9).reduce((sum, item) => sum + item.value, 0),
              },
            ]
          : data

      // Wait for next tick to ensure container dimensions are available
      await nextTick()

      const width = chartContainer.value.clientWidth
      const height = chartContainer.value.clientHeight
      const margin = {top: 30, right: 30, bottom: 70, left: 60}
      const innerWidth = width - margin.left - margin.right
      const innerHeight = height - margin.top - margin.bottom

      const svg = d3
        .select(chartContainer.value)
        .append('svg')
        .attr('width', width)
        .attr('height', height)
        .append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`)

      // X axis
      const x = d3
        .scaleBand()
        .range([0, innerWidth])
        .domain(chartData.map((d) => d.name))
        .padding(0.2)

      svg
        .append('g')
        .attr('transform', `translate(0,${innerHeight})`)
        .call(d3.axisBottom(x))
        .selectAll('text')
        .attr('transform', 'translate(-10,0)rotate(-45)')
        .style('text-anchor', 'end')

      // Y axis
      const y = d3
        .scaleLinear()
        .domain([0, d3.max(chartData, (d) => d.value) * 1.1])
        .range([innerHeight, 0])

      svg.append('g').call(d3.axisLeft(y))

      // Bars
      svg
        .selectAll('bars')
        .data(chartData)
        .enter()
        .append('rect')
        .attr('x', (d) => x(d.name))
        .attr('y', (d) => y(d.value))
        .attr('width', x.bandwidth())
        .attr('height', (d) => innerHeight - y(d.value))
        .attr('fill', '#4f46e5')
        .on('mouseover', function (event, d) {
          d3.select(this).attr('fill', '#818cf8')

          svg
            .append('text')
            .attr('class', 'value-label')
            .attr('x', x(d.name) + x.bandwidth() / 2)
            .attr('y', y(d.value) - 5)
            .attr('text-anchor', 'middle')
            .text(d.value)
        })
        .on('mouseout', function () {
          d3.select(this).attr('fill', '#4f46e5')
          svg.selectAll('.value-label').remove()
        })
    }

    const getTypeClass = (type) => {
      const classes = {
        micro: 'bg-green-100 text-green-800',
        nano: 'bg-blue-100 text-blue-800',
        regional: 'bg-purple-100 text-purple-800',
        brewpub: 'bg-yellow-100 text-yellow-800',
        large: 'bg-red-100 text-red-800',
        planning: 'bg-gray-100 text-gray-800',
        bar: 'bg-pink-100 text-pink-800',
        contract: 'bg-indigo-100 text-indigo-800',
        proprietor: 'bg-orange-100 text-orange-800',
        closed: 'bg-gray-100 text-gray-500',
      }
      return classes[type] || 'bg-gray-100 text-gray-800'
    }

    const debouncedSearch = _.debounce(searchBreweries, 500)

    const debouncedStateSearch = _.debounce(() => {
      currentPage.value = 1
      fetchBreweries()
    }, 500)

    const debouncedCitySearch = _.debounce(() => {
      currentPage.value = 1
      fetchBreweries()
    }, 500)

    const updateGroups = () => {
      if (groupBy.value) {
        groupBreweriesByAttribute()
        renderChart()
      } else {
        groups.value = {}
      }
    }

    const prevPage = () => {
      if (currentPage.value > 1) {
        currentPage.value--
        fetchBreweries()
      }
    }

    const nextPage = () => {
      currentPage.value++
      fetchBreweries()
    }

    const handleResize = _.debounce(() => {
      if (groupBy.value) renderChart()
    }, 250)

    watch(groupBy, updateGroups)

    onMounted(() => {
      fetchBreweries()
      window.addEventListener('resize', handleResize)
    })

    return {
      breweries,
      loading,
      error,
      selectedType,
      searchQuery,
      groupBy,
      currentPage,
      perPage,
      filters,
      chartContainer,
      groups,
      groupByLabel,
      breweryTypes,
      fetchBreweries,
      fetchRandomBrewery,
      debouncedSearch,
      debouncedStateSearch,
      debouncedCitySearch,
      updateGroups,
      getTypeClass,
      prevPage,
      nextPage,
    }
  },
}
</script>

<style scoped>
.container {
  max-width: 1200px;
  margin: 0 auto;
}

.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
