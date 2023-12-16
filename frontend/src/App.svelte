<script>
	import Header from "./components/Header.svelte";
	import Navbar from "./components/Navbar.svelte";
	import FormContainer from "./components/form/FormContainer.svelte";
    import AccountsBalanceContainer from "./components/accountsBalance/accountsBalanceContainer.svelte";
	import MainContainer from "./components/positions/mainContainer.svelte";
	import {addPostionViewVisible, accountsBalanceViewVisible, expensesViewVisible } from './components/store';

	let addPostionViewVisibleValue;
	addPostionViewVisible.subscribe((value) => addPostionViewVisibleValue = value);

	let accountsBalanceViewVisibleValue;
	accountsBalanceViewVisible.subscribe((value) => accountsBalanceViewVisibleValue = value);

	let expensesViewVisibleValue;
	expensesViewVisible.subscribe((value) => expensesViewVisibleValue = value);


</script>

<main>
	<Header/>
	<Navbar/>
	{#if addPostionViewVisibleValue === true}
		<FormContainer/>
	{:else if accountsBalanceViewVisibleValue == true}
		<AccountsBalanceContainer/>
	{:else if expensesViewVisibleValue == true}
		<MainContainer/>
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