<template>
  <div class="min-h-screen bg-gray-100">
    <header class="bg-blue-600 text-white p-4 shadow-md">
      <div class="container mx-auto">
        <h1 class="text-2xl font-bold">Brewery Explorer</h1>
      </div>
    </header>
    
    <main class="container mx-auto py-6">
      <BreweryExplorer />
    </main>
    
    <footer class="bg-gray-200 p-4 mt-10">
      <div class="container mx-auto text-center text-gray-600">
        <p>Built with Django + Vue.js by Christopher Dambamuromo</p>
      </div>
    </footer>
  </div>
</template>

<script>
import BreweryExplorer from './components/BreweryExplorer.vue';

export default {
  name: 'App',
  components: {
    BreweryExplorer
  }
};
</script>