<script>
	import { onMount } from "svelte";
	import {accountsBalanceViewVisible, positionsCockpitViewVisible, onwersAccountsCreatorViewVisible, CategoriesSubcategoriesList } from './components/store';
	import Header from "./components/Header.svelte";
	import Navbar from "./components/Navbar.svelte";
    import AccountsBalanceContainer from "./components/accountsBalance/accountsBalanceContainer.svelte";
	import IncExpCockpit from "./components/IncExp/IncExpCockpit.svelte"
	import OwnersAccountsCreator from "./components/ownersAccountsCreator/ownersAccountsCreator.svelte";

	async function getCategoriesSubcategories(){
        const resposne = await fetch(`/api/v1/types/categories/subcategories`, {method:"GET"})
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

	{#if $accountsBalanceViewVisible == true}
		<AccountsBalanceContainer/>
	{:else if $positionsCockpitViewVisible == true}
		<IncExpCockpit/>
	{:else if $onwersAccountsCreatorViewVisible == true}
		<OwnersAccountsCreator/>
	{/if}

</main>

<style>
	*{
		background-color:#131516;
		color: #fff;
	}
	main {
		background-color:#131516;
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