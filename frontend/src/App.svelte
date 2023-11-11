<script>
	import Header from "./components/Header.svelte";
	import FormContainer from "./components/form/FormContainer.svelte";
	
</script>

<main>
		<Header/>
		<FormContainer/>
</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}
	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>