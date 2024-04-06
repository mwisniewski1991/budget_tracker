<script>
	import { onMount } from "svelte";
	import Header from "./components/Header.svelte";
	import Navbar from "./components/Navbar.svelte";
	import FormContainer from "./components/form/FormContainer.svelte";
    import AccountsBalanceContainer from "./components/accountsBalance/accountsBalanceContainer.svelte";
	import {accountsBalanceViewVisible, positionsCockpitViewVisible, CategoriesSubcategoriesList } from './components/store';
	import IncExpCockpit from "./components/IncExp/IncExpCockpit.svelte"
    import AcountsCard from "./components/accountsBalance/acountsCard.svelte";

	let accountsBalanceViewVisibleValue;
	accountsBalanceViewVisible.subscribe((value) => accountsBalanceViewVisibleValue = value);

	let positionsCockpitViewVisibleValue;
	positionsCockpitViewVisible.subscribe((value) => positionsCockpitViewVisibleValue = value);

	async function getCategoriesSubcategories(){
        const resposne = await fetch(`/api/v1/categories-subcategories`, {method:"GET"})
        const categoriesSubcategories = await resposne.json()
		CategoriesSubcategoriesList.set(categoriesSubcategories);
    };

	onMount(() => {
		getCategoriesSubcategories();
	});


</script>

<main>
	<Header/>
	<Navbar/>

	<!-- {#if addPostionViewVisibleValue === true} -->
		<!-- <FormContainer/> -->
	{#if accountsBalanceViewVisibleValue == true}
		<AccountsBalanceContainer/>
	{:else if positionsCockpitViewVisibleValue == true}
		<IncExpCockpit/>
	{/if}

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