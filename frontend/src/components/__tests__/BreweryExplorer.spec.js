import {beforeEach, describe, expect, it, vi} from 'vitest'

import BreweryExplorer from '../BreweryExplorer.vue'
import axios from 'axios'
import {mount} from '@vue/test-utils'

vi.mock('axios')

describe('BreweryExplorer.vue', () => {
  beforeEach(() => {
    vi.resetAllMocks()
  })

  it('renders correctly', async () => {
    // arrange
    axios.get.mockResolvedValueOnce({
      data: [],
    })

    // act
    const wrapper = mount(BreweryExplorer)

    // Wait for component to be mounted and data to be loaded
    await vi.waitFor(() => {
      expect(wrapper.find('h1').exists()).toBe(true)
    })

    // assert
    expect(wrapper.find('h1').text()).toBe('Brewery Explorer')
    expect(wrapper.find('select[id="brewery-type"]').exists()).toBe(true)
    expect(wrapper.find('input[id="search-input"]').exists()).toBe(true)
    expect(wrapper.find('select[id="group-by"]').exists()).toBe(true)
  })

  it('fetches breweries on mount', async () => {
    // arrange
    const mockBreweries = [
      {id: '1', name: 'Test Brewery', brewery_type: 'micro'},
    ]
    axios.get.mockResolvedValueOnce({
      data: mockBreweries,
    })

    // act
    const wrapper = mount(BreweryExplorer)

    // assert
    await vi.waitFor(() => {
      expect(axios.get).toHaveBeenCalledWith(
        'http://localhost:8000/api/breweries',
        {
          params: {page: 1, per_page: 50},
        }
      )
      expect(wrapper.text()).toContain('Test Brewery')
    })
  })

  it('filters by brewery type', async () => {
    // arrange
    const mockBreweries = [
      {id: '1', name: 'Micro Brewery', brewery_type: 'micro'},
    ]
    axios.get
      .mockResolvedValueOnce({data: []})
      .mockResolvedValueOnce({data: mockBreweries})

    // act
    const wrapper = mount(BreweryExplorer)

    // Wait for initial load
    await vi.waitFor(() => {
      expect(axios.get).toHaveBeenCalledOnce()
    })

    // Find and update the select element
    const select = wrapper.find('select[id="brewery-type"]')
    expect(select.exists()).toBe(true)
    await select.setValue('micro')

    // assert
    await vi.waitFor(() => {
      expect(axios.get).toHaveBeenCalledTimes(2)
      expect(axios.get).toHaveBeenLastCalledWith(
        'http://localhost:8000/api/breweries',
        {
          params: {by_type: 'micro', page: 1, per_page: 50},
        }
      )
    })
  })

  it('searches breweries', async () => {
    // arrange
    const mockBreweries = [
      {id: '1', name: 'Dog Brewery', brewery_type: 'micro'},
    ]
    axios.get
      .mockResolvedValueOnce({data: []})
      .mockResolvedValueOnce({data: mockBreweries})

    // act
    const wrapper = mount(BreweryExplorer)

    // Wait for initial load
    await vi.waitFor(() => {
      expect(axios.get).toHaveBeenCalledOnce()
    })

    // Find and update the search input
    const searchInput = wrapper.find('input[id="search-input"]')
    expect(searchInput.exists()).toBe(true)
    await searchInput.setValue('dog')

    // Wait for debounce
    await new Promise((resolve) => setTimeout(resolve, 600))

    // assert
    await vi.waitFor(() => {
      expect(axios.get).toHaveBeenCalledTimes(2)
      expect(axios.get).toHaveBeenLastCalledWith(
        'http://localhost:8000/api/breweries/search',
        {
          params: {query: 'dog'},
        }
      )
    })
  })

  it('fetches random brewery', async () => {
    // arrange
    const mockBrewery = [
      {id: '1', name: 'Random Brewery', brewery_type: 'brewpub'},
    ]
    axios.get
      .mockResolvedValueOnce({data: []})
      .mockResolvedValueOnce({data: mockBrewery})

    // act
    const wrapper = mount(BreweryExplorer)

    // Wait for initial load
    await vi.waitFor(() => {
      expect(axios.get).toHaveBeenCalledOnce()
    })

    // Find and click the random button
    const randomButton = wrapper.find('button[id="random-brewery-btn"]')
    expect(randomButton.exists()).toBe(true)
    await randomButton.trigger('click')

    // assert
    await vi.waitFor(() => {
      expect(axios.get).toHaveBeenCalledTimes(2)
      expect(axios.get).toHaveBeenLastCalledWith(
        'http://localhost:8000/api/breweries/random',
        {
          params: {size: 1},
        }
      )
    })
  })

  it('groups breweries correctly', async () => {
    // arrange
    const breweries = [
      {id: '1', name: 'A', brewery_type: 'micro', state: 'NY'},
      {id: '2', name: 'B', brewery_type: 'brewpub', state: 'NY'},
      {id: '3', name: 'C', brewery_type: 'micro', state: 'CA'},
    ]

    axios.get.mockResolvedValueOnce({data: breweries})

    // act
    const wrapper = mount(BreweryExplorer)

    // Wait for initial load
    await vi.waitFor(() => {
      expect(wrapper.vm.breweries.length).toBe(3)
    })

    // Find and update the group by select
    const groupBySelect = wrapper.find('select[id="group-by"]')
    expect(groupBySelect.exists()).toBe(true)
    await groupBySelect.setValue('brewery_type')

    // assert
    await vi.waitFor(() => {
      expect(Object.keys(wrapper.vm.groups).length).toBe(2)
      expect(wrapper.vm.groups['micro'].length).toBe(2)
      expect(wrapper.vm.groups['brewpub'].length).toBe(1)
    })
  })
})
